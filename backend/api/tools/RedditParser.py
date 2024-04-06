from typing import List

class RedditParser:
    def parse(self, subreddit: str, submissions: List[object]) -> List[str]:
        titles: List[str] = [submission.title for submission in submissions]
        if subreddit == "hiphopheads":
            return self.parse_hiphopheads(titles)
        return []

    def parse_hiphopheads(self, titles: List[str]) -> List[str]:
        tag = '[FRESH]'
        relevant_titles = [title for title in titles if tag in title]
        return [title.replace(tag, "") for title in relevant_titles]
