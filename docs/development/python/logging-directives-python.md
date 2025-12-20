# Python Logging Directives (InstruktAI Standard)

Use the shared InstruktAI logger in every Python service to keep logs readable, tail-friendly, and free of third-party spam by default.

## Dependency

- PyPI package: `instruktai-python-logger`
- Import module: `instrukt_ai_logging`

## Minimum integration

Call `configure_logging(...)` exactly once at process start (before importing/initializing chatty libraries if possible).

```py
from instrukt_ai_logging import configure_logging

configure_logging("myapp")
```

## Log output contract

- Single primary log file per service: `/var/log/instrukt-ai/{app}/{app}.log`
- Format: logfmt-style `key=value` pairs (easy for humans + AIs to grep)
- Prefer structured pairs over interpolated strings:

```py
import logging

logger = logging.getLogger("instrukt_ai.myapp.worker")
logger.info("job_started", job_id=job_id, user_id=user_id)
```

Values in `**kv` can be any Python object; they are serialized to text for the log line.

## Levels (ours vs third-party)

You control two independent levels:

- `{ENV_PREFIX}_LOG_LEVEL` (our code, i.e. loggers starting with `app_logger_prefix`)
- `{ENV_PREFIX}_THIRD_PARTY_LOG_LEVEL` (everything else)

Optional “spotlight” for third-party debugging:

- `{ENV_PREFIX}_THIRD_PARTY_LOGGERS` = comma-separated logger-name prefixes
  - If set: only those third-party prefixes are allowed at `{ENV_PREFIX}_THIRD_PARTY_LOG_LEVEL`
  - All other third-party loggers are forced to WARNING+ (to prevent spam)

Examples:

```bash
# normal: our debug, third-party quiet
export MYAPP_LOG_LEVEL=DEBUG
export MYAPP_THIRD_PARTY_LOG_LEVEL=WARNING

# temporarily inspect one or more libraries without turning on global spam
export MYAPP_THIRD_PARTY_LOG_LEVEL=INFO
export MYAPP_THIRD_PARTY_LOGGERS="httpcore,httpx,telegram"
```

## Log root override

Override the log root (useful for dev, containers, or non-root installs):

```bash
export INSTRUKT_AI_LOG_ROOT="$PWD/logs"
```

This changes the target path to: `$INSTRUKT_AI_LOG_ROOT/{app}/{app}.log`.
