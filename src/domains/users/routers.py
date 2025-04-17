from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.infrastructure.security import create_access_token
from src.domains.users.services import UserService
from src.domains.users.schemas import LoginRequest, UserCreate, UserResponse, Token

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    return await UserService.create_user(user_data)

@router.post("/login", response_model=Token)
async def login(credentials: LoginRequest):
    user = await UserService.authenticate_user(credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


