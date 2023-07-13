from fastapi import APIRouter
from src.user.routers import router as user_router
from src.task.routers import router as task_router

# Create an APIRouter instance
api_router = APIRouter()


# Include the user router
api_router.include_router(user_router)

# Include the product router
api_router.include_router(task_router)
