from __future__ import annotations
from typing import Literal
import json
import requests
from process_query import ProcessedQuery
from dataclasses import dataclass


@dataclass
class RankRequest:
    query: str
    sensitive: bool
    first_result: int
    last_result: int
    api_version: Literal[1] = 1
    
    def toJSON(self):
        return {
            'api_version': self.api_version,
            'query': self.query,
            'sensitive': self.sensitive,
            'first_result': self.first_result,
            'last_result': self.last_result,
        }

class RankResult:
    def __init__(self, _error, _page, _ranking_speed, _documents) -> None:
        self.error = _error
        self.page = _page
        self.ranking_speed = _ranking_speed
        self.documents = _documents

@dataclass
class DocumentInfo:
    id: str
    url: str
    title: str


class RankingApi:
    instance: RankingApi
    
    def __init__(self, url: str):
        self.url = url
    
    async def _rank_send_request(self, request: str) -> requests.Response:
        raise NotImplemented
    
    async def rank(self, request: RankRequest) -> RankResult:
        """
        request_to_rank sends POST request to Ranking with a formatted json file and return ranking result from remote server
        """
        json_request = json.dumps(request.toJSON())
        # send POST request to ranking server
        resp = requests.post(url=self.url, json=json_request)
        if resp.status_code != 200:
            raise RuntimeError(f"Unable to load data from ranking: {resp.status_code}")
        
        # return ranking result
        
        ranking_result = json.loads(resp, object_hook = class_mapper)
        return ranking_result


RankingApi.instance = RankingApi('')

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

def rank_query(query: ProcessedQuery):
    first_result = query.offset
    last_result = query.page_size-first_result
    
    request = RankRequest(
        
    )
    
    
# 
def request_to_rank(api_version: int, query: str, sensitive: bool, first_result: int, last_result: int):
    # jquery convert query with class ProcessedQuery into json form
    jquery = json.dumps(_query.__dict__)

    # convert all information into a json form
    data = jsonify(
        api_version = api_version,
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