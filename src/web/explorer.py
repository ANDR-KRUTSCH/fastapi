from fastapi import APIRouter, Body, HTTPException

import service.explorer as service
from model.explorer import Explorer
from errors import Missing, Duplicate


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

@router.post(path='/')
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