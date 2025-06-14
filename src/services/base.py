from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models.base import Base
from repositories.base import BaseRepository

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Generic base service providing common CRUD operations.
    """

    def __init__(self, repository: BaseRepository):
        self.repository = repository

    def get(self, id: Any) -> Optional[ModelType]:
        """
        Retrieve a single object by its ID.
        """
        return self.repository.get(id=id)

    def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Retrieve multiple objects with optional pagination.
        """
        return self.repository.get_multi(skip=skip, limit=limit)

    def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new object in the database.
        """
        return self.repository.create(obj_in=obj_in)

    def update(
        self,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Update an existing object with new data.
        """
        return self.repository.update(db_obj=db_obj, obj_in=obj_in)

    def remove(self, *, id: int) -> ModelType:
        """
        Remove an object from the database by its ID.
        """
        return self.repository.remove(id=id)
