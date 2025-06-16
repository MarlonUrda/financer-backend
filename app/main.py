import uvicorn
from fastapi import FastAPI
from api import user, auth, transaction
from db import lifespan
from models import *


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/auth")
app.include_router(user.router, prefix="/user")
app.include_router(transaction.router, prefix="/transaction")


@app.get("/")
def read_root():
    return {"message": "Hello World"}
