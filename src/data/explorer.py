from sqlite3 import Cursor, IntegrityError

from .init import get_or_create_db

from model.explorer import Explorer
from errors import Missing, Duplicate


cursor: Cursor = get_or_create_db()[0]

cursor.execute('CREATE TABLE IF NOT EXISTS explorer (name text PRIMARY KEY, country text, description text)')

def row_to_model(row: tuple) -> Explorer | None:
    if not row: return None
    name, country, description = row
    return Explorer(name=name, country=country, description=description)

def get_one(name: str) -> Explorer | None:
    cursor.execute('SELECT * FROM explorer WHERE name=:name', dict(name=name))
    if (row := cursor.fetchone()): return row_to_model(row=row)
    else: raise Missing(msg=f'Explorer {name} not found')

def get_all() -> list[Explorer] | list:
    cursor.execute('SELECT * FROM explorer')
    return [row_to_model(row=row) for row in cursor.fetchall()]

def create(explorer: Explorer) -> Explorer:
    try:
        cursor.execute('INSERT INTO explorer VALUES (:name, :country, :description)', dict(explorer))
        cursor.connection.commit()
        return get_one(name=explorer.name)
    except IntegrityError:
        raise Duplicate(msg=f'Explorer {explorer.name} already exists')

def modify(name: str, explorer: Explorer) -> Explorer | None:
    try:
        params = dict(explorer)
        params.update(dict(original_name=name))
        cursor.execute('UPDATE explorer SET name=:name, country=:country, description=:description WHERE name=:original_name', params)
        cursor.connection.commit()
        return get_one(name=explorer.name)
    except IntegrityError:
        raise Missing(msg=f'Explorer {name} not found')

def delete(name: str) -> True:
    cursor.execute('DELETE FROM explorer WHERE name=:name', dict(name=name))
    cursor.connection.commit()
    if cursor.rowcount == 1: return True
    else: raise Missing(msg=f'Explorer {name} not found')