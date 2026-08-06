# lib-exception

Shared application exceptions with consistent status codes.

## Installation

Install the library from the repository root:

```bash
uv pip install ./libs/lib-exception
```

For a uv-managed job, declare the package and its local source in `pyproject.toml`:

```toml
[project]
dependencies = [
  "lib_exception",
]

[tool.uv.sources]
lib_exception = { path = "../../libs/lib-exception" }
```

## Exceptions

| Exception | Status | Purpose |
| --- | ---: | --- |
| `BaseException` | — | Base class for application exceptions |
| `MissingException` | 404 | A required resource or value is missing |
| `ValidationException` | 400 | Input or configuration is invalid |

## Usage

```python
from exception.missing_exception import MissingException
from exception.validation_exception import ValidationException


def get_ticker(symbol: str) -> dict:
  if not symbol:
    raise ValidationException("A ticker symbol is required.")

  ticker = None

  if ticker is None:
    raise MissingException(f"Ticker {symbol} was not found.")

  return ticker
```

Catch all exceptions provided by this library through the base class:

```python
from exception.base_exception import BaseException as ApplicationException


try:
  ticker = get_ticker("BTC/USDT")
except ApplicationException as error:
  status = getattr(error, "status", 500)
  print(status, str(error))
```
