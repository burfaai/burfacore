from uuid import uuid4
from datetime import datetime
from pydantic import BaseModel, Field, model_validator

from burfacore.core.types import (
    ComponentType,
    DatasetType,
    TaskType,
    Continent,
    Country,
    SectorType,
    Language,
)


def new_id():
    """_summary_"""
    return str(uuid4()).replace("-", "")


class BurfaBase(BaseModel):
    """_summary_: Class for Burfa base"""

    class Config:
        """_summary_: Pydantic Config class for Hyplate Models."""

        arbitrary_types_allowed = True
        use_enum_values = True
        validate_assignment = True
        evaluation_error_cause = True

    id: str = Field(
        default_factory=new_id,
        title="Object ID",
        description="Unique Identifier",
        example="123e4567e89b12d3a456426614174000",
        exclude=True,
    )
    created_at: str = Field(
        default=datetime.now().isoformat(),
        title="Created At",
        description="Creation Timestamp",
        example="2021-09-01T00:00:00Z",
    )

    @model_validator(mode="before")
    @classmethod
    def normalize(cls, data: dict) -> dict:
        """_summary_: Normalize Data"""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    data[key] = value.strip().lower()
        return data


def burfa_model_factory(
    properties: tuple[tuple[str, type[BurfaBase]]],
) -> type[BurfaBase]:
    """_summary_: Dynamically Create Burfa Data Models"""
    return type(
        "NewModel",
        (BurfaBase,),
        {
            "__str__": lambda self: f"{self.__class__.__name__}",
            "__annotations__": dict(properties),
        },
    )


class BurfaContext(BurfaBase):
    """_summary_: Base Classfor Burfa Context"""

    continent: Continent | None = Field(
        default=None,
        title="Component Continent",
        description="Continent of the component",
        example=Continent.get_values(),
    )
    country: Country = Field(
        default=Country.ANY.value,
        title="Component Country",
        description="Country of the component",
        example=Country.get_values(),
    )
    state: str | None = Field(
        default=None,
        title="Component State",
        description="State of the component",
        example="California",
    )
    sector: SectorType = Field(
        default=SectorType.ANY.value,
        title="Business Domain",
        description="Business domain of the component",
        example=SectorType.get_values(),
    )
    language: Language = Field(
        default=Language.ENGLISH.value,
        title="Component Language",
        description="DatasetLanguage of the component",
        example=Language.get_values(),
    )


class BaseFeature(BurfaBase):
    """_summary_: _description_"""

    feature_name: str = Field(
        ...,
        title="Feature Name",
        description="Name of the feature",
        example="transaction_amount",
    )
    feature_description: str = Field(
        ...,
        title="Feature Description",
        description="Description of the feature",
        example="Amount of the transaction",
    )
    feature_type: str = Field(
        ..., title="Feature Type", description="Type of the feature", example="numeric"
    )
    feature_sub_type: str = Field(
        ...,
        title="Feature Sub Type",
        description="Sub type of the feature",
        example="decimal",
    )
    is_target: bool = Field(
        ..., title="Is Target", description="Is the feature the target"
    )


class BurfaRequest(BurfaBase):
    """_summary_: Base Model for Creating Feature Requests"""

    component: ComponentType = Field(
        ...,
        title="Component Type",
        description="Type of the component",
        example=ComponentType.get_values(),
    )
    type: DatasetType = Field(
        ...,
        title="Dataset Type",
        description="Type of the component",
        example=DatasetType.get_values(),
    )
    goal: str = Field(
        ...,
        title="Component Goal",
        description="Goal of the component",
        example="To predict ......., To build ......., To test .......",
    )
    task: TaskType = Field(
        default=TaskType.CLASSIFICATION.value,
        title="Component Task",
        description="Task of the component",
        example=TaskType.get_values(),
    )
    sample_size: int = Field(
        default=100,
        title="Component Sample Size",
        description="Sample size of the component",
        example=100,
        le=100,
    )
    description: str | None = Field(
        default=None,
        title="Component Description",
        description="Description of the component",
        example="A Dataset of .......",
    )
    iterations: int = Field(
        default=2,
        title="Component Iterations",
        description="Number of iterations",
        example=1,
        ge=1,
        le=10,
    )
