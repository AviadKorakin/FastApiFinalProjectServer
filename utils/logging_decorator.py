import logging
from typing import Iterable
from sqlalchemy.engine import Row  # Importing to handle SQLAlchemy row results

logger = logging.getLogger(__name__)

def log_db_operation(func):
    async def wrapper(*args, **kwargs):  # Make the decorator async-friendly if needed
        # Convert args and kwargs to a more readable format
        formatted_args = [str(arg) for arg in args]
        formatted_kwargs = {k: str(v) for k, v in kwargs.items()}

        logger.info(f"DB Operation: {func.__name__} called with args: {formatted_args}, kwargs: {formatted_kwargs}")
        try:
            result = await func(*args, **kwargs) if callable(func) else func(*args, **kwargs)  # Ensure async compatibility

            # Format the result for logging
            if isinstance(result, Iterable) and not isinstance(result, str):
                # If it's an iterable but not a string, log its elements
                if all(isinstance(item, Row) for item in result):
                    # For SQLAlchemy rows, log each row's dictionary representation
                    formatted_result = f"[{', '.join(str(dict(item)) for item in result)}]"
                else:
                    formatted_result = f"[{', '.join(str(item) for item in result)}]"
            else:
                # Log the result directly if it's not an iterable
                formatted_result = str(result)

            logger.info(f"DB Operation Successful: {func.__name__} returned {formatted_result}")
            return result
        except Exception as e:
            logger.error(f"DB Operation Failed: {func.__name__} raised {e}")
            raise
    return wrapper
