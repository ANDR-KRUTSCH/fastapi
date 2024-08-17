from sqlite3 import Cursor, IntegrityError

from .init import get_or_create_db

from model.creature import Creature
from errors import Missing, Duplicate


cursor: Cursor = get_or_create_db()[0]

cursor.execute('CREATE TABLE IF NOT EXISTS creature (name text PRIMARY KEY, country text, area text, description text, aka text)')

def row_to_model(row: tuple) -> Creature | None:
    if not row: return None
    name, country, area, description, aka = row
    return Creature(name=name, country=country, area=area, description=description, aka=aka)

def get_one(name: str) -> Creature | None:
    cursor.execute('SELECT * FROM creature WHERE name=:name', dict(name=name))
    if (row := cursor.fetchone()): return row_to_model(row=row)
    else: raise Missing(msg=f'Creature {name} not found')

def get_all() -> list[Creature] | list:
    cursor.execute('SELECT * FROM creature')
    return [row_to_model(row=row) for row in cursor.fetchall()]

def create(creature: Creature) -> Creature:
    try:
        cursor.execute('INSERT INTO creature VALUES (:name, :country, :area, :description, :aka)', dict(creature))
        cursor.connection.commit()
        return get_one(name=creature.name)
    except IntegrityError:
        raise Duplicate(msg=f'Creature {creature.name} already exists')

def modify(name: str, creature: Creature) -> Creature:
    try:
        params = dict(creature)
        params.update(dict(original_name=name))
        cursor.execute('UPDATE creature SET name=:name, country=:country, area=:area, description=:description, aka=:aka WHERE name=:original_name', params)
        cursor.connection.commit()
        return get_one(name=creature.name)
    except IntegrityError:
        raise Missing(msg=f'Creature {name} not found')

def delete(name: str) -> True:
    cursor.execute('DELETE FROM creature WHERE name=:name', dict(name=name))
    cursor.connection.commit()
    if cursor.rowcount == 1: return True
    else: raise Missing(msg=f'Creature {name} not found')