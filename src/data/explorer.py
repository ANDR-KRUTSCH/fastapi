from .init import cursor, IntegrityError
from model.explorer import Explorer
from errors import Missing, Duplicate


cursor.execute('CREATE TABLE IF NOT EXISTS explorer (name text PRIMARY KEY, country text, description text)')

def row_to_model(row: tuple) -> Explorer | None:
    if not row: return None
    
    name, country, description = row
    return Explorer(name=name, country=country, description=description)

def model_to_dict(explorer: Explorer) -> dict:
    return dict(explorer)

def get_one(name: str) -> Explorer | None:
    query = 'SELECT * FROM explorer WHERE name=:name'
    params = {'name': name}
    cursor.execute(query, params)
    row = cursor.fetchone()
    if row: return row_to_model(row=row)
    else: raise Missing(msg=f'Explorer {name} not found')

def get_all() -> list[Explorer] | list:
    query = 'SELECT * FROM explorer'
    cursor.execute(query)
    rows = cursor.fetchall()
    return [row_to_model(row=row) for row in rows]

def create(explorer: Explorer) -> Explorer:
    query = 'INSERT INTO explorer VALUES (:name, :country, :description)'
    params = model_to_dict(explorer=explorer)
    try:
        cursor.execute(query, params)
    except IntegrityError:
        raise Duplicate(msg=f'Explorer {explorer.name} already exists')
    return get_one(name=explorer.name)

def modify(name: str, explorer: Explorer) -> Explorer | None:
    if not (name and explorer): return None
    query = 'UPDATE explorer SET name=:name, country=:country, description=:description WHERE name=:original_name'
    params = model_to_dict(explorer=explorer)
    params['original_name'] = name
    cursor.execute(query, params)
    if cursor.rowcount == 1: return get_one(name=explorer.name)
    else: raise Missing(msg=f'Explorer {name} not found')

def delete(name: str) -> bool:
    if not name: return False
    query = 'DELETE FROM explorer WHERE name=:name'
    params = {'name': name}
    cursor.execute(query, params)
    if cursor.rowcount == 1: return True
    else: raise Missing(msg=f'Explorer {name} not found')