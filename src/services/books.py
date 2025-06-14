from typing import List, Optional, Any, Dict, Union
from sqlalchemy.orm import Session

from ..repositories.books import BookRepository
from ..models.books import Book
from ..models.categories import Category
from ..api.schemas.books import BookCreate, BookUpdate
from .base import BaseService


class BookService(BaseService[Book, BookCreate, BookUpdate]):
    """
    Service for managing books.
    """

    def __init__(self, repository: BookRepository):
        super().__init__(repository)
        self.repository = repository

    def get_by_isbn(self, *, isbn: str) -> Optional[Book]:
        """
        Retrieve a book by its ISBN.
        """
        return self.repository.get_by_isbn(isbn=isbn)

    def get_by_title(self, *, title: str) -> List[Book]:
        """
        Retrieve books by partial title match.
        """
        return self.repository.get_by_title(title=title)

    def get_by_author(self, *, author: str) -> List[Book]:
        """
        Retrieve books by partial author match.
        """
        return self.repository.get_by_author(author=author)

    def create(self, *, obj_in: BookCreate) -> Book:
        """
        Create a new book, checking for duplicate ISBN and setting categories.
        """
        existing_book = self.get_by_isbn(isbn=obj_in.isbn)
        if existing_book:
            raise ValueError("ISBN already exists")

        # Convert input to dictionary and extract category IDs
        obj_in_data = obj_in.dict()
        category_ids = obj_in_data.pop("category_ids", [])

        # Create book instance (without committing yet)
        book = Book(**obj_in_data)

        # If category IDs are provided, retrieve them from DB and assign
        if category_ids:
            book.categories = self.repository.db.query(Category).filter(Category.id.in_(category_ids)).all()

        # Save to database
        self.repository.db.add(book)
        self.repository.db.commit()
        self.repository.db.refresh(book)
        return book

    def update(self, *, db_obj: Book, obj_in: Union[BookUpdate, Dict[str, Any]]) -> Book:
        """
        Update book details and associated categories if provided.
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        category_ids = update_data.pop("category_ids", None)

        # Update basic fields
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        # Update categories if explicitly provided
        if category_ids is not None:
            db_obj.categories = self.repository.db.query(Category).filter(Category.id.in_(category_ids)).all()

        self.repository.db.add(db_obj)
        self.repository.db.commit()
        self.repository.db.refresh(db_obj)
        return db_obj

    def update_quantity(self, *, book_id: int, quantity_change: int) -> Book:
        """
        Update the quantity of a book.
        """
        book = self.get(id=book_id)
        if not book:
            raise ValueError(f"Book with ID {book_id} not found")

        new_quantity = book.quantity + quantity_change
        if new_quantity < 0:
            raise ValueError("Quantity cannot be negative")

        return self.update(db_obj=book, obj_in={"quantity": new_quantity})

