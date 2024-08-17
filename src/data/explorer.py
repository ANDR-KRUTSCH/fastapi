import os

from sqlite3 import IntegrityError

from model.explorer import Explorer
from errors import Missing, Duplicate

if os.environ.get('CRYPTID_UNIT_TEST'): from .init import test_db_manager as db_manager
else: from .init import db_manager


db_manager.cursor.execute('CREATE TABLE IF NOT EXISTS explorer (name text PRIMARY KEY, country text, description text)')

def row_to_model(row: tuple) -> Explorer | None:
    if not row: return None
    name, country, description = row
    return Explorer(name=name, country=country, description=description)

def get_one(name: str) -> Explorer | None:
    db_manager.cursor.execute('SELECT * FROM explorer WHERE name=:name', dict(name=name))
    if (row := db_manager.cursor.fetchone()): return row_to_model(row=row)
    else: raise Missing(msg=f'Explorer {name} not found')

def get_all() -> list[Explorer] | list:
    db_manager.cursor.execute('SELECT * FROM explorer')
    return [row_to_model(row=row) for row in db_manager.cursor.fetchall()]

def create(explorer: Explorer) -> Explorer:
    try:
        db_manager.cursor.execute('INSERT INTO explorer VALUES (:name, :country, :description)', dict(explorer))
        db_manager.cursor.connection.commit()
        return get_one(name=explorer.name)
    except IntegrityError:
        raise Duplicate(msg=f'Explorer {explorer.name} already exists')

def modify(name: str, explorer: Explorer) -> Explorer | None:
    params = dict(explorer)
    params.update(dict(original_name=name))
    db_manager.cursor.execute('UPDATE explorer SET name=:name, country=:country, description=:description WHERE name=:original_name', params)
    db_manager.cursor.connection.commit()
    if db_manager.cursor.rowcount == 1: return get_one(name=explorer.name)
    else: raise Missing(msg=f'Explorer {name} not found')

def delete(name: str) -> True:
    db_manager.cursor.execute('DELETE FROM explorer WHERE name=:name', dict(name=name))
    db_manager.cursor.connection.commit()
    if db_manager.cursor.rowcount == 1: return True
    else: raise Missing(msg=f'Explorer {name} not found')