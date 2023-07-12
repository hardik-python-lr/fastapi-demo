from database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from src.product.models import Product
from fastapi.exceptions import HTTPException


def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """Get product based on product id

    Args:
        product_id (int): product id, which want to get.
        db (Session, optional): Database session object. Defaults to Depends(get_db).

    Raises:
        HTTPException: Raise Exception, if id not exist in database.

    Returns:
        Product object: return product obj.
    """
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(
            status_code=400, detail=f"Product id: {product_id} not exist in database"
        )

    return product
