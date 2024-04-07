from typing import List
from typing import Tuple
from enum import Enum

SpotifyData = Tuple[str, List[str], str, str, int, str]

Genre = Enum('Genre', ['HIPHOP', 'ELECTRONIC'])

SubName = {
    Genre.HIPHOP: 'hiphopheads',
    Genre.ELECTRONIC: 'electronicmusic'
}