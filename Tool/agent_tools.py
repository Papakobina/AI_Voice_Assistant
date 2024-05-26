from langchain_community.tools.tavily_search import TavilySearchResults


def get_up_to_date_answer_tavily(query:str) -> str:
    """
    Searches for Most upto date answer on Tavily and return the url
    """
    search = TavilySearchResults()
    res = search.run(f'{query}')
    return res[0]["url"]