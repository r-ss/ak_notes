from fastapi import FastAPI
from fastapi.testclient import TestClient

import mongoengine as mongoengine

from config import Config

from views.info import router as info_router
from views.categories import router as categories_router
from views.files import router as files_router
from views.users_auth import router as users_auth_router
from views.users_crud import router as users_crud_router
from views.notes import router as notes_router

routers = [
    info_router,
    categories_router,
    files_router,
    users_auth_router,
    users_crud_router,
    notes_router
]

# Connecting to DB
mg = mongoengine.connect(host=Config.DBHOST)

app = FastAPI()

testclient = TestClient(app)


# handle root url just in case
@app.get('/')
def read_root():
    return {'message': 'there is no root url'}


# including routes from our views
for r in routers:
    app.include_router(r)
