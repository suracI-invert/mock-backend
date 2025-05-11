from .auth import router as auth_router
from .lesson import router as lesson_router
from .user import router as user_router
from .exercise import router as exercise_router
from .resources import router as resources_router

__all__ = ["auth_router"]
