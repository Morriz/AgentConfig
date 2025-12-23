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

## Logging routine (TeleClaude standard)

Use levels consistently so logs stay tail-friendly and meaningful.

### Levels

- **INFO**: Business-relevant events (user-visible state changes, lifecycle milestones, deploy status).
- **DEBUG**: Successful outcomes (one line per operation; include duration/summary).
- **TRACE**: High-volume or step-by-step chatter (start lines, loop ticks, raw payloads).
- **WARNING**: Recoverable anomalies (retries, unexpected states, missing optional data).
- **ERROR/CRITICAL**: Failures or contract violations that should be fixed.

### Start/End pairs

- Prefer **one line** per operation: log the *completion* at DEBUG with duration.
- If you keep a start line, log it at TRACE and keep the completion at DEBUG.

### Consistency

- Reuse the same message template for the same event.
- Favor structured key/value pairs (e.g., `event=heartbeat_sent`, `duration_ms=...`).
- Throttle or aggregate repetitive logs; identical messages aggregate better.
