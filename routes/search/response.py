import flask
from flask import json
from .query import SearchFormat
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from werkzeug.exceptions import NotImplemented


@dataclass
class SearchResponse:
	query_id: Optional[str]
	query_display: str
	offset: int = 0
	format: SearchFormat = SearchFormat.JSON
	sensitive: bool = False
	warnings: List[str] = field(default_factory=list)
	
	def to_json(self):
		return json.jsonify(
			query_id = self.query_id,
			query_display = self.query_display,
			offset = self.offset,
			warnings = self.warnings if len(self.warnings) > 0 else None
		)
		
	def to_response(self) -> flask.Response:
		if (format == SearchFormat.XML):
			raise NotImplemented("XML output not yet suppported")
		
		
		response = self.to_json()
		if self.sensitive:
			response.headers['Tk'] = 'N'
		
		return response