from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from schemas.users import User  # ✅这样才符合依赖方向

from schemas.books import Book



class LoanBase(BaseModel):
    user_id: int = Field(..., description="ID de l'utilisateur")
    book_id: int = Field(..., description="ID du livre")
    loan_date: datetime = Field(default_factory=datetime.utcnow, description="Date d'emprunt")
    return_date: Optional[datetime] = Field(None, description="Date de retour")
    due_date: datetime = Field(..., description="Date d'échéance")
    extended: bool = Field(False, description="Indique si l'emprunt a été prolongé")


class LoanCreate(LoanBase):
    pass


class LoanUpdate(BaseModel):
    return_date: Optional[datetime] = Field(None, description="Date de retour")
    due_date: Optional[datetime] = Field(None, description="Date d'échéance")
    extended: Optional[bool] = Field(None, description="Indique si l'emprunt a été prolongé")


class LoanInDBBase(LoanBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Loan(LoanInDBBase):
    pass


class LoanWithDetails(Loan):
    user: User
    book: Book