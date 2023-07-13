from database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from src.user.models import User
from fastapi.exceptions import HTTPException
from src.user.schemas import UserResponseSchema


def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Get user based on user id

    Args:
        user_id (int): user id which obj want to get.
        db (Session, optional): Database session object. Defaults to Depends(get_db).

    Raises:
        HTTPException: Raise exception if id not exist in db.

    Returns:
        User object: Return User object
    """
    if user_id:
        user = db.query(User).get(user_id)
        if not user:
            raise HTTPException(
                status_code=400, detail=f"User id: {user_id} not exist in database"
            )

        return user
    return None
