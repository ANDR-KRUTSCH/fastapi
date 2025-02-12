import os

from fastapi import APIRouter, Body, HTTPException

from model.creature import Creature
from errors import Missing, Duplicate

if os.environ.get('CRYPTID_UNIT_TEST'): from fake import creature as service
else: from service import creature as service


router = APIRouter(prefix='/creature')

@router.get(path='/')
def get_all() -> list[Creature] | list:
    return service.get_all()

@router.get(path='/{name}')
def get_one(name: str) -> Creature | None:
    try:
        return service.get_one(name=name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.post(path='/', status_code=201)
def create(creature: Creature = Body()) -> Creature:
    try:
        return service.create(creature=creature)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.patch(path='/{name}')
def modify(name: str, creature: Creature = Body()) -> Creature | None:
    try:
        return service.modify(name=name, creature=creature)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.delete(path='/{name}')
def delete(name: str) -> bool:
    try:
        return service.delete(name=name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)