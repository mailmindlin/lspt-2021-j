from dataclasses import dataclass
from typing import Optional, List
from enum import Enum

from werkzeug.user_agent import UserAgent

class SearchFormat(Enum):
	JSON = 'json'
	XML = 'xml'


@dataclass
class SearchQuery:
	"""
	UserQuery store the user query information parsed from UI/UX team
	"""
	
	query: str
	exclude: List[str]
	include: List[str]
	site: Optional[str] = None
	
	offset: int = 0
	page_size: int = 20
	accept: SearchFormat = SearchFormat.JSON
	
	# Tracking
	sensitive: bool = False
	query_id: Optional[str] = None
	user_id: Optional[str] = None
	user_agent: Optional[UserAgent] = None