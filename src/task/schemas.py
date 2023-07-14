from pydantic import BaseModel, validator, conint
from datetime import datetime
from typing import Optional, Union
from src.task.models import TaskCategory


class TaskBaseSchema(BaseModel):
    """
    Represents the base schema for a task.
    """

    title: str
    category: str
    assign_to: Union[int, None]

    class Config:
        """
        Configuration options for the schema.
        """

        # Enable automatic conversion from attributes to dict during model initialization
        from_attributes = True

    @validator("category")
    def validate_category(cls, value):
        """
        Validator for the 'category' field of a task.

        Ensures that the provided category value is valid by checking if it is one of the
        values defined in the TaskCategory enum.

        Args:
            cls (Type[Task]): The class being validated.
            value (Any): The value of the 'category' field being validated.

        Returns:
            Any: The validated category value.

        Raises:
            ValueError: If the provided category value is not a valid category.
        """
        if value not in TaskCategory.__members__.values():
            raise ValueError("Invalid Category of Task.")
        return value


class TaskCreatePayloadSchema(TaskBaseSchema):
    """
    Represents the schema for creating a task.
    Inherits from TaskBaseSchema.
    """

    assign_to: Optional[conint(ge=1)] = None
    pass


class TaskResponseSchema(TaskBaseSchema):
    """
    Represents the schema for a task response.
    Inherits from TaskBaseSchema.
    """

    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TaskUpdatePayloadSchema(BaseModel):
    """
    Represents the schema for updating a task.
    """

    title: Optional[str] = None
    category: Optional[str] = None
    assign_to: Optional[conint(ge=1)] = None


class MessageSchema(BaseModel):
    """
    Represents a message schema.
    """

    message: str
