import data.explorer as data
from model.explorer import Explorer


def get_all() -> list[Explorer] | list:
    return data.get_all()

def get_one(name: str) -> Explorer | None:
    return data.get_one(name=name)

def create(explorer: Explorer) -> Explorer:
    return data.create(explorer=explorer)

def modify(name: str, explorer: Explorer) -> Explorer | None:
    return data.modify(name=name, explorer=explorer)

def delete(name: str) -> bool:
    return data.delete(name=name)