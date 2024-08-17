import os

from sqlite3 import IntegrityError

from model.creature import Creature
from errors import Missing, Duplicate

if os.environ.get('CRYPTID_UNIT_TEST'): from .init import test_db_manager as db_manager
else: from .init import db_manager


db_manager.cursor.execute('CREATE TABLE IF NOT EXISTS creature (name text PRIMARY KEY, country text, area text, description text, aka text)')

def row_to_model(row: tuple) -> Creature | None:
    if not row: return None
    name, country, area, description, aka = row
    return Creature(name=name, country=country, area=area, description=description, aka=aka)

def get_one(name: str) -> Creature | None:
    db_manager.cursor.execute('SELECT * FROM creature WHERE name=:name', dict(name=name))
    if (row := db_manager.cursor.fetchone()): return row_to_model(row=row)
    else: raise Missing(msg=f'Creature {name} not found')

def get_all() -> list[Creature] | list:
    db_manager.cursor.execute('SELECT * FROM creature')
    return [row_to_model(row=row) for row in db_manager.cursor.fetchall()]

def create(creature: Creature) -> Creature:
    try:
        db_manager.cursor.execute('INSERT INTO creature VALUES (:name, :country, :area, :description, :aka)', dict(creature))
        db_manager.cursor.connection.commit()
        return get_one(name=creature.name)
    except IntegrityError:
        raise Duplicate(msg=f'Creature {creature.name} already exists')

def modify(name: str, creature: Creature) -> Creature:
    params = dict(creature)
    params.update(dict(original_name=name))
    db_manager.cursor.execute('UPDATE creature SET name=:name, country=:country, area=:area, description=:description, aka=:aka WHERE name=:original_name', params)
    db_manager.cursor.connection.commit()
    if db_manager.cursor.rowcount == 1: return get_one(name=creature.name)
    else: raise Missing(msg=f'Creature {name} not found')

def delete(name: str) -> True:
    db_manager.cursor.execute('DELETE FROM creature WHERE name=:name', dict(name=name))
    db_manager.cursor.connection.commit()
    if db_manager.cursor.rowcount == 1: return True
    else: raise Missing(msg=f'Creature {name} not found')