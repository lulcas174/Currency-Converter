from src.infrastructure.security import get_password_hash, verify_password
from src.domains.users.repositories import UserRepository
from src.domains.users.schemas import UserCreate, UserResponse

class UserService:
    @staticmethod
    async def create_user(user_data: UserCreate):
        return await UserRepository.create_user(user_data)

    @staticmethod
    async def authenticate_user(email: str, password: str):
        user = await UserRepository.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user