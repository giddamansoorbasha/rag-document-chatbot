from pydantic import BaseModel, EmailStr

class UserSignUpRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    name: str
    email: EmailStr

class TokenResponse(BaseModel):
    access_token: str
    token_type: str