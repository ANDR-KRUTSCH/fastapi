from .init import cursor, IntegrityError
from model.creature import Creature
from errors import Missing, Duplicate


cursor.execute('CREATE TABLE IF NOT EXISTS creature (name text PRIMARY KEY, country text, area text, description text, aka text)')

def row_to_model(row: tuple) -> Creature | None:
    if not row: return None
    
    name, country, area, description, aka = row
    return Creature(name=name, country=country, area=area, description=description, aka=aka)

def model_to_dict(creature: Creature) -> dict:
    return dict(creature)

def get_one(name: str) -> Creature | None:
    query = 'SELECT * FROM creature WHERE name=:name'
    params = {'name': name}
    cursor.execute(query, params)
    row = cursor.fetchone()
    if row: return row_to_model(row=row)
    else: raise Missing(msg=f'Creature {name} not found')

def get_all() -> list[Creature] | list:
    query = 'SELECT * FROM creature'
    cursor.execute(query)
    rows = cursor.fetchall()
    return [row_to_model(row=row) for row in rows]

def create(creature: Creature) -> Creature:
    query = 'INSERT INTO creature VALUES (:name, :country, :area, :description, :aka)'
    params = model_to_dict(creature=creature)
    try:
        cursor.execute(query, params)
    except IntegrityError:
        raise Duplicate(msg=f'Creature {creature.name} already exists')
    return get_one(name=creature.name)

def modify(name: str, creature: Creature) -> Creature | None:
    if not (name and creature): return None
    query = 'UPDATE creature SET name=:name, country=:country, area=:area, description=:description, aka=:aka WHERE name=:original_name'
    params = model_to_dict(creature=creature)
    params['original_name'] = name
    cursor.execute(query, params)
    if cursor.rowcount == 1: return get_one(name=creature.name)
    else: raise Missing(msg=f'Creature {name} not found')

def delete(name: str) -> bool:
    if not name: return False
    query = 'DELETE FROM creature WHERE name=:name'
    params = {'name': name}
    cursor.execute(query, params)
    if cursor.rowcount == 1: return True
    else: raise Missing(msg=f'Creature {name} not found')