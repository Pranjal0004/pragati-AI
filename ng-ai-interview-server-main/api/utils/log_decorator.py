import functools
import time
import traceback
from loguru import logger
from typing import Any, Callable

def log(func: Callable) -> Callable:
    """
    A decorator that logs function entry and exit with parameters and result
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Get function name and arguments
        func_name = func.__name__
        class_name = args[0].__class__.__name__ if args else None
        
        # Log function entry
        logger.info(
            f"Enter {class_name}.{func_name}\n"
            f"Args: {args[1:] if class_name else args}\n"
            f"Kwargs: {kwargs}"
        )
        
        # Record start time
        start_time = time.time()
        
        try:
            # Execute function
            result = await func(*args, **kwargs)
            
            # Calculate execution time
            execution_time = time.time() - start_time
            
            # Log successful execution with time
            logger.info(
                f"Exit {class_name}.{func_name}\n"
                f"Result: {result}\n"
                f"Execution time: {execution_time:.3f}s"
            )
            return result
            
        except Exception as e:
            # Calculate execution time even for errors
            execution_time = time.time() - start_time
            
            # Capture the stack trace
            stack_trace = traceback.format_exc()
            
            # Log error with stack trace and time
            logger.error(
                f"Error in {class_name}.{func_name}\n"
                f"Error: {str(e)}\n"
                f"Stack trace: {stack_trace}\n"
                f"Execution time: {execution_time:.3f}s"
            )
            raise
    
    return wrapper 