from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    email: str = Field(..., example="admin@example.com", description="Email do usuário")
    password: str = Field(..., example="adminpassword", description="Senha de acesso")

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "email": "admin@example.com",
                "password": "adminpassword"
            }]
        }
    }

class UserCreate(BaseModel):
    email: str = Field(..., example="usuario@example.com", description="Email válido")
    password: str = Field(..., example="SenhaF0rte!", min_length=8, description="Senha com mínimo 8 caracteres")

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "email": "novo.usuario@example.com",
                "password": "Str0ngP@ssw0rd"
            }]
        }
    }