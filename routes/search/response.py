from flask import Response, json
from .query import SearchFormat
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from werkzeug.exceptions import NotImplemented


@dataclass
class SearchResponse:
	query_id: Optional[str]
	format: SearchFormat = SearchFormat.JSON
	sensitive: bool = False
	warnings: List[str] = field(default_factory=list)
	
	def to_json(self):
		result: Dict[str, Any] = {
			'query_id': self.query_id,
		}
		
		if len(self.warnings) > 0:
			result['warnings'] = self.warnings
		
		return json.jsonify(result)
		
	def to_response(self) -> Response:
		if (format == SearchFormat.XML):
			raise NotImplemented("XML output not yet suppported")
		
		
		response = self.to_json()
		if self.sensitive:
			response.headers['Tk'] = 'N'
		
		return response