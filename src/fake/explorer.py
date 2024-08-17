from model.explorer import Explorer
from errors import Missing, Duplicate


_explorers = [
    Explorer(name='Resident Evil', country='US', description='Resident Evil'),
    Explorer(name='Silent Hill', country='US', description='Silent Hill'),
]

def get_all() -> list[Explorer]:
    return _explorers

def get_one(name: str) -> Explorer | None:
    for _explorer in _explorers:
        if _explorer.name == name: return _explorer
    raise Missing(msg=f'Explorer {name} not found')

def create(explorer: Explorer) -> Explorer:
    explorers = [_explorer.name for _explorer in _explorers]
    if explorer.name not in explorers:
        _explorers.append(explorer)
        return explorer
    else: raise Duplicate(msg=f'Explorer {explorer.name} already exists')

def modify(name: str, explorer: Explorer) -> Explorer:
    for _explorer in _explorers:
        if _explorer.name == name:
            _explorer.name = explorer.name
            _explorer.country = explorer.country
            _explorer.description = explorer.description
            return _explorer
    raise Missing(msg='Explorer {explorer.name} already exists')

def delete(name: str) -> True:
    for _explorer in _explorers:
        if _explorer.name == name:
            del _explorer
            return True
    raise Missing(msg=f'Explorer {name} not found')