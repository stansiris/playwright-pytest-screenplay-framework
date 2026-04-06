from contextlib import contextmanager
from functools import wraps


@contextmanager
def screenplay_step_ctx_manager(step_name: str):
    """Context manager for screenplay steps, handling setup and teardown."""
    # Setup code here
    print(f"Starting step: {step_name}")
    try:
        yield  # passes control to the `with` block
    except Exception as exc:
        print(f"Error in step '{step_name}': {exc}")
        raise
    finally:
        # Teardown code here
        print(f"Finished step: {step_name}")


def screenplay_step(step_name: str):
    """Factory for a decorator to wrap a function in a screenplay step context."""

    def decorator(func):
        """Decorator to wrap the target function in a screenplay step context."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            """Wrapper function that executes the target function within the step context."""
            with screenplay_step_ctx_manager(step_name):
                return func(*args, **kwargs)

        return wrapper

    return decorator


# def screenplay_step(step_name: str):
#     """
#     Factory for a decorator to wrap a function in a screenplay step context.
#     Simplified version without a context manager.
#     """
#     def decorator(func):  # wraps the target function
#         @wraps(func)  # preserves original function metadata
#         def wrapper(*args, **kwargs):  # executes target within step context
#             print(f"Starting step: {step_name}")
#             try:
#                 return func(*args, **kwargs)
#             except Exception as exc:
#                 print(f"Error in step '{step_name}': {exc}")
#                 raise
#             finally:
#                 print(f"Finished step: {step_name}")
#         return wrapper  # replaces the original function when decorated
#     return decorator  # returned decorator wraps any function with the step context
