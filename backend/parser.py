import json
import jellyfish

class Parser:
    def parse(self, subreddit, titles):
        if subreddit == "hiphopheads":
            return self.parseHipHopHeads(titles)

    def parseHipHopHeads(self, titles):
        relevantTitles = list(filter(lambda title : "[FRESH]" in title, titles))
        return list(map(lambda title: title.replace("[FRESH] ", ''), relevantTitles))

    def parseSpotifySearch(self, result, query):
        result = json.loads(result)
        return self.getBestResult(result['tracks']['items'], query)

    def getBestResult(self, result, query):
        uri = None
        maxSimilarity = float('-inf')
        for i in range(len(result)):
            similarity = self.similarity(result[i], query)
            if  similarity > maxSimilarity:
                maxSimilarity = similarity
                uri = result[i]['uri']
        return uri

    def similarity(self, searchResult, query):
        match = ''
        match += searchResult['name']
        for artist in searchResult['artists']:
            match += ' '
            match += artist['name']
            break
        dist = jellyfish.levenshtein_distance(match, query)
        length = max(len(match), len(query))
        return float(length - dist) / float(length)
         