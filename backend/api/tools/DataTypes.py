from typing import List
from typing import Tuple
from enum import Enum

SpotifyArtistData = Tuple[str, List[str], str]

SpotifySearchTrackArtistData = Tuple[str, str]

SpotifySearchTrackData = Tuple[
    str, List[SpotifySearchTrackArtistData], str, str, int, str
]

RedditData = Tuple[str, str]

Genre = Enum("Genre", ["HIPHOP", "ELECTRONIC", "INDIE", "GENERAL"])

SubName = {
    Genre.HIPHOP: "hiphopheads",
    Genre.ELECTRONIC: "electronicmusic",
    Genre.INDIE: "indieheads",
}
