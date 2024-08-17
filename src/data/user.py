from sqlite3 import Cursor, IntegrityError

from model.user import User
from errors import Missing, Duplicate

from .init import get_or_create_db


cursor: Cursor = get_or_create_db()[0]

cursor.execute('CREATE TABLE IF NOT EXISTS user (name text PRIMARY KEY, hash text)')
cursor.execute('CREATE TABLE IF NOT EXISTS xuser (name text PRIMARY KEY, hash text)')

def row_to_model(row: tuple) -> User | None:
    if not row: return None
    name, hash = row
    return User(name=name, hash=hash)

def get_one(name: str) -> User | None:
    cursor.execute('SELECT * FROM user WHERE name=:name', dict(name=name))
    if (row := cursor.fetchone()): return row_to_model(row=row)
    else: raise Missing(msg=f'User {name} not found')

def get_all() -> list[User] | list:
    cursor.execute('SELECT * FROM user')
    return [row_to_model(row=row) for row in cursor.fetchall()]

def create(user: User, table: str = 'user') -> User:
    try:
        cursor.execute(f'INSERT INTO {table} VALUES (:name, :hash)', dict(user))
        cursor.connection.commit()
        if table == 'user': return get_one(name=user.name)
    except IntegrityError:
        raise Duplicate(msg=f'{table}: User {user.name} already exists')
    
def modify(name: str, user: User) -> User:
    try:
        params = dict(user)
        params['original_name'] = name
        cursor.execute('UPDATE user SET name=:name, hash=:hash WHERE name=:original_name', params)
        cursor.connection.commit()
        return get_one(name=user.name)
    except IntegrityError:
        raise Missing(msg=f'User {name} not found')

def delete(name: str) -> True:
    user = get_one(name=name)
    cursor.execute('DELETE FROM user WHERE name=:name', dict(name=name))
    cursor.connection.commit()
    if cursor.rowcount == 1: 
        user = create(user=user, table='xuser')
        return True
    else: raise Missing(msg=f'User {name} not found')