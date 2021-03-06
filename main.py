from fastapi import FastAPI
from os import path
import sys

if not path.exists('.env'):
    sys.exit("The app will not work properly w/o .env file.")

from app.routes import users, auth, events
from app.database.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(events.router)
app.include_router(auth.router)
