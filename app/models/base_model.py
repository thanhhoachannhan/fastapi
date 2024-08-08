from typing import Any, Dict

from sqlalchemy import MetaData
from sqlalchemy.orm import as_declarative, declared_attr


class_registry: Dict[str, Any] = {}


@as_declarative(class_registry=class_registry)
class Base:
    id: Any
    __name__: str
    __abstract__: bool = True
    metadata = MetaData()

    @declared_attr
    def __tablename__(self) -> str:
        if '__tablename__' in vars(self):
            return getattr(self, '__tablename__')
        return self.__name__.lower()
