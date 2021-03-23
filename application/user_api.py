from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import Databese.sql_queries as crud
from .shemas import schemas
from api.main_app import application as app
from api.main_app import get_db



@app.post("/users/create/", name='Регистрация пользователя', response_model=schemas.UserCreateResponse)
def create_user(user: schemas.UserPassword,
                db: Session = Depends(get_db)):
    """Метод регистрации нового пользователя"""
    # [20.03.2021 edwardgra4ev]
    # :param user: Pydantic схема их schemas.UserPassword
    # :param db: Новая сессия базы данных
    # :return:
    # 1) В случаи успеха, Pydantic схема из schemas.UserCreateResponse содержащая логин и ответ о регистрации
    # 2) Если такой пользователь есть, возвращаем сообщение "Account registered successfully"
    db_user = crud.get_user_by_login(db, login=user.login)
    if db_user:
        raise HTTPException(status_code=400, detail="Login already registered")
    result = {'login': crud.create_user(db=db, user=user).login,
              'description': 'Account registered successfully'}
    return result


@app.post("/users/createkey/", name='Регистрация ключа', response_model=schemas.UserKeyDatetimeCreation)
def create_key(user: schemas.UserLogin, db: Session = Depends(get_db)):
    """Метод регистрации нового ключа"""
    # [20.03.2021 edwardgra4ev]
    # :param user: Pydantic схема их schemas.UserLogin
    # :param db: Новая сессия базы данных
    # :return:
    # 1) В случаи успеха, Pydantic схема из schemas.UserKey содержащая логин и uid ключ
    # 2) Если такого пользователя нет, возвращаем сообщение "Login not found"
    db_user = crud.get_user_by_login(db, login=user.login)
    if db_user:
        user_key = crud.create_user_key(db=db, user_id=db_user.id)
        return {'key': user_key.key, 'datetime_creation': user_key.datetime_creation}
    else:
        raise HTTPException(status_code=400, detail="Login not found")


@app.post("/users/getallkey/", name='Получение всех ключей пользователя', response_model=schemas.UserAllKey)
def get_all_user_key(user: schemas.UserLogin, db: Session = Depends(get_db)):
    """Метод получения всех ключей по логину"""
    # [20.03.2021 edwardgra4ev]
    # :param user: Pydantic схема их schemas.UserLogin
    # :param db: Новая сессия базы данных
    # :return:
    # 1) В случаи успеха, Pydantic схема из schemas.UserKey содержащая логин и uid ключ
    # 2) Если такого пользователя нет, возвращаем сообщение "Login not found"
    db_user = crud.get_user_by_login(db, login=user.login)
    if db_user:
        all_key = crud.get_user_all_key(db=db, user_id=db_user.id)
        result_list = []
        for data in all_key:
            key, datetime_creation = data.key, data.datetime_creation
            result_list.append({'key': key, 'datetime_creation': datetime_creation})
        return {'login': user.login, 'list_key': result_list}
    else:
        raise HTTPException(status_code=400, detail="Login not found")

@app.post('/users/deletekey/', name='Удалить ключ', response_model=schemas.DeleteKeyResult)
def delete_key(user: schemas.DeleteKey, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_login(db, login=user.login)
    if db_user:
        db_key = crud.search_user_key(db, key=user.key)
        if db_key:
            crud.delete_key(db, key=user.key)

            return {'key': user.key, 'description': 'The key has been successfully deleted'}
        else:
            raise HTTPException(status_code=400, detail="Key not found")
    else:
        raise HTTPException(status_code=400, detail="Login not found")