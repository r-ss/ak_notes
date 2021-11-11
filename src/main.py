from fastapi import FastAPI
from fastapi.testclient import TestClient

import mongoengine as mongoengine

from config import Config
from info import Info

from user_auth import router as auth_router
from views.tags import router as tags_router
from views.categories import router as categories_router
from views.files import router as files_router
from views.users import router as users_router
from views.notes import router as notes_router

routers = [
    auth_router,
    tags_router,
    categories_router,
    files_router,
    users_router,
    notes_router
]

# Connecting to DB
mg = mongoengine.connect(host=Config.DBHOST)

app = FastAPI()
testclient = TestClient(app)


##############################
# just two default routes here
@app.get('/')
def read_root():
    return {'message':'there is no root url'}

@app.get('/info', summary='Returns basic env and system information')
def info():
    return Info().get()
##############################


# including routes from our views
for r in routers:
    app.include_router(r)