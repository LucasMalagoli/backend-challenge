# app/crud_router.py

from typing import TypeVar, Type, Optional, Sequence, Union, Generator, List, Callable
from enum import Enum
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

TModel = TypeVar("TModel")
TReadSchema = TypeVar("TReadSchema", bound=BaseModel)
TCreateSchema = TypeVar("TCreateSchema", bound=BaseModel)
TUpdateSchema = TypeVar("TUpdateSchema", bound=BaseModel)
DbGetterType = Callable[[], Union[Session, Generator[Session, None, None]]]


class CRUDRouter:
    def __init__(
        self,
        model: Type[TModel],
        read_schema: Type[TReadSchema],
        create_schema: Type[TCreateSchema],
        update_schema: Type[TUpdateSchema],
        db_getter: DbGetterType,
        prefix: str,
        tags: Optional[Sequence[str | Enum]] = None,
    ):
        self.model = model
        self.read_schema = read_schema
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.db_getter = db_getter
        self.router = APIRouter(prefix=prefix, tags=list(tags) if tags else None)

    def register_routes(self):
        self.router.post("/", response_model=self.read_schema, status_code=status.HTTP_201_CREATED)(self._create())
        self.router.get("/", response_model=List[self.read_schema])(self._read_all())
        self.router.get("/{id}", response_model=self.read_schema)(self._read_one())
        self.router.patch("/{id}", response_model=self.read_schema)(self._update())
        self.router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)(self._delete())

    # -------------------------------
    # Endpoints (wrapped as closures)
    # -------------------------------

    def _create(self):
        def route(item: self.create_schema, db: Session = Depends(self.db_getter)):  # type: ignore
            return self.create(item, db)

        # this changes the "Route" default text in /docs, style choice
        route.__name__ = f"Creates a {self.model.__name__} instance"
        return route

    def _read_all(self):
        def route(skip: int = 0, limit: int = 100, db: Session = Depends(self.db_getter)):
            return self.read_all(skip, limit, db)
        route.__name__ = f"Returns all {self.model.__name__} instances, paginated"
        return route

    def _read_one(self):
        def route(id: int, db: Session = Depends(self.db_getter)):
            return self.read_one(id, db)
        route.__name__ = f"Returns a single {self.model.__name__} instance"
        return route

    def _update(self):
        def route(id: int, item: self.update_schema, db: Session = Depends(self.db_getter)):  # type: ignore
            return self.update(id, item, db)
        route.__name__ = f"Partially/Fully updates a single {self.model.__name__} instance"
        return route

    def _delete(self):
        def route(id: int, db: Session = Depends(self.db_getter)):
            return self.delete(id, db)
        route.__name__ = f"Deletes a single {self.model.__name__} instance"
        return route

    # -------------------------------
    # Default handlers (meant to override)
    # -------------------------------

    def create(self, item: TCreateSchema, db: Session):  # type: ignore
        db_item = self.model(**item.model_dump())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def read_all(self, skip: int, limit: int, db: Session):
        return db.query(self.model).offset(skip).limit(limit).all()

    def read_one(self, id: int, db: Session):
        db_item = db.query(self.model).get(id)
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        return db_item

    def update(self, id: int, item: TUpdateSchema, db: Session):  # type: ignore
        db_item = db.query(self.model).get(id)
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        for key, value in item.model_dump(exclude_unset=True).items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
        return db_item

    def delete(self, id: int, db: Session):
        db_item = db.query(self.model).get(id)
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        db.delete(db_item)
        db.commit()
        return None
