import logging
from fastapi import Request

logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    # Log the request method and URL
    logger.info(f"Incoming request: {request.method} {request.url}")

    # Proceed with processing the request
    response = await call_next(request)

    return response
