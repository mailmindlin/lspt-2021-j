from flask import json, jsonify
import requests

class DocumentResults:
    def __init__(self, _error, _documents) -> None:
        self.error = _error
        self.documents = _documents

class DocumentInfo:
    def __init__(self, _id, _url, _title, _last_updated) -> None:
        self.id = _id
        self.url = _url
        self.title = _title
        self.last_updated = _last_updated

# Map keys to classes
mapping = {frozenset(('id',
                                        'url',
                                        'title',
                                        'last_updated')): DocumentInfo,
                    frozenset(('error',
                                        'documents')): DocumentResults}

# helper function to extract variable from nested json into different classes
def class_mapper(d):
    return mapping[frozenset(d.keys())](**d)


# handle_dds_result handle the response from DDS team and return array of documents id 
def handle_dds_result(dds_result):
    # if received result got error, directly send error msg to UI/UX and return empty array
    if dds_result.error != '':
        # TODO: send error msg to UIUX
        return []
    # otherwise, extract document IDs from the parsed data and return an array of document IDs
    else:
        documents = []
        for k in len(dds_result.documents):
            documents.append(dds_result.documents[k])
        return documents


# request_to_rank sends POST request to DDS with a formatted json file and return DDS result from remote server
def request_to_dds(documents_id):
    # convert  information into a json form
    data = jsonify(
        documents = documents_id
    )
    # send POST request to ranking server
    resp = requests.post(url='',  json = data)
    # return ranking result
    dds_result = json.loads(resp, object_hook = class_mapper)
    return dds_result