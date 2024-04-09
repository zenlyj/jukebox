from typing import List
from typing import Union
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

    def parse(self, subreddit: str, submissions: List[object]) -> List[str]:
        titles: List[str] = [submission.title for submission in submissions]
        if subreddit == "hiphopheads":
            return [title for title in self.__parse_hiphopheads(titles) if title]
        if subreddit == "electronicmusic":
            return [title for title in self.__parse_electronicmusic(titles) if title]
        return []

    def __parse_hiphopheads(self, titles: List[str]) -> List[str]:
        relevant_titles = [title for title in titles if self.tag in title.lower()]
        return [self.__normalize(title) for title in relevant_titles]

    def __parse_electronicmusic(self, titles: List[str]) -> List[str]:
        relevant_titles = [title for title in titles if self.tag in title.lower()]
        return [self.__normalize(title) for title in relevant_titles]

    def __normalize(self, title: str) -> Union[str, None]:
        split = self.__remove_tag(title).split("-")
        if len(split) < 2:
            return None
        name, artist = split[1], split[0]
        normalized_name, normalized_artist = self.__normalize_name(
            name
        ), self.__normalize_artist(artist)
        normalized_title = self.__remove_misc(f"{normalized_name} {normalized_artist}")
        return normalized_title

    def __remove_tag(self, title: str) -> str:
        return re.sub(self.tag_regex, "", title.lower()).strip()

    def __normalize_name(self, name: str) -> str:
        new_name = name.lower().strip()
        for stop_word in self.name_stop_words:
            new_name = re.sub(stop_word, "", new_name)
        return new_name.strip()

    def __normalize_artist(self, artist: str) -> str:
        new_artist = artist.lower().strip()
        for stop_word in self.artist_stop_words:
            new_artist = re.sub(stop_word, "", new_artist)
        return new_artist.strip()

    def __remove_misc(self, title: str) -> str:
        new_title = title
        for stop_word in self.misc_stop_words:
            new_title = re.sub(stop_word, "", new_title)
        return " ".join(new_title.strip().split())
