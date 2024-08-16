import data.creature as data
from model.creature import Creature


def get_all() -> list[Creature] | list:
    return data.get_all()

def get_one(name: str) -> Creature | None:
    return data.get_one(name=name)

def create(creature: Creature) -> Creature:
    return data.create(creature=creature)

def modify(name: str, creature: Creature) -> Creature | None:
    return data.modify(name=name, creature=creature)

def delete(name: str) -> bool:
    return data.delete(name=name)