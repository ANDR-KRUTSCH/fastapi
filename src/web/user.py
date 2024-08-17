import os
from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from model.user import User
from errors import Missing, Duplicate


if os.environ.get('CRYPTID_UNIT_TEST'): from fake import user as service
else: from service import user as service

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix='/user')

oauth2_dep = OAuth2PasswordBearer(tokenUrl='user/token')

def unauthed():
    raise HTTPException(status_code=401, detail='Incorrect username or password', headers={'WWW-Authenticate': 'Bearer'})

def get_current_user_dep(token: str = Depends(oauth2_dep)) -> User:
    if not (username := service.get_jwt_username(token)):
        raise Missing(msg=f'User {token} not found')
    if not (user := service.lookup_user(username)):
        raise Missing(msg=f'User {token} not found')
    return user

@router.get(path='/token')
def get_current_user(current_user: User = Depends(get_current_user_dep)) -> User:
    return current_user

@router.post(path='/token')
def create_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = service.auth_user(name=form_data.username, plain=form_data.password)
    if not user: unauthed()
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(data={'sub': user.name}, expires=expires)
    return {'access_token': access_token, 'token_type': 'bearer'}

@router.get(path='/')
def get_all() -> list[User] | list:
    return service.get_all()

@router.get(path='/{name}')
def get_one(name: str) -> User:
    try:
        return service.get_one(name=name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.post(path='/', status_code=201)
def create(user: User) -> User:
    try:
        return service.create(user=user)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)

@router.patch(path='/{name}')
def modify(name: str, user: User = Body()) -> User:
    try:
        return service.modify(name=name, user=user)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.delete(path='/{name}')
def delete(name: str) -> bool:
    try:
        return service.delete(name=name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)