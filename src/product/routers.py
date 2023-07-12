from fastapi_crudrouter import SQLAlchemyCRUDRouter
from src.product.schemas import (
    ProductBaseSchema,
    ProductCreatePayloadSchema,
    ProductUpdatePayloadSchema,
    ProductResponseSchema,
    MessageSchema,
)
from database import get_db
from src.product.models import Product
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List
from src.product.services import get_product_by_id


# Create the router using SQLAlchemyCRUDRouter from fastapi_crudrouter
router = SQLAlchemyCRUDRouter(
    schema=ProductBaseSchema,
    create_schema=ProductCreatePayloadSchema,
    update_schema=ProductUpdatePayloadSchema,
    db_model=Product,
    db=get_db,
    get_all_route=False,
    get_one_route=False,
    create_route=False,
    update_route=False,
    delete_one_route=True,
    delete_all_route=False,
    tags=["Product"],
)


@router.get(
    "/products", response_model=List[ProductResponseSchema]
)  # response_model: how looks response
def get_products(db: Session = Depends(get_db)):
    """Retrieve all products from the database.

    Returns:
        Pydantic Schema: return List of ProductResponseSchema object.
    """

    # Get all Product record query
    products = db.query(Product).all()

    # Itrate all products object and return based on respective response schema's object
    lst_products = [ProductResponseSchema(**(vars(product))) for product in products]

    return lst_products


@router.post("/products", response_model=ProductResponseSchema)
def create_product(payload: ProductCreatePayloadSchema, db: Session = Depends(get_db)):
    """Create new product

    Args:
        payload (ProductCreatePayloadSchema): Product details, which need for create product record.
        db (Session, optional): Database session object. Defaults to Depends(get_db).

    Returns:
        Pydantic Schema: Return ProductResponseSchema object.
    """
    product = Product(
        name=payload.name,
        category=payload.category,
        price=payload.price,
    )

    # add product obj in database
    db.add(product)
    # commit changes
    db.commit()

    # return product object based on respective schema
    return ProductResponseSchema.from_orm(product)


@router.patch("/products", response_model=ProductResponseSchema)
def update_product(
    product_id: int, payload: ProductUpdatePayloadSchema, db: Session = Depends(get_db)
):
    """Update product object

    Args:
        product_id (int): product_id which need to update.
        payload (ProductUpdatePayloadSchema): Data which need to update.
        db (Session, optional): Database session object. Defaults to Depends(get_db).

    Returns:
        Pydantic schema: return updated record object
    """

    # return product object, which id pass
    product = get_product_by_id(product_id=product_id, db=db)

    if product:
        # convert into dict.
        update_data = payload.dict(exclude_unset=True)
        # ittrate dict items.
        for field, value in update_data.items():
            if value is not None:
                # update fields in to product object
                setattr(product, field, value)

        # add product obj in db
        db.add(product)
        # change commits
        db.commit()
        # refresh and reflact change
        db.refresh(product)

        # return product obj
        return ProductResponseSchema.from_orm(product)

    # return error message
    return MessageSchema(message=f"product_id: {product_id} not exist in database")
