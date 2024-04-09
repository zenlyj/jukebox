def similarity(query: str, result: str) -> float:
    query_keywords = set(query.strip().lower().split())
    result_keywords = set(result.strip().lower().split())
    matching_keywords = set.intersection(query_keywords, result_keywords)
    return len(matching_keywords) / len(query_keywords)
