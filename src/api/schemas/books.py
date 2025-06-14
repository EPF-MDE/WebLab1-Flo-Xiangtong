from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ----- Category Schemas -----

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Category name")
    description: Optional[str] = Field(None, max_length=200, description="Category description")

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="Category name")

class CategoryInDBBase(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Category(CategoryInDBBase):
    pass


# ----- Book Schemas -----

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Book title")
    author: str = Field(..., min_length=1, max_length=100, description="Book author")
    isbn: str = Field(..., min_length=10, max_length=13, description="Book ISBN")
    publication_year: int = Field(..., ge=1000, le=datetime.now().year, description="Publication year")
    description: Optional[str] = Field(None, max_length=1000, description="Book description")
    quantity: int = Field(..., ge=0, description="Available quantity")
    publisher: Optional[str] = Field(None, max_length=100, description="Publisher")
    language: Optional[str] = Field(None, max_length=50, description="Language")
    pages: Optional[int] = Field(None, gt=0, description="Number of pages")

class BookCreate(BookBase):
    category_ids: Optional[List[int]] = Field(default_factory=list, description="List of category IDs")

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="Book title")
    author: Optional[str] = Field(None, min_length=1, max_length=100, description="Book author")
    isbn: Optional[str] = Field(None, min_length=10, max_length=13, description="Book ISBN")
    publication_year: Optional[int] = Field(None, ge=1000, le=datetime.now().year, description="Publication year")
    description: Optional[str] = Field(None, max_length=1000, description="Book description")
    quantity: Optional[int] = Field(None, ge=0, description="Available quantity")
    publisher: Optional[str] = Field(None, max_length=100, description="Publisher")
    language: Optional[str] = Field(None, max_length=50, description="Language")
    pages: Optional[int] = Field(None, gt=0, description="Number of pages")
    category_ids: Optional[List[int]] = Field(default_factory=list, description="List of category IDs")

class BookInDBBase(BookBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Book(BookInDBBase):
    categories: List[Category] = []

