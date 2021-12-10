import re
from typing import List, Tuple
import dataclasses
from .query import SearchQuery


def find_and_replace(pattern: re.Pattern, text: str, replace: str) -> Tuple[str, List[re.Match]]:
	"""Replace all instances of pattern, returning a list of the matches"""
	pattern = re.compile(pattern)
	matches: List[re.Match] = list()
	# Keep track of last position searched, so we don't backtrack
	idx = 0
	while (match:= pattern.search(text, idx)) is not None:
		matches.append(match)
		# Replace match in text
		text = text[:match.pos] + match.expand(replace) + text[match.endpos:]
		idx = match.endpos + 1
	return (text, matches)

def named_group(name: str, value: str):
	return f"(?P<{name}>{value})"
	
def parse_query(raw: SearchQuery) -> SearchQuery:
	"""Parse query text to pull out additional fields"""
	
	query = raw.query
	include = list(raw.include)
	exclude = list(raw.exclude)
	site = raw.site
	
	
	# Word-break look[ahead/behind] (we only want to start/end at beginning/end of string or whitespace)
	lb_word_break = "(^|(?<=\\s))"
	la_word_break = "($|(?=\\s))"
	
	# Find "quote includes"
	quote_include_body = "[^\"]+?"
	quote_include = re.compile(f"{la_word_break}\"{named_group('include', quote_include_body)}\"{lb_word_break}")
	query, include_matches = find_and_replace(quote_include, query, "")
	for match in include_matches:
		include.append(match.group("include"))
	
	# Find hyphen -excludes
	#TODO: we can probably merge this with the quote_include regex
	simple_exclude_body = "[^-\\s][^\\s]*?" # Can't start with quotes
	hyphen_exclude = re.compile(f"{la_word_break}-((\"{named_group('exclude', quote_include_body)}\")|{named_group('exclude1', simple_exclude_body)}){lb_word_break}")
	query, exclude_matches = find_and_replace(hyphen_exclude, query, "")
	for match in exclude_matches:
		exclude.append(match.group('exclude') or match.group('exclude1'))
	
	# Find site:filter
	valid_hostname = "^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\\-]{0,61}[a-zA-Z0-9])(\\.([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\\-]{0,61}[a-zA-Z0-9]))*$"
	site_filter = re.compile(f"{la_word_break}site:{named_group('site', valid_hostname)}{lb_word_break}")
	query, site_matches = find_and_replace(site_filter, query, "")
	for match in site_matches:
		if (site is not None):
			#TODO: warn user?
			pass
		
		site = match.group('site')
	
	result = dataclasses.replace(raw)
	result.query = query
	result.include = include
	result.exclude = exclude
	result.site = site
	
	return result