import os
from datetime import datetime, timedelta, UTC

from jwt import PyJWTError
from jwt.api_jwt import decode as jwt_decode, encode as jwt_encode
from passlib.context import CryptContext

from model.user import User


if os.environ.get('CRYPTID_UNIT_TEST'): from fake import user as data
else: from data import user as data

SECRET_KEY = 'keep-it-secret-keep-it-safe'
ALGORITHM = 'HS256'
pwd_context = CryptContext(schemes=['sha256_crypt'], deprecated='auto')

def verify_password(plain: str, hash: str) -> bool:
    return pwd_context.verify(secret=plain, hash=hash)

def get_hash(plain: str) -> str:
    return pwd_context.hash(secret=plain)

def get_jwt_username(token: str) -> str | None:
    try:
        payload: dict = jwt_decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        if not (username := payload.get('sub')): return None
    except PyJWTError: return None
    return username

def lookup_user(username: str) -> User | None:
    if (user := get_one(name=username)): return user
    else: return None

def auth_user(name: str, plain: str) -> User | None:
    if not (user := lookup_user(username=name)): return None
    if not verify_password(plain=plain, hash=user.hash): return None
    return user

def create_access_token(data: dict, expires: timedelta | None = None):
    src = data.copy()
    now = datetime.now(tz=UTC)
    if not expires:
        expires = timedelta(minutes=15)
    src.update({'exp': now + expires})
    return jwt_encode(payload=src, key=SECRET_KEY)

def get_all() -> list[User] | list:
    return data.get_all()

def get_one(name: str) -> User:
    return data.get_one(name=name)

def create(user: User) -> User:
    user.hash = get_hash(plain=user.hash)
    return data.create(user=user)

def modify(name: str, user: User) -> User:
    return data.modify(name=name, user=user)

def delete(name: str) -> bool:
    return data.delete(name=name)