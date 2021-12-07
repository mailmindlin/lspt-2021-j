from werkzeug.wrappers import request

# UserQuery store the user query information parsed from UI/UX team
class UserQuery:
    def __init__(self, _q, _q_site, _q_exclude, _q_include, _qid, _offset, _page_size, _uid, _accept, _user_agent) -> None:
        self.q = _q
        self.q_site = _q_site
        self.q_exclude = _q_exclude
        self.q_include = _q_include
        self.qid = _qid
        self.offset = _offset
        self.page_size = _page_size
        self.uid = _uid
        self.accept = _accept
        self.user_agent = _user_agent

# handle_user_query receives user query from UI/UX team, and return all information need for processing query
def handle_user_query():
    query = request.args.get("q")
    q_site = request.args.get("q_site")
    q_exclude = request.args.get("q_exclude")
    q_include = request.args.get("q_include")
    qid = request.args.get("q_id")
    offset = request.args.get("offset")
    page_size = request.args.get("page_size")
    uid = request.args.get("uid")
    accept = request.args.get("Accept")
    user_agent = request.args.get("User-Agent")
    user_query = UserQuery(query, q_site, q_exclude, q_include, qid, offset, page_size, uid, accept, user_agent)
    return user_query

