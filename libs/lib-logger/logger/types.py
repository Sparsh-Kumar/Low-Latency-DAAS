import logging
from colorama import Fore, Style # type: ignore
from dataclasses import dataclass, field
from typing import Dict, Literal

@dataclass
class LoggerConfig:
  name: str = 'app_logger'
  level: Literal[10] = logging.DEBUG
  format: str = '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
  date_format: str = '%Y-%m-%d %H:%M:%S'
  colors: Dict[int, str] = field(
    default_factory = lambda: {
      logging.DEBUG: Fore.CYAN,
      logging.INFO: Fore.GREEN,
      logging.WARNING: Fore.YELLOW,
      logging.ERROR: Fore.RED,
      logging.CRITICAL: Fore.RED + Style.BRIGHT
    }
  )

