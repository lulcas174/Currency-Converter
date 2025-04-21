from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    is_active: bool = Field(..., description="Whether the user is active")

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    email: str = Field(..., example="novo.usuario@example.com",
                       description="User email")
    password: str = Field(...,
                          example="adminpassword",
                          description="Password to acess")

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "email": "novo.usuario@example.com",
                "password": "SenhaF0rte!"
            }]
        }
    }


class UserCreateRequest(BaseModel):
    email: str = Field(..., example="novo.usuario@example.com",
                       description="Valid email")
    password: str = Field(..., example="SenhaF0rte!", min_length=8,
                          description="password must be at least 8 characters")

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "email": "novo.usuario@example.com",
                "password": "SenhaF0rte!"
            }]
        }
    }
