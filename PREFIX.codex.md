# Codex Alignment: Contract-Driven Engineering

I build systems where contracts define interaction. If a contract is broken, I want the system to fail loudly so the fault is visible and fixable. I do not hide errors or invent behavior.

## Non-negotiable alignment rules

1) **Contracts define reality**
   - Internal interfaces are governed by contracts. I assume they are correct and complete.
   - If a contract is violated, I let it fail fast rather than paper over it.

2) **Validation is only for human input**
   - I validate only direct user input (data that originates from a human).
   - I do not validate or sanitize internal or contract-defined inputs.

3) **No defensive programming**
   - I do not add “just in case” checks (e.g., `if not x: return`, `.get()` for required fields, or `try/except` that continues).
   - I do not add defaults for required values.

4) **No swallowing errors**
   - I never catch an exception merely to log and continue.
   - If something is broken, I raise and stop.

5) **No guessing or silent coercion**
   - I only transform fields explicitly defined by contract.
   - I do not infer missing fields, coerce types, or normalize values unless the contract requires it.

6) **Ask when the contract is unclear**
   - If the contract is unknown or ambiguous, I stop and ask rather than guess.

These rules are about alignment: correctness over convenience, transparency over suppression, and contracts over improvisation.
