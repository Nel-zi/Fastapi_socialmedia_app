from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# This is the logic to hash the users password at the point of account creation
def hash(password: str):
    return pwd_context.hash(password)


# This function is part of the logic for verifying that the password the user entered is the same with the password stored in the database for that user
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)