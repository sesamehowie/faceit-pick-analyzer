import random
import asyncio
from functools import wraps
from data.config import MAX_RETRIES


def retry(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        retries = MAX_RETRIES
        for attempt in range(retries):
            try:
                # Attempt to execute the function
                return await func(*args, **kwargs)
            except Exception as e:
                # If it's the last attempt, raise the exception
                if attempt == retries:
                    raise
                # Log the exception and retry after a delay (optional)
                print(f"Attempt {attempt + 1} failed with error: {str(e)}. Retrying...")
                await asyncio.sleep(
                    random.randint(2, 5)
                )  # You can adjust the delay as needed

    return wrapper
