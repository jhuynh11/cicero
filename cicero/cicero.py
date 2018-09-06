from textblob import TextBlob, Word
from textblob.wordnet import VERB
import praw
from praw.models import MoreComments
import pandas as pd


def m1():
    text = TextBlob("She rode her bicycle to the store and and.")
    out = ""
    for word in text.words:
        try:
            out += " " + word.definitions[0]
        except IndexError:
            pass

    print(out)

def most_used_word(phrase):
    text = TextBlob(phrase)
    out = ""
    for word in text.words:
        print(text.words.count(word))


def subreddit_scrape(reddit):
    subreddit = reddit.subreddit('vancouver')

    top_subreddit = subreddit.top(limit=100)
    # hot_subreddit = subreddit.hot(limit=10)

    topics_dict = {"title": [],
                   "score": [],
                   "id": [],
                   "url": [],
                   "comms_num": [],
                   "created": [],
                   "body": [],
                   "comments": []}

    for submission in top_subreddit:
        submission.comments.replace_more(limit=None)
        for top_level_comment in submission.comments:
            print(top_level_comment.body)

    # for submission in top_subreddit:
    #     topics_dict["title"].append(submission.title)
    #     topics_dict["score"].append(submission.score)
    #     topics_dict["id"].append(submission.id)
    #     topics_dict["url"].append(submission.url)
    #     topics_dict["comms_num"].append(submission.num_comments)
    #     topics_dict["created"].append(submission.created)
    #     topics_dict["body"].append(submission.selftext)
    #     topics_dict["comments"].append(submission.comments)


    # topics_data = pd.DataFrame(topics_dict)



def get_comments(reddit):
    submission = reddit.submission(url='https://www.reddit.com/r/funny/comments/3g1jfi/buttons/')
    # or with the submission’s ID which comes after comments / in the URL:
    # submission = reddit.submission(id='3g1jfi')

    submission.comments.replace_more(limit=None)
    for top_level_comment in submission.comments:
        print(top_level_comment.body)

if __name__ == '__main__':
    reddit = praw.Reddit(client_id='XXXX',
                         client_secret='XXXX',
                         user_agent='XXXX',
                         username='XXXX',
                         password='XXXXX')
    subreddit_scrape(reddit)
    # get_comments(reddit)


