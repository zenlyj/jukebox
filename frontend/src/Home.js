import React, { useEffect, useState } from 'react'
import SpotifyPlayer from 'react-spotify-web-playback';
import { Button, Grid } from '@mui/material';
import AppHeader from './AppHeader';
import Jukebox from './Jukebox'
import Playlist from './Playlist'

function Home(props) {
    const [playlistURI, setPlaylistURI] = useState([])
    const [isPlaying, setIsPlaying] = useState(false)
    const [val, setVal] = useState(0)

    useEffect(() => {
        const windowURL = window.location.search
        const params = new URLSearchParams(windowURL)
        const authCode = params.get('code')
        const accessToken = sessionStorage.getItem('access_token')
        if (accessToken !== null) {
            accessTokenExpiryCheck(accessToken)
        }
        if (accessToken === null && authCode !== null) {
            Promise.resolve(fetch('http://localhost:8000/spotify/authorize?authorization_code='+authCode))
            .then(value => Promise.resolve(value.json())
                .then(value => {
                    const access_token = value.access_token
                    const refresh_token = value.refresh_token
                    sessionStorage.setItem('access_token', access_token)
                    sessionStorage.setItem('refresh_token', refresh_token)
                    console.log(access_token)
                    console.log(refresh_token)
                })
            )            
        }             
    })

    const accessTokenExpiryCheck = (accessToken) => {
        fetch('http://localhost:8000/spotify/search?' + new URLSearchParams({
            query: 'test',
            query_type: 'track',
            access_token: accessToken
        }))
        .then(response => {
            if (response.status === 200) return
            response.json().then(response => {
                console.log(response)
                if (response.detail === 'The access token expired') {
                    refreshAccessToken(accessToken)
                }
            })
        })
    }
    
    const refreshAccessToken = (accessToken) => {
        const refreshToken = sessionStorage.getItem('refresh_token')
        const url = 'http://localhost:8000/spotify/authorize/refresh/?' + new URLSearchParams({
            refresh_token: refreshToken
        })
        
        fetch(url).then(response => {
            if (response.status !== 200) {
                console.log('Unable to refresh access token')
                return
            }
            response.json().then(response => {
                sessionStorage.setItem('access_token', response.access_token)
                console.log('Access Token refreshed')
            })
        })
    }

    const updateDatabaseOnTokenRefresh = (oldAccessToken, newAccessToken) => {
        const url = 'http://localhost:8000/playlist/'
    }

    const forceRender = () => {
        setVal(val+1)
    }

    const updatePlaylistURI = (uris) => {
        setPlaylistURI(uris)
    }
    
    return (
        <Grid container spacing={3} sx={{bgcolor: '#141414ff'}}>
            <Grid item xs={12} sx={{height: '8vh'}}>
                <AppHeader />
            </Grid>
            <Grid item xs={6} sx={{height: '84.5vh'}}>
                <Jukebox forceRender={forceRender}/>
            </Grid>
            <Grid item xs={6} sx={{height: '84.5vh'}}>
                <Playlist playSongs={setIsPlaying} updatePlaylistURI={updatePlaylistURI} forceRender={forceRender} />
            </Grid>
            <Grid item xs={12} sx={{height: '10vh'}}>
                {   sessionStorage.getItem('access_token') !== null  && isPlaying?
                        <SpotifyPlayer 
                            token={sessionStorage.getItem('access_token')}
                            uris={playlistURI}
                        />
                    : <div> </div>
                }
            </Grid>
      </Grid>
    )
}

export default Home