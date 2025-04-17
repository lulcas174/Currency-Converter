from sqlalchemy import Column, Integer, String, Boolean, UUID, ForeignKey, Float, DateTime
from src.infrastructure.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(), primary_key=True, index=True, default=uuid.uuid4)
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