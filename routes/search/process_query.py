from .query import SearchQuery

# ProcessedQuery contains information about processed query
class ProcessedQuery:
    def __init__(self, _raw, _lang, _include, _exclude)  -> None:
        self.raw = _raw
        self.lang = _lang
        self.include = _include
        self.exclude = _exclude


def process_query(user_query: SearchQuery) -> SearchQuery:
    """
    Expand synonyms
    """
    # TODO: do some processing
    return user_query