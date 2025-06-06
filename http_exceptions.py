from fastapi import HTTPException

from sqlmodel import SQLModel


class AccessDenied(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail="Access denied")


class ObjectWithIdNotFound(HTTPException):
    def __init__(self, id: int, model: type[SQLModel]):
        super().__init__(
            status_code=404, detail=f"{model.__name__} with id {id} not found"
        )
