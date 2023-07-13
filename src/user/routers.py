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
    prefix="/users",
)


@router.get("", response_model=List[UserResponseSchema])
def get_users(db: Session = Depends(get_db)):
    """Get all the users

    Args:
        db (Session, optional): Database session object. Defaults to Depends(get_db).

    Returns:
        List of UserResponseSchema: List of user objects
    """
    # Get all User records from the database
    all_users = db.query(User).all()

    # Iterate through all users and return them based on the response schema
    return [UserResponseSchema(**(vars(user))) for user in all_users]


@router.post("", response_model=UserResponseSchema)
def create_user(payload: UserCreatePayloadSchema, db: Session = Depends(get_db)):
    """Create a new user

    Args:
        payload (UserCreatePayloadSchema): User details needed to create a new user record.
        db (Session, optional): Database session object. Defaults to Depends(get_db).

    Returns:
        UserResponseSchema: Newly created user object
    """
    # Validate password
    check_password = validate_password(
        password=payload.password, confirm_password=payload.confirm_password
    )

    if check_password:
        # Create a new User object with the provided details
        new_user = User(
            username=payload.username,
            email=payload.email,
            phn_no=payload.phn_no,
            password=check_password,
        )
        # Add the user object to the database
        db.add(new_user)
        # Commit the changes to the database
        db.commit()

        # Return the user object based on the response schema
        return UserResponseSchema.from_orm(new_user)


@router.patch("/{user_id}", response_model=UserResponseSchema)
def update_user(
    user_id: int, payload: UserUpdatePayloadSchema, db: Session = Depends(get_db)
):
    """Update a user object

    Args:
        user_id (int): ID of the user to update.
        payload (UserUpdatePayloadSchema): Data to update the user with.
        db (Session, optional): Database session object. Defaults to Depends(get_db).

    Returns:
        UserResponseSchema: Updated user object
    """
    # Get the user object based on the provided user_id
    user = get_user_by_id(user_id=user_id, db=db)

    if user:
        # Convert the payload to a dictionary and exclude unset values
        update_data = payload.dict(exclude_unset=True)

        # Iterate through the dictionary items
        for field, value in update_data.items():
            if value is not None:
                # Update the fields in the user object
                setattr(user, field, value)

        # Add the updated user object to the database
        db.add(user)
        # Commit the changes to the database
        db.commit()
        # Refresh and reflect the changes
        db.refresh(user)

        # Return the updated user object based on the response schema
        return UserResponseSchema.from_orm(user)

    # Return an error message if the user_id doesn't exist in the database
    return MessageSchema(message=f"user_id: {user_id} does not exist in the database")
