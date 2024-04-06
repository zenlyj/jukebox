from fastapi import FastAPI
from api.database import SessionLocal, engine, Base
from fastapi.middleware.cors import CORSMiddleware
from api.routers import Spotify
from api.routers import Songs
from api.routers import Playlist

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
