from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Union


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


class TaskCreatePayloadSchema(TaskBaseSchema):
    """
    Represents the schema for creating a task.
    Inherits from TaskBaseSchema.
    """

    assign_to: Optional[int] = None
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
    assign_to: Optional[int] = None


class MessageSchema(BaseModel):
    """
    Represents a message schema.
    """

    message: str
