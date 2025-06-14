from fastapi import APIRouter

from api.routes.books import router as books_router
from api.routes.users import router as users_router
from api.routes.loans import router as loans_router
from api.auth import router as auth_router
from api.stats import router as stats_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(books_router, prefix="/books", tags=["books"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(loans_router, prefix="/loans", tags=["loans"])
api_router.include_router(stats_router, prefix="/stats", tags=["stats"])

