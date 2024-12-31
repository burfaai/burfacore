from datetime import datetime
from typing import Callable, Any
from pathlib import Path


class burfa_step:
    """_summary_: Decorator for Burfa Pipeline Step"""

    def __init__(self, func: Callable[..., Any]):
        self.func = func
        self.func._pipeline_step = self.func.__name__
        self.func._log = Path("./.log.txt")

    def __call__(self, *args, **kwargs):
        with open(self.func._log.name, "a", encoding="utf-8") as ff:
            try:
                _func, _result = self.func.__name__, self.func(*args, **kwargs)
                ff.write(
                    f"Timestamp: {datetime.now().isoformat()}\tCalled: {self.func.__name__}(**)\tDescription: {self.func.__doc__}...\n"
                )
                return _func, _result
            except Exception as e:
                ff.write(
                    f"Timestamp: {datetime.now().isoformat()}\tError at: {self.func.__name__}(**)\tDescription: {self.func.__doc__}\tError: {e}...\n"
                )

                raise ValueError(
                    f"Error in {self.func.__name__} Pipeline State: {e}"
                ) from e
