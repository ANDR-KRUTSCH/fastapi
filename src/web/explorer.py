import os

from fastapi import APIRouter, Body, HTTPException

from model.explorer import Explorer
from errors import Missing, Duplicate

if os.environ.get('CRYPTID_UNIT_TEST'): from fake import explorer as service
else: from service import explorer as service


router = APIRouter(prefix='/explorer')

@router.get(path='/')
def get_all() -> list[Explorer] | list:
    return service.get_all()

@router.get(path='/{name}')
def get_one(name: str) -> Explorer | None:
    try:
        return service.get_one(name=name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.post(path='/', status_code=201)
def create(explorer: Explorer = Body()) -> Explorer:
    try:
        return service.create(explorer=explorer)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.patch(path='/{name}')
def modify(name: str, explorer: Explorer = Body()) -> Explorer | None:
    try:
        return service.modify(name=name, explorer=explorer)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.delete(path='/{name}')
def delete(name: str) -> bool:
    try:
        return service.delete(name=name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)