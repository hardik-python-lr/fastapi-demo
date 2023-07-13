from passlib.context import CryptContext

# Create a CryptContext object with bcrypt as the hashing scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """Verify if a plain password matches a hashed password.

    Args:
        plain_password (str): Plain password to verify.
        hashed_password (str): Hashed password to compare against.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """
    # Verify if the plain password matches the hashed password
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Encode a password into a hashed format.

    Args:
        password (str): Password to hash.

    Returns:
        str: Hashed password.
    """
    # Hash the password using the CryptContext object
    return pwd_context.hash(password)
