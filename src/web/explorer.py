from fastapi import APIRouter

import fake.explorer as service
from model.explorer import Explorer


router = APIRouter(prefix='/explorer')


@router.get(path='/')
def get_all() -> list[Explorer]:
    return service.get_all()

@router.get(path='/{name}')
def get_one(name: str) -> Explorer | None:
    return service.get_one(name=name)

@router.post(path='/')
def create(explorer: Explorer) -> Explorer:
    return service.create(explorer=explorer)

@router.patch(path='/')
def modify(explorer: Explorer) -> Explorer:
    return service.modify(explorer=explorer)

@router.put(path='/')
def replace(explorer: Explorer) -> Explorer:
    return service.replace(explorer=explorer)

@router.delete(path='/{name}')
def delete(name: str) -> bool:
    return service.delete(name=name)