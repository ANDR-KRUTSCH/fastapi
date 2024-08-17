from model.creature import Creature
from errors import Missing, Duplicate


_creatures = [
    Creature(name='Resident Evil', country='US', area='Raccoon City', description='Resident Evil', aka='RE'),
    Creature(name='Silent Hill', country='US', area='Silent Hill', description='Silent Hill', aka='SH'),
]

def get_all() -> list[Creature]:
    return _creatures

def get_one(name: str) -> Creature | None:
    for _creature in _creatures:
        if _creature.name == name: return _creature
    raise Missing(msg=f'Creature {name} not found')

def create(creature: Creature) -> Creature:
    creatures = [_creature.name for _creature in _creatures]
    if creature.name not in creatures:
        _creatures.append(creature)
        return creature
    else: raise Duplicate(msg=f'Creature {creature.name} already exists')

def modify(name: str, creature: Creature) -> Creature:
    for _creature in _creatures:
        if _creature.name == name:
            _creature.name = creature.name
            _creature.country = creature.country
            _creature.area = creature.area
            _creature.description = creature.description
            _creature.aka = creature.aka
            return _creature
    raise Missing(msg=f'Creature {name} not found')

def delete(name: str) -> bool:
    for _creature in _creatures:
        if _creature.name == name:
            del _creature
            return True
    raise Missing(msg=f'Creature {name} not found')