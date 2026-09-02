from unittest.mock import MagicMock, patch

from logger.logger import CustomLogger


def test_debug_function_should_call_debug_in_logger_handler() -> None:

  logger_instance = None
  get_logger_mock = MagicMock()

  with patch("logger.logger.getLogger", autospec=True) as get_logger:
    get_logger.return_value = get_logger_mock
    logger_instance = CustomLogger()

  logger_instance.debug("debug message")
  get_logger_mock.debug.assert_called_once_with("debug message")


def test_info_function_should_call_info_in_logger_handler() -> None:

  logger_instance = None
  get_logger_mock = MagicMock()

  with patch("logger.logger.getLogger", autospec=True) as get_logger:
    get_logger.return_value = get_logger_mock
    logger_instance = CustomLogger()

  logger_instance.info("info message")
  get_logger_mock.info.assert_called_once_with("info message")


def test_warning_function_should_call_warning_in_logger_handler() -> None:

  logger_instance = None
  get_logger_mock = MagicMock()

  with patch("logger.logger.getLogger", autospec=True) as get_logger:
    get_logger.return_value = get_logger_mock
    logger_instance = CustomLogger()

  logger_instance.warning("warning message")
  get_logger_mock.warning.assert_called_once_with("warning message")


def test_error_function_should_call_error_in_logger_handler() -> None:

  logger_instance = None
  get_logger_mock = MagicMock()

  with patch("logger.logger.getLogger", autospec=True) as get_logger:
    get_logger.return_value = get_logger_mock
    logger_instance = CustomLogger()

  logger_instance.error("error message")
  get_logger_mock.error.assert_called_once_with("error message")
