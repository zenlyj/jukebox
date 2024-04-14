# About

On popular social news aggregation platform [Reddit](https://www.reddit.com/), there are communities/subreddits dedicated to music discussion, such as [r/hiphopheads](https://www.reddit.com/r/hiphopheads/), [r/electronicmusic](https://www.reddit.com/r/electronicmusic/), [r/indieheads](https://www.reddit.com/r/indieheads/). In these communities, users post about the latest music, videos and news relating to their favorite artists.

jukebox is a web application that extracts user-submitted song recommendations from the abundance of information that is available in these music communities. It supports music playback with Spotify, allowing users to listen to the recommended songs on jukebox, streamlining their music discovery and listening experience.

# Tools and Technologies

1. FastAPI
2. React
3. SQLite
4. [PRAW](https://praw.readthedocs.io/en/stable/)
5. [Spotify-API](https://developer.spotify.com/documentation/web-api/)

# Features

## Spotify Integration

![spotify_login](https://raw.githubusercontent.com/zenlyj/jukebox/main/docs/spotify_login.PNG)

The application integrates with Spotify, allowing users to play recommended tracks through the browser. On application launch, users will be greeted with the Spotify login page, prompting for user authentication.

A premium Spotify account is required in order to use the Spotify API for music playback. The application automatically refreshes access tokens to ensure that users remain authenticated with Spotify over prolonged application usage.

## Discover Mode

![discover_selection](https://raw.githubusercontent.com/zenlyj/jukebox/main/docs/discover_selection.PNG)

Once authenticated, users will be brought to the Discover page, where they have the following music genre options to choose from:

- Hip-Hop, from [r/hiphopheads](https://www.reddit.com/r/hiphopheads/)
- Electronic, from [r/electronicmusic](https://www.reddit.com/r/electronicmusic/)
- Indie, from [r/indieheads](https://www.reddit.com/r/indieheads/)
- General, from every genre listed above

![discover_browse](https://raw.githubusercontent.com/zenlyj/jukebox/main/docs/discover_browse.PNG)

Upon selecting a genre, a list of recommended tracks will be displayed along with the following information:

- Song title
- Song artist(s)
- Timestamp of associated Reddit post
- Song duration

## Listen Mode

![listen](https://raw.githubusercontent.com/zenlyj/jukebox/main/docs/listen.PNG)

In the Listen page, a playlist is shown, consisting of tracks added from the Discover page. At the bottom of the page, the music player is used to control music playback.
