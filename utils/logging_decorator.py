import logging
from typing import Iterable

logger = logging.getLogger(__name__)

def log_db_operation(func):
    def wrapper(*args, **kwargs):
        # Convert args and kwargs to a more readable format
        formatted_args = [str(arg) for arg in args]
        formatted_kwargs = {k: str(v) for k, v in kwargs.items()}

        logger.info(f"DB Operation: {func.__name__} called with args: {formatted_args}, kwargs: {formatted_kwargs}")
        try:
            result = func(*args, **kwargs)

            # Format the result for logging
            if isinstance(result, Iterable) and not isinstance(result, str):
                formatted_result = f"[{', '.join(str(item) for item in result)}]"
            else:
                formatted_result = str(result)

            logger.info(f"DB Operation Successful: {func.__name__} returned {formatted_result}")
            return result
        except Exception as e:
            logger.error(f"DB Operation Failed: {func.__name__} raised {e}")
            raise
    return wrapper
