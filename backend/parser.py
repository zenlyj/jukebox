import json
from typing import List

class Parser:
    def parse(self, subreddit, titles) -> List[str]:
        if subreddit == "hiphopheads":
            return self.parseHipHopHeads(titles)

    def parseHipHopHeads(self, titles) -> List[str]:
        relevantTitles = list(filter(lambda title : "[FRESH]" in title, titles))
        return list(map(lambda title: title.replace("[FRESH] ", ''), relevantTitles))

    def parseSpotifySearch(self, result, query):
        result = json.loads(result)
        return self.getBestResult(result['tracks']['items'], query)

    def getBestResult(self, result, query):
        name, artist_names, uri, album_cover, duration, spotify_id = None, None, None, None, None, None
        maxSimilarity = float('-inf')
        for i in range(len(result)):
            curr = result[i]
            curr_name, curr_artist_names = curr['name'], [artist['name'] for artist in curr['artists']]
            similarity = self.similarity(query, ' '.join([curr_name, ' '.join(curr_artist_names)]))
            if  similarity > maxSimilarity:
                maxSimilarity = similarity
                name = curr_name
                artist_names = curr_artist_names
                uri = curr['uri']
                album_cover = curr['album']['images'][0]['url']
                duration = curr['duration_ms']
                spotify_id = curr['id']
        return name, artist_names, uri, album_cover, duration, spotify_id

    def similarity(self, query: str, result: str):
        query_keywords = set(query.strip().lower().split(" "))
        result_keywords = set(result.strip().lower().split(" "))
        matching_keywords = set.intersection(set(query_keywords), set(result_keywords))
        return len(matching_keywords)/len(query_keywords)
