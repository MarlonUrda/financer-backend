from fastapi import FastAPI
from app.api import user, auth, transaction
from contextlib import asynccontextmanager
from app.db import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/auth")
app.include_router(user.router, prefix="/user")
app.include_router(transaction.router, prefix="/transaction")


@app.get("/")
def read_root():
    return {"message": "Hello World"}
