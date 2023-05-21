from uuid import UUID
from pydantic import BaseModel, Field


class UserSignup(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class Login(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
#TokenSchema is a Pydantic BaseModel that 
# has two fields: access_token and refresh_token, both of type str. This model is used to represent the 
# JWT tokens that are issued to a client during authentication.

class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None
    
#TokenPayload is a Pydantic model that is used to represent the payload of a
#  JSON Web Token (JWT) 
# used for authentication and authorization in the application.

class UserAuth(BaseModel):
    email: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")


class UserOut(BaseModel):
    id: UUID
    email: str


class SystemUser(UserOut):
    password: str


class UpdatePassword(BaseModel):
    email: str
    old_password: str
    new_password: str


class ForgotPassword(BaseModel):
    email: str


class ResetPassword(BaseModel):
    email: str
    otp: str
    password: str
