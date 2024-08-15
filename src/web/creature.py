from fastapi import APIRouter

import fake.creature as service
from model.creature import Creature


router = APIRouter(prefix='/creature')


@router.get(path='/')
def get_all() -> list[Creature]:
    return service.get_all()

@router.get(path='/{name}')
def get_one(name: str) -> Creature | None:
    return service.get_one(name=name)

@router.post(path='/')
def create(creature: Creature) -> Creature:
    return service.create(creature=creature)

@router.patch(path='/')
def modify(creature: Creature) -> Creature:
    return service.modify(creature=creature)

@router.put(path='/')
def replace(creature: Creature) -> Creature:
    return service.replace(creature=creature)

@router.delete(path='/{name}')
def delete(name: str) -> bool:
    return service.delete(name=name)