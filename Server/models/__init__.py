# Server/models/__init__.py
from .user_model import User


# This makes sure SQLModel.metadata knows about all three tables
__all__ = ["User"]