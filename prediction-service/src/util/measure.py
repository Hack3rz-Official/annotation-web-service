from functools import wraps
from time import process_time
import logging
logger = logging.getLogger('waitress')


def measure(func):
    """
    Function to measure the time it takes to execute a function
    :param func: a function that will be measured
    :return: the function wrapped with the measuring function
    """
    @wraps(func)
    def _time_it(*args, **kwargs):
        start = int(round(process_time() * 1000))
        try:
            return func(*args, **kwargs)
        finally:
            end_ = int(round(process_time() * 1000)) - start
            logger.debug(
                f"Total execution time {func.__name__}: {end_ if end_ > 0 else 0} ms"
            )

    return _time_it
