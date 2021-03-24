from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel
import datetime


class UserKey(BaseModel):
    key: UUID


class UserKeyDatetimeCreation(UserKey):
    datetime_creation: Optional[datetime.datetime]


class DeleteKey(BaseModel):
    login: str
    key: UUID


class DeleteKeyResult(BaseModel):
    key: UUID
    description: str


class UserCreateResponse(BaseModel):
    login: str
    description: Optional[str]


class UserLogin(BaseModel):
    login: str


class UserPassword(UserLogin):
    password: str


class UserAllKey(BaseModel):
    login: str
    list_key: List[UserKey]


class User(UserPassword):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class ChangeUserDataresponse(BaseModel):
    new_login: str
    description: Optional[str]


class NewUserData(BaseModel):
    new_login: Optional[str]
    new_password: Optional[str]


class ChangeUserData(BaseModel):
    login: str
    password: str
    new_user_data: List[NewUserData]

