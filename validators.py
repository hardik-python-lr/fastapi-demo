from fastapi import HTTPException
from authentications import get_password_hash


def validate_password(password: str, confirm_password: str):
    """Validate the password and confirm password.

    Args:
        password (str): Password to validate.
        confirm_password (str): Confirmation password to compare against.

    Returns:
        str: Hashed password if validation passes.

    Raises:
        HTTPException: If the password and confirm password do not match.
    """
    # Check if the password matches the confirm password
    if password != confirm_password:
        raise HTTPException(
            status_code=400, detail="Password and Confirm password do not match"
        )

    # Hash the password
    hashed_password = get_password_hash(password=password)
    return hashed_password
