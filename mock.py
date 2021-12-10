
from typing import Any, Dict, List

from client.ranking import DocumentInfo


def mock_ranking(request):
	raise NotImplemented

def mock_dds(request):
	raise NotImplemented

def fake_data() -> List[Dict[str, str]]:
	id = 0
	result = []
	def fake(search: str, url: str, title: str):
		nonlocal id
		id += 1
		result.append({
			'id': id,
			'search': search,
			'url': url,
			'title': title,
		})
	
	fake('dog', 'https://en.wikipedia.org/wiki/Dog', 'Dog - Wikipedia')
	fake('dog', 'https://www.petfinder.com/dog-breeds/', 'List of Dog Breeds | Petfinder')
	fake('dog', 'https://www.nationalgeographic.com/animals/mammals/facts/domestic-dog', 'Dog, facts and photos - National Geographic')
	fake('puppy', 'https://en.wikipedia.org/wiki/Puppy', 'Puppy - Wikipedia')
	return result
	
	
def inject_mocks():
	print("-" * 80)
	print("    Mocking client APIs")
	print("-" * 80)
	
	data = fake_data()
	
	
	from client.ranking import RankingClient, RankRequest, RankResult
	
	class RankingClientMock(RankingClient):
		def __init__(self):
			pass
		
		async def rank(self, request: RankRequest) -> RankResult:
			def match_item(item: Dict[str, str]):
				return (item['search'] in request.query)
			
			candidates = list(filter(match_item, data))
			if len(candidates) > 0:
				return RankResult(
					page = request.first_result,
					ranking_speed=5,
					documents=[DocumentInfo(
						id=document['id'],
						url=document['url'],
						title=document['title'],
					) for document in candidates]
				)
			raise RuntimeError("no ranking results")
	
	RankingClient.instance = RankingClientMock()
	
	from client.dds import DDSClient
	class DDSClientMock(DDSClient):
		def __init__(self) -> None:
			pass
	
	DDSClient.instance = DDSClientMock()