from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sql_app.database import SessionLocal, engine
from fastapi.responses import RedirectResponse
from starlette.requests import Request
import requests
import base64
from fastapi.middleware.cors import CORSMiddleware
from sql_app import crud, models, schemas
from typing import List
import json
from parser import Parser

models.Base.metadata.create_all(bind=engine)
parser = Parser()

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

@app.get("/spotify/authorize/")
def authorize_spotify(authorization_code: str):
    client_id = '3f2c9540f73f41a9961f2e2f86357e18'
    client_secret = '056631f28de642a48fe6e8a30523b4a7'
    client_credentials = (client_id + ':' + client_secret).encode('ascii')
    client_credentials = base64.b64encode(client_credentials)
    headers = {
        'Authorization' : 'Basic ' + client_credentials.decode('utf-8'),
        'Content-Type' : 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type' : 'authorization_code',
        'code' : authorization_code,
        'redirect_uri' : 'http://localhost:3000/home/'
    }
    result = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    if result.status_code != 200:
        errorMessage = json.loads(result.text)['error_description']
        raise HTTPException(status_code=result.status_code, detail=errorMessage)
    
    result = json.loads(result.text)
    access_token = result['access_token']
    refresh_token = result['refresh_token']

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }

@app.get("/spotify/authorize/refresh/")
def reauthorize_spotify(refresh_token: str):
    client_id = '3f2c9540f73f41a9961f2e2f86357e18'
    client_secret = '056631f28de642a48fe6e8a30523b4a7'
    client_credentials = (client_id + ':' + client_secret).encode('ascii')
    client_credentials = base64.b64encode(client_credentials)
    headers = {
        'Authorization' : 'Basic ' + client_credentials.decode('utf-8'),
        'Content-Type' : 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type' : 'refresh_token',
        'refresh_token' : refresh_token
    }
    result = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    if result.status_code != 200:
        errorMessage = json.loads(result.text)['error_description']
        raise HTTPException(status_code=result.status_code, detail=errorMessage)
    
    result = json.loads(result.text)
    access_token = result['access_token']
    
    return {
        'access_token': access_token
    }


@app.get("/spotify/search/")
def search_spotify(query: str, query_type: str, access_token: str):
    print(query)
    url = 'https://api.spotify.com/v1/search'
    params = {
        'q' : query,
        'type' : query_type,
        'limit' : 5
    }
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer ' + access_token
    }
    result = requests.get(url, headers=headers, params=params)
    if result.status_code != 200:
        errorMessage = json.loads(result.text)['error']['message']
        raise HTTPException(status_code=result.status_code, detail=errorMessage)
    uri = parser.parseSpotifySearch(result.text, query)
    if uri == None:
        raise HTTPException(status_code=404, detail='Track not found on Spotify')
    return {
        'uri' : uri
    }


@app.get("/songs/", response_model=List[schemas.Song])
def get_songs(db: Session = Depends(get_db)):
    return crud.get_songs(db)

@app.post("/songs/", response_model=schemas.Song)
def add_songs(song: schemas.SongCreate, db: Session = Depends(get_db)):
    return crud.create_song(db, song)

@app.get("/playlist/", response_model=List[schemas.Song])
def get_playlist_songs(authentication_code: str, db: Session = Depends(get_db)):
    return crud.get_playlist_songs(db, authentication_code)

@app.post("/playlist/", response_model=schemas.Playlist)
def add_song_to_playlist(playlist: schemas.PlaylistCreate, db: Session = Depends(get_db)):
    return crud.add_song_to_playlist(db, playlist)

@app.delete("/playlist/")
def remove_song_from_playlist(authentication_code: str, song_id: int, db: Session = Depends(get_db)):
    numDeleted = crud.remove_song_from_playlist(db, authentication_code, song_id)
    if numDeleted == 0:
        raise HTTPException(status_code=400, detail='Failed to delete song')
    return {
        'detail': 'Delete Successful'
    }

@app.put('/playlist/')
def update_token_code(old_access_token: str, new_access_token: str, db: Session = Depends(get_db)):
    numUpdated = crud.update_access_token_on_refresh(db, old_access_token, new_access_token)
    return {
        'detail': '{x} songs updated'.format(x=numUpdated)
    }