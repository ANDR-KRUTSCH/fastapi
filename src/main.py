from fastapi import FastAPI

from web import explorer, creature, user


app = FastAPI()

app.include_router(router=explorer.router)
app.include_router(router=creature.router)
app.include_router(router=user.router)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='main:app', reload=True)