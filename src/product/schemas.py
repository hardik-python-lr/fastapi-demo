from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProductBaseSchema(BaseModel):
    """
    Represents the base schema for a product.
    """

    name: str
    category: str
    price: int
    available: Optional[bool]

    class Config:
        """
        Configuration options for the schema.
        """

        # Enable automatic conversion from attributes to dict during model initialization
        from_attributes = True


class ProductCreatePayloadSchema(ProductBaseSchema):
    """
    Represents the schema for creating a product.
    Inherits from ProductBaseSchema.
    """

    pass


class ProductResponseSchema(ProductBaseSchema):
    """
    Represents the schema for a product response.
    Inherits from ProductBaseSchema.
    """

    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ProductUpdatePayloadSchema(BaseModel):
    """
    Represents the schema for updating a product.
    """

    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[int] = None
    available: Optional[bool] = True


class MessageSchema(BaseModel):
    """
    Represents a message schema.
    """

    message: str
