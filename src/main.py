from fastapi import FastAPI
from fastapi.testclient import TestClient

import mongoengine as mongoengine

from config import Config
from info import Info

from views.tags import router as tags_router
from views.files import router as files_router
from views.users import router as users_router
routers = [
    tags_router,
    files_router,
    users_router
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

@app.get('/info')
def info():
    return Info().get()
##############################


# including routes from our views
for r in routers:
    app.include_router(r)