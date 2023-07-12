from fastapi_crudrouter import SQLAlchemyCRUDRouter
from src.user.schemas import (
    UserBaseSchema,
    UserCreatePayloadSchema,
    UserUpdatePayloadSchema,
    UserResponseSchema,
    MessageSchema,
)
from database import get_db
from src.user.models import User
from fastapi import Depends
from sqlalchemy.orm import Session
from validators import validate_password
from typing import List
from src.user.services import get_user_by_id


# Create the router using SQLAlchemyCRUDRouter from fastapi_crudrouter
router = SQLAlchemyCRUDRouter(
    schema=UserBaseSchema,
    create_schema=UserCreatePayloadSchema,
    update_schema=UserUpdatePayloadSchema,
    db_model=User,
    db=get_db,
    get_all_route=False,
    get_one_route=False,
    create_route=False,
    update_route=False,
    delete_one_route=True,
    delete_all_route=False,
    tags=["User"],
)


@router.get("/users", response_model=List[UserResponseSchema])
def get_users(db: Session = Depends(get_db)):
    """Get all the users

    Args:
        db (Session, optional): Database session object. Defaults to Depends(get_db).

    Returns:
        Pydantic Schema's list: list of user objects
    """
    # Get all User record query
    users = db.query(User).all()

    # Itrate all users object and return based on respective response schemas
    lst_users = [UserResponseSchema(**(vars(user))) for user in users]

    return lst_users


@router.post("/users", response_model=UserResponseSchema)
def create_user(payload: UserCreatePayloadSchema, db: Session = Depends(get_db)):
    """Create new user

    Args:
        payload (UserCreatePayloadSchema): User details, which need for create product record.
        db (Session, optional): Database session object. Defaults to Depends(get_db).

    Returns:
        Pydantic Schema: Return ProductResponseSchema object.
    """
    # validate password
    check_password = validate_password(
        password=payload.password, confirm_password=payload.confirm_password
    )

    if check_password:
        user = User(
            username=payload.username,
            email=payload.email,
            phn_no=payload.phn_no,
            password=payload.password,
        )
        # add user obj in database
        db.add(user)
        # commit changes
        db.commit()

        # return user obj based on respective schema
        return UserResponseSchema.from_orm(user)


@router.patch("/users", response_model=UserResponseSchema)
def update_user(
    user_id: int, payload: UserUpdatePayloadSchema, db: Session = Depends(get_db)
):
    """Update user object

    Args:
        user_id (int): product_id which need to update.
        payload (UserUpdatePayloadSchema):  Data which need to update.
        db (Session, optional): Database session object. Defaults to Depends(get_db).

    Returns:
        Pydantic schema: return updated record object
    """
    # return user object, which id pass
    user = get_user_by_id(user_id=user_id, db=db)

    if user:
        # convert into dict.
        update_data = payload.dict(exclude_unset=True)
        # ittrate dict items.
        for field, value in update_data.items():
            if value is not None:
                # update fields in to product object
                setattr(user, field, value)

        # add user obj in dbF
        db.add(user)
        # change commits
        db.commit()
        # refresh and reflact change
        db.refresh(user)

        # return user obj
        return UserResponseSchema.from_orm(user)

    # return error message
    return MessageSchema(message=f"user_id: {user_id} not exist in database")
