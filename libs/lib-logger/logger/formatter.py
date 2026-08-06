from typing import Dict
from logging import LogRecord, Formatter
from colorama import Fore, Style # type: ignore

class ColoredFormatter(Formatter):

  def __init__ (
    self,
    fmt: str | None = None,
    datefmt: str | None = None,
    colors: Dict[int, str] | None = None
  ) -> None:

    if not fmt or not datefmt or not colors:
      raise Exception('Fmt, Datefmt and Colors configuration are required.')

    self._fmt: str | None = fmt
    self._datefmt: str | None = datefmt
    super().__init__ (
      fmt = self._fmt,
      datefmt = self._datefmt
    )
    self._colors: Dict[int, str] = colors

  def format(self, record: LogRecord | None = None) -> str:
    color: str = self._colors.get(
      record.levelno,
      Fore.WHITE
    )
    message: str = super().format(record)
    return f'{color} {message} {Style.RESET_ALL}'


