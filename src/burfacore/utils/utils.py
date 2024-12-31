from datetime import datetime
from typing import Callable, Any


class burfa_step:
    """_summary_: Decorator for Burfa Pipeline Step"""

    def __init__(self, func: Callable[..., Any]):
        self.func = func

    def __call__(self, *args, **kwargs):
        try:
            _result = self.func(*args, **kwargs)
            _log = f"Timestamp: {datetime.now().isoformat()}\tCalled: {self.func.__name__}(**)\tDescription: {self.func.__doc__}...\n"
            print(_log)
            return _result
        except Exception as e:
            log = f"Timestamp: {datetime.now().isoformat()}\tError at: {self.func.__name__}(**)\tDescription: {self.func.__doc__}\tError: {e}...\n"
            print(log)
            raise ValueError(
                f"Error in {self.func.__name__} Pipeline State: {e}"
            ) from e
