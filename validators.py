from fastapi import HTTPException
from authentications import get_password_hash


def validate_password(password: str, confirm_password: str):
    # Check password matching with confirm password
    if password != confirm_password:
        raise HTTPException(
            status_code=400, detail="Password and Confirm password not matched"
        )

    # Encode plain text to cypher text
    hash_password = get_password_hash(password=password)
    return hash_password
