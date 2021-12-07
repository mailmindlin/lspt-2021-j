from flask import Flask
from controller.uiux import handle_user_query
from controller.process_query import process_query
from controller.ranking import request_to_rank, handle_ranking_result
from controller.dds import request_to_dds, handle_dds_result
from controller.evaluation import evaluation
app = Flask(__name__)

@app.route('/search', methods = ['GET'])
def search():
    user_query = handle_user_query()
    processed_query = process_query(user_query)
    ranking_result = request_to_rank(processed_query)
    document_ids = handle_ranking_result(ranking_result)
    dds_result = request_to_dds(document_ids)
    documents = handle_dds_result(dds_result)
    response = evaluation(documents)
    return response
    
    

@app.route('/track', methods = ['POST'])
def track():
    # TODO
    pass
