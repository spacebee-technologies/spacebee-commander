import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional
from enum import Enum

DEFAULT_LOGGER_NAME = 'app_logger'

class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    def __str__(self):
        return self.name

class ColoredFormatter(logging.Formatter):
    """Formatter que agrega colores ANSI a los logs en consola."""

    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m',       # Reset
        'BOLD': '\033[1m',        # Bold
        'DIM': '\033[2m',         # Dim
    }

    def format(self, record):
        original_levelname = record.levelname

        # Color levelname
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        record.levelname = f"{color}{record.levelname}{self.COLORS['RESET']}"

        # Format message
        formatted = super().format(record)

        # Go back to original
        record.levelname = original_levelname

        return formatted
class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

    def setup(self,
              log_name: str = DEFAULT_LOGGER_NAME,
              level: LogLevel = LogLevel.INFO,
              log_to_file: bool = True,
              log_dir: Optional[Path] = None,
              use_colors: bool = True):
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(level.value)

        # Clean existing handlers
        self.logger.handlers.clear()

        # Handler for console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level.value)

        supports_color = (
            use_colors and
            hasattr(sys.stdout, 'isatty') and
            sys.stdout.isatty()
        )
        # Format different according to level
        if level == LogLevel.DEBUG:
            format_string = '%(asctime)s [%(levelname)s] %(name)s.%(funcName)s:%(lineno)d - %(message)s'
        else:
            format_string = '%(asctime)s [%(levelname)s] - %(message)s'

        if supports_color:
            console_format = ColoredFormatter(format_string, datefmt='%H:%M:%S')
        else:
            console_format = logging.Formatter(format_string, datefmt='%H:%M:%S')

        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)

        # Handler for file (DEBUG)
        if log_to_file:
            if log_dir is None:
                log_dir = Path.home() / '.spacebee_commander' / 'logs'

            log_dir.mkdir(parents=True, exist_ok=True)

            log_file_path = log_dir / f'{log_name}.log'

            file_handler = logging.handlers.RotatingFileHandler(
                log_file_path,
                maxBytes=10485760,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(logging.DEBUG)

            file_format = logging.Formatter(
                '%(asctime)s [%(levelname)s] %(name)s.%(funcName)s:%(lineno)d - %(message)s'
            )
            file_handler.setFormatter(file_format)
            self.logger.addHandler(file_handler)
            self.logger.info(f"Logging to file: {log_file_path}")


        self.logger.info(f"Logger configured to level: {level.name}")
