import fake.explorer as data
from model.explorer import Explorer


def get_all() -> list[Explorer]:
    return data.get_all()

def get_one(name: str) -> Explorer | None:
    return data.get_one(name=name)

def create(explorer: Explorer) -> Explorer:
    return data.create(explorer=explorer)

def replace(id, explorer: Explorer) -> Explorer:
    return data.replace(id, explorer=explorer)

def modify(id, explorer: Explorer) -> Explorer:
    return data.modify(id, explorer=explorer)

def delete(id, explorer: Explorer) -> bool:
    return data.delete(id)