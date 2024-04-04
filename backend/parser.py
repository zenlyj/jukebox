import json
import jellyfish
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
        name, artist_names, uri, album_cover, duration = None, None, None, None, None
        maxSimilarity = float('-inf')
        for i in range(len(result)):
            similarity = self.similarity(result[i], query)
            if  similarity > maxSimilarity:
                maxSimilarity = similarity
                name = result[i]['name']
                artist_names = [artist['name'] for artist in result[i]['artists']]
                uri = result[i]['uri']
                album_cover = result[i]['album']['images'][0]['url']
                duration = result[i]['duration_ms']
                spotify_id = result[i]['id']
        return name, artist_names, uri, album_cover, duration, spotify_id

    def similarity(self, searchResult, query) -> float:
        match = ''
        match += searchResult['name']
        for artist in searchResult['artists']:
            match += ' '
            match += artist['name']
            break
        dist = jellyfish.levenshtein_distance(match, query)
        length = max(len(match), len(query))
        return float(length - dist) / float(length)
         