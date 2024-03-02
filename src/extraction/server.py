"""This is the module that extracts news and stores in mongodb through api calls.
"""

import atexit
import datetime
import os

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from core_nlp.rule_based import RuleBasedModel
from core_nlp.gpt import GPTModel
from linguistics import preprocess
from news import extract
from sql_svc import query
from mongo_svc import access

# configures Flask server and mysql database
server = Flask(__name__)

# config
config = {
    "SQL_SVC_ADDRESS": os.environ.get("SQL_SVC_ADDRESS"),
    "MONGO_SVC_ADDRESS": os.environ.get("MONGO_SVC_ADDRESS")
}

def main():
    """The function that extracts news and processes news before sending it to mongodb for storage.

    Returns:
        A tuple, A result/error message and A status code.
    """
    # fetch parameters from yaml files
    # nlp_method: A string that indicates the core nlp method type. Possible option: 'rule-based', 'gpt'.
    nlp_method = os.environ.get("NLP_METHOD")
    # search_category: The category you want to get headlines for. Possible options: business, entertainment,
    # general, health, science, sports, technology.
    search_category = os.environ.get("SEARCH_CATEGORY")
    # search_country: The 2-letter ISO 3166-1 code of the country you want to get headlines for. e.g. 'us'.
    search_country = os.environ.get("SEARCH_COUNTRY")

    if nlp_method == 'rule-based':
        model = RuleBasedModel()
    elif nlp_method == 'gpt':
        model = GPTModel()
    else:
        return f"Incorrect core nlp method: {nlp_method}", 404

    # Fetch keywords from sql db for all usernames
    query_res, err = query.get_keywords(config)
    print(query_res)
    
    if not err:
        for keyword in query_res:
            data = {
                'keyword': keyword
            }

            # Extract news given keywords
            crawler = extract.activate_crawler(os.environ.get("NEWS_API_KEY"))
            search_result = extract.search_news(crawler, keyword, search_category, search_country)
            if search_result['totalResults'] != 0:
                all_articles = extract.get_articles(search_result)

                # Iterate through all extracted articles
                for article in all_articles:
                    # Preprocess raw texts
                    article['paragraphs'] = preprocess.filter_paragraphs(
                        preprocess.get_paragraphs(article["text"]), keyword
                    )
                    
                    # Use core nlp to generate report
                    extracted_paragraphs = "\n".join(article['paragraphs'])
                    article['events'] = model.find_events(extracted_paragraphs, keyword)

                # Store report to mongo db
                data['news'] = all_articles
                _, err = access.store(config, data)
                if err:
                    return err
            else:
                print(f"no article found for keyword: {keyword}")
    else:
        return err

    return f'successful news extraction, timestamp: {datetime.datetime.utcnow()}', 200

def test():
    print('yes!')

# initiates aps scheduler
scheduler = BackgroundScheduler(daemon=True)
# add main function to scheduler and start scheduler
scheduler.add_job(func=test, trigger='interval', seconds=30)
scheduler.start()

# shut down the scheduler when exiting the flask server
# atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=9050, debug=True)
    # scheduler = BlockingScheduler()
    # scheduler.add_job(main, 'interval', minutes=1)
    # scheduler.start()

    # # initiates aps scheduler
    # scheduler = BackgroundScheduler(daemon=True)
    # # add main function to scheduler and start scheduler
    # scheduler.add_job(func=test, trigger='interval', seconds=15)
    # scheduler.start()

    # nlp_method = 'rule-based'
    # nlp_method = 'gpt'
    # print(main(nlp_method))