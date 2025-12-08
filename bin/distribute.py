#!/usr/bin/env python3
import argparse
import json
import os
import shutil

import frontmatter


def get_command_map_substitutions(command_map, agent_name):
    """
    Returns a dictionary of substitutions for COMMAND_MAP placeholders
    for a specific agent.
    """
    subs = {}
    if agent_name in command_map:
        for command, value in command_map[agent_name].items():
            subs[f"{{COMMAND_MAP.{command}}}"] = value
    return subs


def transform_to_codex(post):
    """Transforms a post to the Codex format."""
    lines = ["---"]
    description = post.metadata.get("description", "")
    lines.append(f'description: "{description}"')

    arg_hint = post.metadata.get("argument-hint")
    if arg_hint:
        # Transform "[subject]" to "subject=<subject>"
        arg_name = arg_hint.strip("[]")
        lines.append(f"argument-hint: subject=<{arg_name}>")
    lines.append("---")
    lines.append("")
    lines.append(post.content)
    return "\n".join(lines)


def transform_to_gemini(post):
    """Transforms a post to the Gemini TOML format."""
    description = post.metadata.get("description", "")

    # Use triple quotes for description if it contains newlines
    if "\n" in description:
        description_str = f'"""\n{description}\n"""'
    else:
        description_str = f'"{description}"'

    return f'description = {description_str}\nprompt = """\n{post.content}\n"""\n'


def process_file(content, agent_prefix, command_map_subs):
    """Applies substitutions to the file content."""
    content = content.replace("{AGENT_PREFIX}", agent_prefix)
    for placeholder, value in command_map_subs.items():
        content = content.replace(placeholder, value)
    return content


def main():
    parser = argparse.ArgumentParser(
        description="Transpile and distribute agent markdown files."
    )
    parser.add_argument(
        "--deploy", action="store_true", help="Sync generated files to their locations."
    )
    args = parser.parse_args()

    # Get the project root, which is the parent directory of the script's directory
    script_dir = os.path.dirname(os.path.realpath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)

    dist_dir = "dist"
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir)

    with open("command-map.json", "r") as f:
        command_map = json.load(f)

    master_agents_file = "AGENTS.master.md"
    master_commands_dir = "commands.master"

    agents_config = {
        "claude": {
            "check_dir": os.path.expanduser("~/.claude"),
            "prefix": "",
            "master_dest": os.path.join(dist_dir, "claude", "CLAUDE.md"),
            "commands_dest_dir": os.path.join(dist_dir, "claude", "commands"),
            "deploy_master_dest": os.path.join(
                os.path.expanduser("~/.claude"), "CLAUDE.md"
            ),
            "deploy_commands_dest": os.path.join(
                os.path.expanduser("~/.claude"), "commands"
            ),
            "ext": ".md",
            "transform": lambda p: frontmatter.dumps(p),
        },
        "codex": {
            "check_dir": os.path.expanduser("~/.codex"),
            "prefix": "prompts:",
            "master_dest": os.path.join(dist_dir, "codex", "CODEX.md"),
            "commands_dest_dir": os.path.join(dist_dir, "codex", "commands"),
            "deploy_master_dest": os.path.join(
                os.path.expanduser("~/.codex"), "CODEX.md"
            ),
            "deploy_commands_dest": os.path.join(
                os.path.expanduser("~/.codex"), "commands"
            ),
            "ext": ".md",
            "transform": transform_to_codex,
        },
        "gemini": {
            "check_dir": os.path.expanduser("~/.gemini"),
            "prefix": "",
            "master_dest": os.path.join(dist_dir, "gemini", "GEMINI.md"),
            "commands_dest_dir": os.path.join(dist_dir, "gemini", "commands"),
            "deploy_master_dest": os.path.join(
                os.path.expanduser("~/.gemini"), "GEMINI.md"
            ),
            "deploy_commands_dest": os.path.join(
                os.path.expanduser("~/.gemini"), "commands"
            ),
            "ext": ".toml",
            "transform": transform_to_gemini,
        },
        "agents": {
            "check_dir": ".",  # Always exists
            "prefix": "",
            "master_dest": "AGENTS.md",
            "commands_dest_dir": "commands",
            "ext": ".md",
            "transform": lambda p: frontmatter.dumps(p),
        },
    }

    # Ensure master files exist
    if not os.path.exists(master_agents_file):
        print(f"Error: Master agents file not found at {master_agents_file}")
        return
    if not os.path.exists(master_commands_dir):
        print(f"Error: Master commands directory not found at {master_commands_dir}")
        return

    with open(master_agents_file, "r") as f:
        master_agents_content = f.read()

    command_files = [f for f in os.listdir(master_commands_dir) if f.endswith(".md")]

    for agent_name, config in agents_config.items():
        if agent_name != "agents" and not os.path.isdir(config["check_dir"]):
            print(f"Skipping {agent_name}: directory {config['check_dir']} not found.")
            continue

        print(f"Processing {agent_name}...")

        # For "agents", output is in root, not dist
        if agent_name == "agents":
            master_dest_path = config["master_dest"]
            commands_dest_path = config["commands_dest_dir"]
        else:
            master_dest_path = config["master_dest"]
            commands_dest_path = config["commands_dest_dir"]

        master_dest_dir = os.path.dirname(master_dest_path)
        if master_dest_dir:
            os.makedirs(master_dest_dir, exist_ok=True)
        os.makedirs(commands_dest_path, exist_ok=True)

        command_map_subs = get_command_map_substitutions(command_map, agent_name)

        # Process AGENTS.master.md
        processed_agents_content = process_file(
            master_agents_content, config["prefix"], command_map_subs
        )
        with open(master_dest_path, "w") as f:
            f.write(processed_agents_content)

        # Process commands.master/*.md
        for command_file in command_files:
            with open(os.path.join(master_commands_dir, command_file), "r") as f:
                try:
                    post = frontmatter.load(f)

                    # Also substitute in the body of the command
                    post.content = process_file(
                        post.content, config["prefix"], command_map_subs
                    )

                    transformed_content = config["transform"](post)

                    base_name = os.path.splitext(command_file)[0]
                    output_filename = f"{base_name}{config['ext']}"

                    with open(
                        os.path.join(commands_dest_path, output_filename), "w"
                    ) as out_f:
                        out_f.write(transformed_content + "\n")
                except Exception as e:
                    print(
                        f"Error processing file {command_file} for agent {agent_name}: {e}"
                    )

    print("\nTranspilation complete.")

    if args.deploy:
        print("Deploying files...")
        for agent_name, config in agents_config.items():
            if agent_name == "agents":
                continue  # Skip deploying the local "agents" files

            if not os.path.isdir(config["check_dir"]):
                continue

            print(f"Deploying {agent_name}...")

            # Deploy master file
            shutil.copy(config["master_dest"], config["deploy_master_dest"])

            # Deploy command files
            deploy_commands_dir = config["deploy_commands_dest"]
            if not os.path.exists(deploy_commands_dir):
                os.makedirs(deploy_commands_dir)

            source_commands_dir = config["commands_dest_dir"]
            for f in os.listdir(source_commands_dir):
                shutil.copy(
                    os.path.join(source_commands_dir, f),
                    os.path.join(deploy_commands_dir, f),
                )

        print("Deployment complete.")


if __name__ == "__main__":
    main()
