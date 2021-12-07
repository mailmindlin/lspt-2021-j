
class QueryResult:
    def __init__(self, _error, _metrics, _offset, _query_display,  _qid, _results) -> None:
        self.error = _error
        self.metrics = _metrics
        self.offset = _offset
        self.query_display = _query_display
        self.qid = _qid
        self.results = _results

class ResultMetics:
    def __init__(self, _computer_time, _total_results) -> None:
        self.computer_time = _computer_time
        self.total_results = _total_results

class ResultEntry:
    def __init__(self, _url, _title, _snippet, _last_updated) -> None:
        self.url = _url
        self.title = _title
        self.snippet = _snippet
        self.last_updated = _last_updated
    
# evaluate and return result in json/xml form
def evaluation():
    # TODO
    pass