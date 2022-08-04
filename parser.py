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
        difference = float('inf')
        for i in range(len(result)):
            levDist = self.getLevDist(result[i], query)
            if levDist < difference:
                difference = levDist
                uri = result[i]['uri']
        return uri

    def getLevDist(self, searchResult, query):
        match = ''
        match += searchResult['name']
        for artist in searchResult['artists']:
            match += ' '
            match += artist['name']
            break
        print(match, query)
        return jellyfish.levenshtein_distance(match, query)
         