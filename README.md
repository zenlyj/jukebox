# Motivation

As an avid fan of hip-hop music, I find myself browsing [r/hiphopheads](https://www.reddit.com/r/hiphopheads/) frequently to discover newly released tracks and albums to listen to. However, the process of sifting through a sea of posts to find related content can be tiresome, not to mention the added step of searching up tracks on Spotify to play them. Hence, jukebox was developed to automate this mundane process, allowing us to save time and streamline our music discovery-listening.

# Tools and Technologies

1. FastAPI
2. ReactJS
3. SQLite
4. [PRAW](https://praw.readthedocs.io/en/stable/)
5. [Spotify-API](https://developer.spotify.com/documentation/web-api/)


# Features

## Spotify Integration

![spotify_login](https://raw.githubusercontent.com/zenlyj/hip-hop-jukebox/main/README_images/spotify_login.PNG)

The application integrates with Spotify, allowing users to play recommended tracks through the browser. Upon application launch, users will be greeted with a Spotify login page, prompting for user authentication. A premium Spotify account will be required in order to use Spotify API. The application handles refresh of API access tokens, therefore, users do not need to authenticate themselves frequently.

## Music Recommendation

![song_recommendation](https://raw.githubusercontent.com/zenlyj/hip-hop-jukebox/main/README_images/song_recommendation.PNG)

Upon authentication with Spotify, the user will be redirected to the home page of Hip Hop Jukebox. On the left of the page is a list of music tracks pulled from r/hiphopheads.

## Music Playback

![song_playlist](https://raw.githubusercontent.com/zenlyj/hip-hop-jukebox/main/README_images/song_playlist.PNG)

After identifying music tracks of interest, users can place them in a playlist by clicking on the items on the recommendation list. After which, users are able to play songs in the playlist by clicking on the header of the playlist.

![song_player](https://raw.githubusercontent.com/zenlyj/hip-hop-jukebox/main/README_images/song_player.PNG)
A player component will be shown, allowing users to control the music playback.
