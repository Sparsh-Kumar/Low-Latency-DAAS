from typing import TextIO
from logging import Logger, StreamHandler, getLogger
from .types import LoggerConfig
from .formatter import ColoredFormatter

class CustomLogger:
  def __init__(
    self,
    logger_config: LoggerConfig | None = None
  ) -> None:
    self._logger_config: LoggerConfig = logger_config or LoggerConfig()
    self._logger: Logger = getLogger(self._logger_config.name)
    self._logger.setLevel(self._logger_config.level)

    logger_console_handler: StreamHandler[TextIO] = StreamHandler()
    logger_console_handler.setFormatter(
      ColoredFormatter(
        self._logger_config.format,
        self._logger_config.date_format,
        self._logger_config.colors
      )
    )
    self._logger.addHandler(logger_console_handler)

  def debug (self, message: str = '') -> None:
    self._logger.debug(message)

  def info (self, message: str = '') -> None:
    self._logger.info(message)

  def warning (self, message: str = '') -> None:
    self._logger.warning(message)

  def error (self, message: str = '') -> None:
    self._logger.error(message)

