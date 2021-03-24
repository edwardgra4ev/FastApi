from sqlalchemy.orm import Session
import hashlib
import uuid
from schemas import schemas
from Databese import models


def get_user_by_login(db: Session, login: str):
    """Получение пользователя по логину"""
    return db.query(models.User).filter(models.User.login == login).first()


def search_user_key(db: Session, key: uuid):
    """Поиск ключа пользователя"""
    return db.query(models.UserKey).filter(models.UserKey.key == key).first()


def create_user(db: Session, user: schemas.User):
    """Создание пользоватя"""
    salt = uuid.uuid4().hex
    password = hashlib.sha256(salt.encode() + user.password.encode()).hexdigest() + ':' + salt
    db_user = models.User(login=user.login, hashed_password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_key(db: Session, key: uuid):
    """Удаление ключа пользователя"""
    key_row = db.query(models.UserKey).filter(models.UserKey.key == key).first()
    db.delete(key_row)
    db.commit()
    return key_row


def create_user_key(db: Session, user_id: int):
    """Создание ключа пользователя"""
    db_key = models.UserKey(owner_id=user_id)
    db.add(db_key)
    db.commit()
    db.refresh(db_key)
    return db_key


def get_user_all_key(db: Session, user_id: int):
    """Получить все ключи пользователя"""
    return db.query(models.UserKey).filter(models.UserKey.owner_id == user_id).all()

def update_username_or_password(db: Session, user: schemas.ChangeUserData):
    new_data = user.new_user_data
    new_login, new_password = new_data[0].new_login, new_data[0].new_password

    if new_password is not None:
        salt = uuid.uuid4().hex
        new_password = hashlib.sha256(salt.encode() + new_password.encode()).hexdigest() + ':' + salt
        db.query(models.User).filter(models.User.login == user.login).update({'hashed_password': new_password})
        db.commit()
    if new_login is not None:
        db.query(models.User).filter(models.User.login == user.login).update({'login': new_login})
        db.commit()
        return new_login
    return user.login