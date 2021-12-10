from flask import Flask
from werkzeug.exceptions import InternalServerError, NotImplemented
from controller.uiux import read_query
from controller.parse_query import parse_query
from controller.process_query import process_query
from controller.ranking import RankingApi
from controller.dds import DDSApi, request_to_dds, handle_dds_result
from controller.evaluation import evaluation
app = Flask(__name__)

@app.route('/.well-known/gpc.json', methods = ['GET'])
def gpc():
    """
    See [https://globalprivacycontrol.github.io/gpc-spec/]
    """
    return {
        "gpc": True,
        "lastUpdate": "2021-12-09"
    }


@app.route('/search', methods = ['GET'])
async def search():
    user_query = read_query()
    
    # Parse "include", -exclude, and site:filter.com
    user_query = parse_query(user_query)
    
    processed_query = process_query(user_query)
    
    try:
        ranked = await RankingApi.instance.rank(processed_query)
    except Exception as e:
        #TODO: log exception
        raise InternalServerError("Error getting results from ranking")
    
    try:
        doc_info = await DDSApi.instance.get_document_info(ranked.documents)
    except Exception as e:
        #TODO: log exception
        #TODO: We might be able to recover here
        raise InternalServerError("Error getting results from DDS")
    
    # Build response
    
    response = evaluation()
    return response


@app.route('/track', methods = ['POST'])
def track():
    # TODO
    raise NotImplemented()
