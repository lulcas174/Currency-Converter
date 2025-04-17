from sqlalchemy import Column, Integer, String, Boolean
from src.infrastructure.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(
        String(128),
        name="hashed_password",
        index=True
    )
    is_active = Column(
        Boolean, 
        default=True,
        name="is_active"
    )