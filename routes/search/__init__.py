from .. import blueprint

import traceback
from werkzeug.exceptions import BadRequest, InternalServerError

from client.ranking import RankRequest, RankingClient
from client.dds import DDSClient

from .read_query import read_query
from .parse_query import parse_query
from .process_query import process_query
from .response import SearchResponse


@blueprint.route('/search', methods = ['GET'])
async def search():
	user_query = read_query()
	warnings = list()
	
	# Parse "include", -exclude, and site:filter.com\
	try:
		user_query = parse_query(user_query)
	except Exception as e:
		print("ERROR persing user query")
		traceback.print_exc()
		# Swallow (we just won't disamiguate)
		warnings.append("There was a problem parsing the query text")
	
	processed_query = process_query(user_query)
	
	try:
		ranked = await RankingClient.instance.rank(RankRequest(
			query=user_query.query,
			sensitive=user_query.sensitive,
			first_result=user_query.offset,
			last_result=user_query.offset + user_query.page_size,
		))
	except Exception as e:
		#TODO: log exception
		raise InternalServerError(f"Error getting results from ranking: {traceback.format_exc()}")
	
	try:
		doc_info = await DDSClient.instance.get_document_info(ranked.documents)
	except Exception as e:
		#TODO: log exception
		#TODO: We might be able to recover here
		raise InternalServerError("Error getting results from DDS")
	
	# Build response
	response = SearchResponse(
		query_id="sdf",
		format = user_query.accept,
		sensitive=True,
		warnings=warnings
	)
	return response.to_response()