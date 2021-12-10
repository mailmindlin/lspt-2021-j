from flask import request

from werkzeug.exceptions import BadRequest

from ..model.search import SearchQuery
DEFAULT_PAGE_SIZE = 20


def read_query():
    """
    Parses a UserQuery from the HTTP request fields
    """
    query = request.args.get("q")
    if query is None:
        raise BadRequest("No query provided")
    
    q_site = request.args.get("q_site")
    
    #TODO: test that we throw a HTTP 400 if these fields aren't valid ints
    offset = request.args.get("offset", default=0, type=int)
    if (offset is None) or offset < 0:
        raise BadRequest("Invalid field: offset")
    
    page_size = request.args.get("page_size", default=DEFAULT_PAGE_SIZE, type=int)
    if (page_size is None) or (page_size < 1):
        raise BadRequest("Invalid field: page_size")
    
    #TODO: is there a better way of passing DNT?
    dnt = False
    if request.headers.get("DNT") == "1":
        dnt = True
    if request.headers.get("Sec-GPC") == "1":
        dnt = True
    
    return SearchQuery(
        query=query,
        exclude=request.args.getlist("q_exclude"),
        include=request.args.getlist("q_include"),
        site=q_site,
        offset=offset,
        page_size=page_size,
        
        sensitive=dnt,
        query_id=request.args.get("q_id"),
        user_id=request.args.get("uid"),
        user_agent=request.user_agent,
    )