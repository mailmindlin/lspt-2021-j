from flask import json, jsonify
import requests
from process_query import ProcessedQuery


class RankRequest:
    def __init__(self, _api_version, _query, _sensitive, _first_result, _last_result) -> None:
        self.api_version =_api_version
        self.query = _query
        self.sensitive = _sensitive
        self.first_result = _first_result
        self.last_result = _last_result


class RankResult:
    def __init__(self, _error, _page, _ranking_speed, _documents) -> None:
        self.error = _error
        self.page = _page
        self.ranking_speed = _ranking_speed
        self.documents = _documents

class DocumentInfo:
    def __init__(self, _id, _url, _title) -> None:
        self.id = _id
        self.url = _url
        self.title = _title


# Map keys to classes
mapping = {frozenset(('id',
                                        'url',
                                        'title',
                                        'snippet',
                                        'last_crawled')): DocumentInfo,
                    frozenset(('error',
                                        'page',
                                        'ranking_speed',
                                        'documents')): RankResult}

# helper function to extract variable from nested json into different classes
def class_mapper(d):
    return mapping[frozenset(d.keys())](**d)

# handle_ranking_result handle the response from ranking team and extract necessary information from response
def handle_ranking_result(ranking_result):
    # if received result got error, directly send error msg to UI/UX and return empty array
    if ranking_result.error != '':
        # TODO: send error msg to UIUX
        return []
    # otherwise, extract document IDs from the parsed data and return an array of document IDs
    else:
        documents_id = []
        for k in len(ranking_result.documents):
            documents_id.append(ranking_result.documents[k].id)
        return documents_id

# request_to_rank sends POST request to Ranking with a formatted json file and return ranking result from remote server
def request_to_rank(_api_version, _query, _sensitive, _first_result, _last_result):
    # jquery convert query with class ProcessedQuery into json form
    jquery = json.dumps(_query.__dict__)

    # convert all information into a json form
    data = jsonify(
        api_version = _api_version,
        query = jquery,
        sensitive = _sensitive,
        first_result = _first_result,
        last_result = _last_result
    )
    # send POST request to ranking server
    resp = requests.post(url='127.0.0.1',  json = data)
    # return ranking result
    ranking_result = json.loads(resp, object_hook = class_mapper)
    return ranking_result