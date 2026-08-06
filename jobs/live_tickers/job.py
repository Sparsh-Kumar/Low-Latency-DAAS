import asyncio

from exception.missing_exception import MissingException  # type: ignore
from exception.validation_exception import ValidationException  # type: ignore
from logger.logger import CustomLogger  # type: ignore


async def main() -> None:
  print(MissingException)
  print(ValidationException)
  print(CustomLogger)


if __name__ == "__main__":
  asyncio.run(main())
