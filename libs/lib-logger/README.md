# lib-logger

A small colored console logger built on Python's standard `logging` module.

## Installation

Install the library from the repository root:

```bash
uv pip install ./libs/lib-logger
```

For a uv-managed job, declare the package and its local source in `pyproject.toml`:

```toml
[project]
dependencies = [
  "lib_logger",
]

[tool.uv.sources]
lib_logger = { path = "../../libs/lib-logger" }
```

## Usage

```python
from logger.logger import CustomLogger


logger = CustomLogger()

logger.debug("Loading ticker configuration.")
logger.info("Live tickers job started.")
logger.warning("Ticker response was delayed.")
logger.error("Unable to process ticker response.")
```

Messages include a timestamp, log level, logger name, and message. Each level uses a different console color.

## Configuration

Use `LoggerConfig` to customize the logger name and output format:

```python
from logger.logger import CustomLogger
from logger.types import LoggerConfig


config = LoggerConfig(
  name="live_tickers",
  format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
  date_format="%Y-%m-%d %H:%M:%S",
)

logger = CustomLogger(config)
logger.info("Logger configured successfully.")
```

The default configuration logs at `DEBUG` level and defines colors for `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL` messages.
