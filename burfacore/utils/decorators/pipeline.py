from typing import Callable, Any


class burfa_step:
    """_summary_: Decorator for Burfa Pipeline Step"""

    def __init__(self, func: Callable[..., Any]):
        self.func = func

    def __call__(self, *args, **kwargs):
        try:
            _result = self.func(*args, **kwargs)
            print(
                f"Called: {self.func.__name__}(**)\tDescription: {self.func.__doc__}..."
            )
            return _result
        except Exception as e:
            print(
                f"Error at: {self.func.__name__}(**)\tDescription: {self.func.__doc__}\tError: {e}..."
            )
            raise ValueError(
                f"Error in {self.func.__name__} Pipeline State: {e}"
            ) from e
