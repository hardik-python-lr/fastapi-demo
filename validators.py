from fastapi import HTTPException


def validate_password(password: str, confirm_password: str):
    # Check password matching with confirm password
    if password != confirm_password:
        raise HTTPException(
            status_code=400, detail="Password and Confirm password not matched"
        )
    return password
