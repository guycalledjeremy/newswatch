"""This is the module that extract news articles when given a keyword. 
"""

from newsapi import NewsApiClient
from newspaper import Article

def activate_crawler(key):
    """Activate api and return a newsapi news cralwer.

    Args:
        key: A string for the api key for newsapi.

    Returns:
        A NewsApiClient object that can query top headlines given keywords.
    """
    return NewsApiClient(api_key=key)

def search_news(crawler, keyword, target_category, target_country):
    """Use newsapi to search top headlines given keywords, it extracts urls to later extract news text.

    Args:
        crawler: A NewsApiClient object.
        keyword: A string for keywords for searching.
        target_category: The category you want to get headlines for. Possible options: business, entertainment,
        general, health, science, sports, technology.
        target_country: The 2-letter ISO 3166-1 code of the country you want to get headlines for. e.g. 'us'.

    Returns:
        A dictionary that contains a list of articles and a count of total results.
    """
    return crawler.get_top_headlines(
        category=target_category,
        q=keyword,
        country=target_country
    )

def get_articles(search_result):
    """Given crawler's search result, extract full text from the news' url.

    Args:
        search_reult: Crawler's search result, a dictionary that contains a list of articles and a count of total
        results.

    Returns:
        A list of articles including full texts.
    """
    articles = []

    if search_result['totalResults'] > 0:
        for result in search_result['articles']:
            try:
                # extract text from url
                article = Article(result['url'])
                article.download()
                # parse the text from the web page
                article.parse() 

                # create news dictioinary
                news = {}
                news["authors"] = article.authors
                if article.publish_date:
                    news["date"] = article.publish_date.strftime("%m/%d/%Y, %H:%M:%S")
                news["text"] = article.text
                news["title"] = result['title']

                # store this news to the final list
                articles.append(news)
            except Exception as e:
                print(e)

    return articles