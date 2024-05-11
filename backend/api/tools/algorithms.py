import numpy as np
from typing import Set


def similarity(query: str, result: str) -> float:
    query_keywords = set(query.strip().lower().split())
    result_keywords = set(result.strip().lower().split())
    matching_keywords = set.intersection(query_keywords, result_keywords)
    return len(matching_keywords) / len(query_keywords)


def preference_score(
    all_genres: Set[int], user_preferred_genres: Set[int], song_genres: Set[int]
) -> int:
    genres = list(all_genres)
    n = len(genres)
    preference_vector = np.array(
        [1 if genres[i] in user_preferred_genres else 0 for i in range(n)]
    )
    song_vector = np.array([1 if genres[i] in song_genres else 0 for i in range(n)])
    return np.dot(preference_vector, song_vector)
