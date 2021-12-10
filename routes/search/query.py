from dataclasses import dataclass
from typing import Optional, List
from enum import Enum
import re

from werkzeug.user_agent import UserAgent

class SearchFormat(Enum):
	JSON = 'json'
	XML = 'xml'


whitespace = re.compile("\\s")

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
	
	@property
	def display_query(self) -> str:
		result = self.query.strip()
		for exclude in self.exclude:
			if re.search(whitespace, exclude):
				result += f' -"{exclude}"'
			else:
				result += f' -{exclude}'
		
		for include in self.include:
			#TODO: handle double quotes in include string?
			result += f' "{include}"'
		
		if self.site is not None:
			result += f' site:{self.site}'
		
		# Strip again if we started with an empty query string
		return result.strip()