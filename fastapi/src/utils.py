from passlib.context import CryptContext
# imports the CryptContext class from the passlib library, which is used to securely hash passwords.
#When you hash a password, you convert it from its original 
# form (a string of characters) into a fixed-length string of bytes, 
# using a mathematical algorithm that cannot be reversed. The resulting hash value is 
# unique to the original password, and any small change to the password will result in a completely different hash value.
from datetime import datetime, timedelta
# library, which are used to work with dates and times.
from typing import Union, Any, Optional
#This line imports some type hints that can be used to 
# improve code readability and maintainability.
#Union is a type that allows a value to be of one of several possible types. For example, Union[int, str] means that a variable can be either an integer or a string.
#Any ,'Optional'

from settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES
#SECRET_KEY is likely a string or byte string used as a secret key for encoding and decoding tokens. This is typically used to verify the authenticity of a 
# token and to prevent it from being tampered with.
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# using the bcrypt algorithm. To verify a password against a previously generated hash
#When set to "auto", the CryptContext object will automatically upgrade any hashes that use a deprecated 
# scheme to a newer scheme when the hash is verified. 
#or example, the MD5 hash algorithm was once widely used for password hashing,
#  but it has since been found to be 
# insecure due to its susceptibility to collision attacks.

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)
#get_hashed_password that takes a string password as input 
# and returns a hashed version of the password as a string.


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)
#verify_password that takes two string arguments: password and hashed_pass.
#  The function returns a boolean value indicating whether the plaintext 
# password matches the hashed version stored in hashed_pass.


def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
 #create_access_token that takes two arguments: subject and expires_delta. 
 # The function returns a string, which is a JSON Web Token (JWT) 
 # that can be used to authenticate and authorize access to protected resources.


    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt
#The above code defines a function called create_refresh_token 
# that takes two arguments: subject and expires_delta. 
# The function returns a string, which is a JSON Web Token (JWT) that can be used to obtain a new access token.

#The subject argument can be either a string 
# or any other value that can be serialized to JSON. 
# It represents the identity of the user for whom the refresh token is being created.