import fake.creature as data
from model.creature import Creature


def get_all() -> list[Creature]:
    return data.get_all()

def get_one(name: str) -> Creature | None:
    return data.get_one(name=name)

def create(creature: Creature) -> Creature:
    return data.create(creature=creature)

def replace(id, creature: Creature) -> Creature:
    return data.replace(id, creature=creature)

def modify(id, creature: Creature) -> Creature:
    return data.modify(id, creature=creature)

def delete(id, creature: Creature) -> bool:
    return data.delete(id)