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
        attrs.update(dict(steps=[], total=0))
        for _, member in attrs.items():
            if hasattr(member, "_pipeline_step"):
                member._log.unlink(missing_ok=True)
                attrs.update(dict(log=member._log))
                attrs["steps"].append(member._pipeline_step)
                attrs["total"] += 1
        return super().__new__(cls, name, bases, attrs)


class BasePipeline(Generic[T, P], metaclass=PipelineMeta):
    """_summary_: Pipeline class for sequential functions"""

    def __init__(self, *args, **kwargs):
        """_summary_: Initialize pipeline"""
        super().__init__(*args, **kwargs)
        self.functions: Sequence[Callable[[Any], Any]] = []

    def next(self, function: Callable, *args, **kwargs):
        """_summary_: Add function to pipeline"""
        self.functions += [partial(function, *args, **kwargs)]

    def _init_pipeline(self, *args, **kwargs):
        """_summary_: Initialize This Pipeline"""
        self.next(self.start, *args, **kwargs)

    def run(self, *args, **kwargs) -> P:
        """_summary_: Kickoff pipeline"""
        self._init_pipeline(*args, **kwargs)
        return reduce(lambda _this, _next: _next(_this()), self.functions, initial=0)

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
    def run(self, *args, **kwargs) -> M:
        """_summary_: Execute"""
        raise NotImplementedError("Method not implemented")
