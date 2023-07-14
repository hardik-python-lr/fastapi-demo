from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional
from email_validator import validate_email, EmailNotValidError
import re


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

    @validator("email")
    def validate_email(cls, value):
        """
        Validator for the 'email' field of a user.

        Validates that the provided email address is in a valid format.

        Args:
            cls (Type[User]): The class being validated.
            value (Any): The value of the 'email' field being validated.

        Returns:
            str: The validated and normalized email address.

        Raises:
            ValueError: If the provided email address is not valid.
        """

        try:
            emailinfo = validate_email(value)

            # After this point, use only the normalized form of the email address,
            email = emailinfo.normalized
            return email
        except EmailNotValidError as e:
            raise ValueError("Not a valid email address.")

    @validator("phn_no")
    def validate_phn_no(cls, value):
        """
        Validator for the 'phn_no' field of a user.

        Validates that the provided phone number is in a valid format.

        Args:
            cls (Type[User]): The class being validated.
            value (Any): The value of the 'phn_no' field being validated.

        Returns:
            str: The validated phone number.

        Raises:
            ValueError: If the provided phone number is not valid.
        """
        phone_number = str(value)
        if not isinstance(phone_number, str):
            raise ValueError("Phone number must be a string")

        pattern = r"^\+?\d{1,3}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$"
        # The regex pattern used for phone number validation

        if re.match(pattern, phone_number):
            return phone_number
        else:
            raise ValueError("Invalid phone number format")


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
