from selenium.common.exceptions import NoSuchElementException, TimeoutException
from loguru import logger


def handle_find_element_exceptions(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except NoSuchElementException:
            if len(args) > 1:
                logger.warning(f"No such element {args[3]}")
            return None
        except TimeoutException:
            if len(args) > 1:
                logger.warning(
                    f"Timeout Exception: Element not found | For value: {args[3]}"
                )
            return None
        except Exception as e:
            if len(args) > 1:
                logger.error(f"{e} {args[3]}")
            return None

    return wrapper


def handle_general_exceptions(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except TypeError as e:
            logger.debug(e)
            return None
        except ValueError as e:
            logger.debug(e)
            return None
        except Exception as e:
            logger.debug(e)
            return None

    return wrapper
