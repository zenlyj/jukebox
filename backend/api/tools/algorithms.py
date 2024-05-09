import numpy as np
from typing import List


def similarity(query: str, result: str) -> float:
    query_keywords = set(query.strip().lower().split())
    result_keywords = set(result.strip().lower().split())
    matching_keywords = set.intersection(query_keywords, result_keywords)
    return len(matching_keywords) / len(query_keywords)


def score(
    all_genres: List[int], user_preferred_genres: List[int], song_genres: List[int]
) -> int:
    n = len(all_genres)
    preferred_set, song_set = set(user_preferred_genres), set(song_genres)
    preference_vector = np.array(
        [1 if all_genres[i] in preferred_set else 0 for i in range(n)]
    )
    song_vector = np.array([1 if all_genres[i] in song_set else 0 for i in range(n)])
    return np.dot(preference_vector, song_vector)
