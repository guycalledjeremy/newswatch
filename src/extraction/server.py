"""This is the module that extracts news and stores in mongodb through api calls.
"""

import datetime

# from flask import Flask, request
from apscheduler.schedulers.blocking import BlockingScheduler

from common import config_utils
from core_nlp import rule_based
from .news import extract
from .sql_svc import query
from .mongo_svc import access

# config
config = config_utils.load_config("extraction/config.yaml")
# secret config
secret = config_utils.load_config("extraction/secret.yaml")

def main(config, search_category="business", search_country="us"):
    """The function that extracts news and processes news before sending it to mongodb for storage.

    Args:
        config: dictionary with config information.
        search_category: The category you want to get headlines for. Possible options: business, entertainment,
        general, health, science, sports, technology.
        search_country: The 2-letter ISO 3166-1 code of the country you want to get headlines for. e.g. 'us'.

    Returns:
        A tuple, A result/error message and A status code.
    """
    # Fetch keywords from sql db for all usernames
    query_res, err = query.get_keywords(config)
    
    if not err:
        for keyword in query_res:
            # Extract news given keywords
            crawler = extract.activate_crawler(secret["NEWS_API_KEY"])
            search_result = extract.search_news(crawler, keyword, search_category, search_country)
            raw_articles = extract.get_articles(search_result)

            # Use core nlp to generate report

            # Store report to mongo db
            raw_data = {
                'keyword': keyword,
                'news': raw_articles
            }
            _, err = access.store(config, raw_data)
            if err:
                return err
    else:
        return err

    return f'successful news extraction, timestamp: {datetime.datetime.utcnow()}', 200

if __name__ == "__main__":
    # server.run(host="0.0.0.0", port=9050, debug=True)
    # scheduler = BlockingScheduler()
    # scheduler.add_job(main, 'interval', minutes=1)
    # scheduler.start()

    print(main(config))
    # print(query.get_keywords(config))