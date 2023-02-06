import requests

from solvedac.error import SuggestionsApiError


def search_suggestion(query: str):
    """
    검색어 자동완성
    :param query: 검색어
    :return: 자동완성 결과
    """
    url = "https://solved.ac/api/v3/search/suggestion"
    params = {"query": query}
    headers = {"Content-Type": "application/json"}

    response = requests.get(url=url, params=params, headers=headers)

    status_code = response.status_code
    match status_code:
        case 200:
            return response.json()
        case _:
            raise SuggestionsApiError(
                f"unexpected error: status code: {status_code}"
            )
