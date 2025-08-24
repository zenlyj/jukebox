from fastapi import FastAPI
from api.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from api.routers import Spotify
from api.routers import Songs
from api.routers import Playlist
from api.routers import Preferences
from api.exceptions.handlers import add_exception_handlers

Base.metadata.create_all(bind=engine)

app = FastAPI()

add_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Spotify.router)
app.include_router(Songs.router)
app.include_router(Playlist.router)
app.include_router(Preferences.router)
