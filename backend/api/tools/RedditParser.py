from typing import List
from typing import Union
from api.tools.DataTypes import SubName
from api.tools.DataTypes import Genre
from api.tools.DataTypes import RedditData
import re


class RedditParser:
    name_stop_words = ["official music video", "official video", "produced by"]
    artist_stop_words = ["&", ",", "x "]
    misc_stop_words = [
        r"[\[|\()]([2][0-9]{3})[\]|\)]",
        "feat. ",
        "ft. ",
        "ft ",
        "\(",
        "\)",
        "\[",
        "\]",
    ]
    tag, tag_regex = "[fresh]", "\[fresh\]"

    def parse(self, subreddit: str, submissions: List[object]) -> List[RedditData]:
        relevant_submissions = [
            submission
            for submission in submissions
            if self.tag in submission.title.lower()
        ]
        titles: List[str] = [submission.title for submission in relevant_submissions]
        normalized_titles = []
        if subreddit == SubName[Genre.HIPHOP]:
            normalized_titles = [
                title for title in self._parse_hiphopheads_titles(titles) if title
            ]
        if subreddit == SubName[Genre.ELECTRONIC]:
            normalized_titles = [
                title for title in self._parse_electronicmusic_titles(titles) if title
            ]
        if subreddit == SubName[Genre.INDIE]:
            normalized_titles = [
                title for title in self._parse_indieheads_titles(titles) if title
            ]
        created_timestamps = [
            str(int(submission.created_utc)) for submission in relevant_submissions
        ]
        return [
            (data[0], data[1]) for data in zip(normalized_titles, created_timestamps)
        ]

    def _parse_hiphopheads_titles(self, titles: List[str]) -> List[str]:
        return [self._normalize(title) for title in titles]

    def _parse_electronicmusic_titles(self, titles: List[str]) -> List[str]:
        return [self._normalize(title) for title in titles]

    def _parse_indieheads_titles(self, titles: List[str]) -> List[str]:
        return [self._normalize(title) for title in titles]

    def _normalize(self, title: str) -> Union[str, None]:
        split = self._remove_tag(title).split("-")
        if len(split) < 2:
            return None
        name, artist = split[1], split[0]
        normalized_name, normalized_artist = self._normalize_name(
            name
        ), self._normalize_artist(artist)
        normalized_title = self._remove_misc(f"{normalized_name} {normalized_artist}")
        return normalized_title

    def _remove_tag(self, title: str) -> str:
        return re.sub(self.tag_regex, "", title.lower()).strip()

    def _normalize_name(self, name: str) -> str:
        new_name = name.lower().strip()
        for stop_word in self.name_stop_words:
            new_name = re.sub(stop_word, "", new_name)
        return new_name.strip()

    def _normalize_artist(self, artist: str) -> str:
        new_artist = artist.lower().strip()
        for stop_word in self.artist_stop_words:
            new_artist = re.sub(stop_word, "", new_artist)
        return new_artist.strip()

    def _remove_misc(self, title: str) -> str:
        new_title = title
        for stop_word in self.misc_stop_words:
            new_title = re.sub(stop_word, "", new_title)
        return " ".join(new_title.strip().split())
