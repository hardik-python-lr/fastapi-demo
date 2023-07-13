from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# check password
def verify_password(plain_password, hashed_password):
    """Verifing plain and hashed password

    Args:
        plain_password (str): user plain password, which is user use for create new user
        hashed_password (str): cypher text, which is encoded plain password.

    Returns:
        bool: Return True, if password is correct or Return False if password is wrong.
    """
    return pwd_context.verify(plain_password, hashed_password)


# encode in to hash password
def get_password_hash(password):
    """Convert plain password into hash password.

    Args:
        password (str): User plain password.

    Returns:
        str: Return hashed password.
    """
    return pwd_context.hash(password)
