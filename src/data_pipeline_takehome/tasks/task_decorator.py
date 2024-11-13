from contextlib import contextmanager
import functools
import random

from data_pipeline_takehome.utilities.tasks import (
    ConfigurationManager,
    SignatureManager,
)
from ..utilities.logging import get_logger

task_call_stack = []


class TaskCallStackExceededException(Exception):
    pass


def validate_task_call_stack() -> bool:
    global task_call_stack
    if len(task_call_stack) > 1:
        tasks = ", ".join(task_call_stack)
        task_call_stack = []
        raise TaskCallStackExceededException(f"Task call stack exceeded with {tasks}")
    return True


@contextmanager
def track_task_call(func_name):
    global task_call_stack
    task_call_stack.append(func_name)
    try:
        yield
    finally:
        task_call_stack.pop()


def task(_func=None, retry_count=3, failure_rate: float = 0.1):

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = get_logger(func.__name__)
            logger.info("Task init")

            logger.info("Validating Task Call Stack")
            validate_task_call_stack()

            logger.info("Validating Configuration")
            signature_analysis = SignatureManager.analyze(func, *args, **kwargs)
            if signature_analysis.config_included:
                args = [ConfigurationManager.build_config(logger), *args]

            with track_task_call(func.__name__):

                logger.info("Executing Function")

                attempt = 0
                while attempt < retry_count:
                    try:
                        if random.random() < failure_rate:  # noqa: S311
                            msg = "Unexpected error occurred"
                            raise ValueError(msg)
                        func_return = func(*args, **kwargs)
                        break
                    except Exception as e:
                        logger.error(e)
                        # add backoff here too for network related issues
                        logger.info("Retrying...")
                        attempt += 1
                        if attempt >= retry_count:
                            raise

                logger.info("Validting Function Return")
                signature_analysis.check_return(func_return)
                return func_return

        return wrapper

    if _func is None:
        return decorator
    return decorator(_func)
