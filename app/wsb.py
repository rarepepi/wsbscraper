import asyncio
import asyncpraw
import time
from asyncpraw.models import MoreComments
import os
from collections import Counter
import config
from utils import clean_comment, clean_submission
import pandas as pd


async def reddit_instance():
    """
    Return instance of Reddit
    """
    reddit = asyncpraw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'), client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT'),
    )
    return reddit

async def subreddit_type_submissions(sub="wallstreetbets", kind="new"):
    """
    """
    comments = []
    articles = []
    red = await reddit_instance()
    subreddit = await red.subreddit(sub)
    if kind == "hot":
        submissions = subreddit.hot()
    elif kind == "top":
        submissions = subreddit.top()
    elif kind == "new":
        submissions = subreddit.new()
    elif kind == "random_rising":
        submissions = subreddit.random_rising()
    else:
        submissions = subreddit.random()

    async for submission in submissions:
        article = clean_submission(submission)
        article['subreddit'] = sub

        articles.append(article)

        top_level_comments = await submission.comments()
        print(f"📗 Looking at submission: {article['title'][:40]}...")
        for top_level_comment in top_level_comments:
            if isinstance(top_level_comment, MoreComments):
                continue
            comment = clean_comment(top_level_comment)
            print(f"🗯️ ... {comment['author']} said {comment['body'][:40]}")
            comment['article_id'] = article['id']
            comments.append(comment)

    return (articles, comments)


async def data_for_subreddit(sub, kind):
    """
    """
    data = await subreddit_type_submissions(sub, kind)
    return data


def filter_by_tickers(comment):
    tickers = ["GME", "AMC", "NOK", "SLV", "SPCE",
            "TSLA", "PLTR", "TELL", "HUGE", "CAT", "RIOT"]
    mentions = []
    for tick in tickers:
        if tick in comment:
            mentions.append(tick)
    if len(mentions) > 0:
        return mentions
    else:
        return None

async def get_data_frame():
    tic = time.perf_counter()
    assert os.getenv('REDDIT_CLIENT_ID') is not None
    kinds = ['hot', 'new', 'top']
    articles, comments = await data_for_subreddit('wallstreetbets', 'hot')
    articles_df = pd.DataFrame(articles)
    comments_df = pd.DataFrame(comments) 
    toc = time.perf_counter()
    print(f"{toc - tic:0.4f} seconds")
    return (articles_df, comments_df)

async def main():
    tic = time.perf_counter()
    assert os.getenv('REDDIT_CLIENT_ID') is not None
    kinds = ['hot', 'new', 'top']
    # task = asyncio.createTask(data_for_subreddit('wallstreetbets', 'hot'))
    # done, pending = await task()
    # if done:
    #     print(done)
    # data = await asyncio.gather(*[data_for_subreddit('wallstreetbets', f"{kind}") for kind in kinds])

    comments = data[0][1]
    raw_comments_list = [(c['body'], c['ups']) for c in comments]
    tickers = []
    for comment in raw_comments_list:
        filtered = filter_by_tickers(comment[0])
        if filtered is not None:
            for f in filtered:
                tickers.append(f)
    print(f"looked through {len(raw_comments_list)} total comments and found {len(tickers)} ticker symbols")
    print(Counter(tickers))
    toc = time.perf_counter()
    print(f"{toc - tic:0.4f} seconds")

