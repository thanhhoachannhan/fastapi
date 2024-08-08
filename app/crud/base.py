from typing import List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.log import get_logger


ORMModel = TypeVar('ORMModel')
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)
OwnerIDType = int

log = get_logger(__name__)


class CRUDRepository:
    def __init__(self, model: Type[ORMModel]) -> None:
        self._model = model
        self._name = model.__name__

    def get_one(self, db: Session, *args, **kwargs) -> Optional[ORMModel]:
        log.debug(
            'retrieving one record for %s',
            self._model.__name__,
        )
        return db.query(self._model).filter(*args).filter_by(**kwargs).first()

    def get_many(
        self, db: Session, *args, skip: int = 0, limit: int = 100, **kwargs
    ) -> List[ORMModel]:
        log.debug(
            'retrieving many records for %s with pagination skip %s and limit %s',
            self._model.__name__,
            skip,
            limit,
        )
        return (
            db.query(self._model)
            .filter(*args)
            .filter_by(**kwargs)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, obj_create: CreateSchemaType) -> ORMModel:
        log.debug(
            'creating record for %s with data %s',
            str(self._model.__name__),
            obj_create.model_dump(),
        )
        obj_create_data = obj_create.model_dump(exclude_none=True, exclude_unset=True)
        db_obj = self._model(**obj_create_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        db_obj: ORMModel,
        obj_update: UpdateSchemaType,
    ) -> ORMModel:
        log.debug(
            'updating record for %s with data %s',
            self._model.__name__,
            obj_update.model_dump(),
        )
        obj_update_data = obj_update.model_dump(
            exclude_unset=True
        )  # exclude_unset=True -
        # do not update fields with None
        for field, value in obj_update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: ORMModel) -> ORMModel:
        log.debug('deleting record for %s with id %s', self._model.__name__, db_obj.id)
        db.delete(db_obj)
        db.commit()
        return db_obj

    def create_with_owner(
        self, db: Session, obj_create: CreateSchemaType, owner_id: OwnerIDType
    ) -> ORMModel:
        log.debug(
            'creating record for %s with data %s',
            self._model.__name__,
            obj_create.model_dump(),
        )
        obj_create_data = obj_create.model_dump(
            exclude_none=True, exclude_unset=True, exclude_defaults=True
        )
        db_obj = self._model(**obj_create_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_many_for_owner(
        self,
        db: Session,
        *args,
        owner_id: OwnerIDType,
        skip: int = 0,
        limit: int = 100,
        **kwargs
    ) -> List[ORMModel]:
        return self.get_many(
            db, *args, skip=skip, limit=limit, owner_id=owner_id, **kwargs
        )
