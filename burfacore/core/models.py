import asyncio
import multiprocessing
from abc import abstractmethod
from functools import cached_property, partial, reduce
from typing import Any, TypeVar, Generic, Callable, Sequence
from burfacore.core.types import DatasetType, TaskType
from burfacore.core.schema import BurfaRequest


M = TypeVar("M")
P = TypeVar("P")
T = TypeVar("T", bound=BurfaRequest)


class BurfaModel(Generic[P]):
    """_summary_: Interface for All Models"""

    def __init__(self, dataset_type: DatasetType, task: TaskType, model_name: str):
        self.task = task
        self.model_name = model_name
        self.dataset_type = dataset_type

    @abstractmethod
    @cached_property
    def model(self) -> P:
        """_summary_: Model"""
        raise NotImplementedError("Method not implemented")


class PipelineMeta(type):
    """_summary_: Metaclass for Burfa task"""

    def __new__(cls, name: str, bases: tuple, attrs: dict):
        """_summary_: Create new Burfa Pipeline"""
        attrs.update(dict(steps=[]))
        for _, member in attrs.items():
            if "step" in member.__class__.__name__:
                attrs["steps"].append(_)
        return super().__new__(cls, name, bases, attrs)


class BasePipeline(Generic[T, P], metaclass=PipelineMeta):
    """_summary_: Pipeline class for sequential functions"""

    def __init__(self, *args, **kwargs):
        """_summary_: Initialize Pipeline"""
        super().__init__(*args, **kwargs)
        self.functions: Sequence[Callable[[Any], Any]] = []
        self.completed = 0

    def next(self, function: Callable, *args, **kwargs):
        """_summary_: Add a Pipeline Step to Pipeline Sequence"""
        self.functions += [partial(function, self, *args, **kwargs)]

    def _init_pipeline(self, *args, **kwargs):
        """_summary_: Initialize Pipeline Sequence"""
        self.next(self.start, *args, **kwargs)

    def _progress(self):
        """_summary_: Progress Bar"""
        return round((self.completed / len(self.functions)) * 100)

    def _call_func(self, _next: Callable, *args, **kwargs):
        """_summary_: Call Pipeline Step"""
        result = _next(*args, **kwargs)
        self.completed += 1
        print(
            f"Completed Step: {self.steps[self.completed-1]}\tProgress: {self._progress()}%"
        )
        return result

    async def run_async(self, *args, **kwargs) -> P:
        """_summary_: Run Pipeline"""
        self._init_pipeline(*args, **kwargs)
        return reduce(
            lambda _, _next: self._call_func(_next, *args, **kwargs), self.functions, 0
        )

    def run(self, *args, **kwargs) -> P:
        """_summary_: Run Pipeline"""
        asyncio.run(self.run_async(*args, **kwargs))

    @abstractmethod
    def start(self, *args, **kwargs):
        """_summary_: Starting Pipeline...."""
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def end(self, *args, **kwargs) -> P:
        """_summary_: Ending Pipeline...."""
        raise NotImplementedError("Method not implemented")


class BaseAgent(Generic[T, P, M]):
    """_summary_: Interface for All Burfa Agents"""

    def __init__(self, request: T):
        self.request = request

    @abstractmethod
    def execute(self, *args, **kwargs) -> M:
        """_summary_: Execute"""
        raise NotImplementedError("Method not implemented")

    def run(self, *args, **kwargs) -> M:
        """_summary_: Run"""
        with multiprocessing.Pool() as pool:
            return pool.map(
                partial(self.execute(*args, **kwargs)), range(self.request.iterations)
            )
