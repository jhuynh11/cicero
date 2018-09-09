from textblob import TextBlob, Word
from textblob.wordnet import VERB
import praw
from praw.models import MoreComments
import pandas as pd
from collections import Counter
import numpy as np


def most_used_word(phrase):
    text = TextBlob(phrase)
    out = ""
    for word in text.words:
        print(text.words.count(word))


def subreddit_scrape(reddit, subreddit_name, limit):
    """
    Scrapes the subredits within subreddit_list
    :param reddit: Reddit object used to connect to the subreddit
    :param subreddit_name: Name of subreddit to scrape
    :param limit: Number of submissions to scrape
    :return: Pandas Dataframe of the scraped subreddit
    """

    subreddit = reddit.subreddit(subreddit_name)

    top_subreddit = subreddit.top(limit=limit,
                                  time_filter='year')

    topics_dict = {"title": [],
                   "score": [],
                   "id": [],
                   "url": [],
                   "comms_num": [],
                   "created": [],
                   "body": [],
                   "comments": []}

    for submission in top_subreddit:
        topics_dict["title"].append(submission.title)
        topics_dict["score"].append(submission.score)
        topics_dict["id"].append(submission.id)
        topics_dict["url"].append(submission.url)
        topics_dict["comms_num"].append(submission.num_comments)
        topics_dict["created"].append(submission.created)
        topics_dict["body"].append(submission.selftext)
        topics_dict["comments"].append(submission.comments)

    return pd.DataFrame(topics_dict)


def get_sentiment(df, subreddit_name):
    """
    Returns the sentiment of comments
    :param df: Dataframe of scraped subreddit information
    :return: Dataframe of comments and their sentiment
    """

    comments_sentiment = {"title": [],
                          "comment": [],
                          "polarity": [],
                          "subjectivity": []}

    for index, row in df.iterrows():
        for top_level_comment in row["comments"]:
            comments_sentiment["title"].append(row["title"])
            row["comments"].replace_more(limit=None)
            text = TextBlob(top_level_comment.body)
            polarity = text.sentiment.polarity
            subjectivity = text.sentiment.subjectivity
            comments_sentiment["comment"].append(top_level_comment.body)
            comments_sentiment["polarity"].append(polarity)
            comments_sentiment["subjectivity"].append(subjectivity)

    data = pd.DataFrame(comments_sentiment)
    data.to_csv(subreddit_name + '_sentiment.csv')
    print("Sentiment for " + subreddit_name + " outputted.")


def get_frequency(text):
    pass


if __name__ == '__main__':
    # reddit = praw.Reddit(client_id='XXX',
    #                      client_secret='XXX',
    #                      user_agent='XXX')

    cities = ["ottawa", "toronto", "vancouver"]

    # for city in cities:
    #     df = subreddit_scrape(reddit, city, limit=200)
    #     get_sentiment(df, city)

    # df = subreddit_scrape(reddit, 'ottawa', limit=200)
    # get_sentiment(df, 'ottawa')
    data = pd.read_csv('ottawa_sentiment.csv')
    print(data.describe())
    data = pd.read_csv('toronto_sentiment.csv')
    print(data.describe())
    data = pd.read_csv('vancouver_sentiment.csv')
    print(data.describe())
    # pivot = pd.pivot_table(data, index=["title"], values=["polarity"])
    # pivot.to_csv('test.csv')

    # tblob = TextBlob(str(data["comment"].tolist()))
    # print(tblob.noun_phrases)
    # cnt = Counter(str(tblob.noun_phrases).split()).most_common(100)
    # print(cnt)


