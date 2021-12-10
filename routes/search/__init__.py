from .. import blueprint

import traceback
import uuid
from werkzeug.exceptions import BadRequest, InternalServerError

from client.ranking import RankRequest, RankingClient
from client.dds import DDSClient

from .read_query import read_query
from .parse_query import parse_query
from .process_query import process_query
from .response import SearchResponse
from .SensitivityPredictor import SensitivityPredictor, SensitivityPredictorBase
SensitivityPredictor: SensitivityPredictorBase


@blueprint.route('/search', methods = ['GET'])
async def search():
	raw_query = read_query()
	query = raw_query
	warnings = list()
	
	query_id = uuid.uuid4()
	
	# Parse "include", -exclude, and site:filter.com\
	try:
		query = parse_query(query)
	except Exception as e:
		print("ERROR persing user query")
		traceback.print_exc()
		# Swallow (we just won't disamiguate)
		warnings.append("There was a problem parsing the query text")
	
	if (not query.sensitive) and  SensitivityPredictor.is_sensitive(raw_query.display_query):
		query.sensitive = True
	
	processed_query = process_query(query)
	
	try:
		ranked = await RankingClient.instance.rank(RankRequest(
			query=query.query,
			sensitive=query.sensitive,
			first_result=query.offset,
			last_result=query.offset + query.page_size,
		))
	except Exception as e:
		#TODO: log exception
		raise InternalServerError(f"Error getting results from ranking: {traceback.format_exc()}")
	
	docIds = ranked.documents
	# Trim to page_size
	if len(docIds) > query.page_size:
		docIds = docIds[:query.page_size]
	
	try:
		doc_info = await DDSClient.instance.get_document_info(ranked.documents)
	except Exception as e:
		#TODO: log exception
		#TODO: We might be able to recover here
		# raise InternalServerError("Error getting results from DDS")
		pass
	
	
	# Build response
	warnings.append(f"processed={query}")
	response = SearchResponse(
		query_id = str(query_id),
		offset = query.offset,
		query_display = raw_query.display_query,
		format = query.accept,
		sensitive = query.sensitive,
		warnings = warnings,
	)
	return response.to_response()