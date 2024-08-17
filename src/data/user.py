import os

from sqlite3 import IntegrityError

from model.user import User
from errors import Missing, Duplicate

if os.environ.get('CRYPTID_UNIT_TEST'): from .init import test_db_manager as db_manager
else: from .init import db_manager


db_manager.cursor.execute('CREATE TABLE IF NOT EXISTS user (name text PRIMARY KEY, hash text)')
db_manager.cursor.execute('CREATE TABLE IF NOT EXISTS xuser (name text PRIMARY KEY, hash text)')

def row_to_model(row: tuple) -> User | None:
    if not row: return None
    name, hash = row
    return User(name=name, hash=hash)

def get_one(name: str) -> User | None:
    db_manager.cursor.execute('SELECT * FROM user WHERE name=:name', dict(name=name))
    if (row := db_manager.cursor.fetchone()): return row_to_model(row=row)
    else: raise Missing(msg=f'User {name} not found')

def get_all() -> list[User] | list:
    db_manager.cursor.execute('SELECT * FROM user')
    return [row_to_model(row=row) for row in db_manager.cursor.fetchall()]

def create(user: User, table: str = 'user') -> User:
    try:
        db_manager.cursor.execute(f'INSERT INTO {table} VALUES (:name, :hash)', dict(user))
        db_manager.cursor.connection.commit()
        if table == 'user': return get_one(name=user.name)
    except IntegrityError:
        raise Duplicate(msg=f'{table}: User {user.name} already exists')
    
def modify(name: str, user: User) -> User:
    params = dict(user)
    params['original_name'] = name
    db_manager.cursor.execute('UPDATE user SET name=:name, hash=:hash WHERE name=:original_name', params)
    db_manager.cursor.connection.commit()
    if db_manager.cursor.rowcount == 1: return get_one(name=user.name)
    else: raise Missing(msg=f'User {name} not found')

def delete(name: str) -> True:
    user = get_one(name=name)
    db_manager.cursor.execute('DELETE FROM user WHERE name=:name', dict(name=name))
    db_manager.cursor.connection.commit()
    if db_manager.cursor.rowcount == 1: 
        user = create(user=user, table='xuser')
        return True
    else: raise Missing(msg=f'User {name} not found')