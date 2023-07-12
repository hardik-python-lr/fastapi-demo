from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserBaseSchema(BaseModel):
    """
    Represents the base schema for a user.
    """

    username: str
    email: str
    phn_no: int

    class Config:
        """
        Configuration options for the schema.
        """

        # Enable automatic conversion from attributes to dict during model initialization
        from_attributes = True


class UserCreatePayloadSchema(UserBaseSchema):
    """
    Represents the schema for creating a user.
    Inherits from UserBaseSchema.
    """

    password: str
    confirm_password: str


class UserResponseSchema(UserBaseSchema):
    """
    Represents the schema for a user response.
    Inherits from UserBaseSchema.
    """

    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UserUpdatePayloadSchema(BaseModel):
    """
    Represents the schema for updating a user.
    """

    username: Optional[str] = None
    email: Optional[str] = None
    phn_no: Optional[int] = None


class MessageSchema(BaseModel):
    """
    Represents a message schema.
    """

    message: str
