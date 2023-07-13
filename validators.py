from fastapi import HTTPException
from authentications import get_password_hash


def validate_password(password: str, confirm_password: str):
    """Check password and confirm password matched or not.if matched then convert into hash password.

    Args:
        password (str): user passed password field value.
        confirm_password (str): user passed confirm password field value.

    Raises:
        HTTPException: Raise HTTPException if password or confirm password not mached.

    Returns:
        str: Return hashed password.
    """
    # Check password matching with confirm password
    if password != confirm_password:
        raise HTTPException(
            status_code=400, detail="Password and Confirm password not matched"
        )

    # Encode plain text to cypher text
    hash_password = get_password_hash(password=password)
    return hash_password
