from __future__ import annotations
from typing import Any, Literal, List, Dict
import json
import requests
from dataclasses import dataclass
from .client import RESTfulClient


@dataclass
class RankRequest:
    query: str
    sensitive: bool
    first_result: int
    last_result: int
    api_version: Literal[1] = 1
    
    def to_json(self):
        return {
            'api_version': self.api_version,
            'query': self.query,
            'sensitive': self.sensitive,
            'first_result': self.first_result,
            'last_result': self.last_result,
        }

@dataclass
class RankResult:
    page: int
    ranking_speed: int
    documents: List[DocumentInfo]

@dataclass
class DocumentInfo:
    @staticmethod
    def parse(raw: Dict[str, str]):
        return DocumentInfo(
            id = raw['id'],
            url = raw['url'],
            title = raw['title'],
        )
    
    id: str
    url: str
    title: str


class RankingClient(RESTfulClient):
    instance: RankingClient
    
    def __init__(self, url: str):
        self.url = url
    
    async def _rank_send_request(self, request: RankRequest):
        # send POST request to ranking server
        return requests.post(
            url = self.url,
            json=json.dumps(request.to_json()),
            headers={
                'Accept': 'application/json',
            }
        )
    def _rank_parse_response(self, response: Dict[str, Any]) -> RankResult:
        if 'error' in response:
            raise RuntimeError(f"Ranking: {response['error']}")
        
        documents = [DocumentInfo.parse(document) for document in response.get(response, [])]
        
        return RankResult(
            page=response['page'],
            ranking_speed=response['ranking_speed'],
            documents=documents
        )
            
    
    async def rank(self, request: RankRequest) -> RankResult:
        """
        request_to_rank sends POST request to Ranking with a formatted json file and return ranking result from remote server
        """
        # send POST request to ranking server
        resp = await self._rank_send_request(request)
        
        if resp.status_code != 200:
            raise RuntimeError(f"Unable to load data from ranking: {resp.status_code}")
        
        # return ranking result
        return self._rank_parse_response(resp.json())


RankingClient.instance = RankingClient('')

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