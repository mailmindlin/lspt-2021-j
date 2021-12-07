from uiux import UserQuery

# ProcessedQuery contains information about processed query
class ProcessedQuery:
    def __init__(self, _raw, _lang, _include, _exclude)  -> None:
        self.raw = _raw
        self.lang = _lang
        self.include = _include
        self.exclude = _exclude


# process_query return the processed query after processing given the unprocssed query as input
def process_query(user_query):
    # TODO: do some processing
    pass