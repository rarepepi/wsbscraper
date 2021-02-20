import asyncio
import asyncpraw
import time
from asyncpraw.models import MoreComments
import os
from collections import Counter


async def reddit_instance():
    """
    Return instance of Reddit
    """
    reddit = asyncpraw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'), client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT'),
    )
    return reddit


def clean_submission(submission):
    """
    Take Reddit submission and turn into dictionary
    """
    try:
        submission_author = submission.author.name
    except:
        submission_author = "None"
    data = {
        "id": submission.id,
        "title": submission.title,
        "score": submission.score,
        "url": submission.url,
        "name": submission.name,
        "author": submission_author,
        "is_video": submission.is_video,
        "selftext": submission.selftext,
        "shortlink": submission.shortlink,
        "subreddit_subscribers": submission.subreddit_subscribers,
        "thumbnail": submission.thumbnail,
        "ups": submission.ups,
        "downs": submission.downs,
        "created": submission.created
    }

    for k, v in data.items():
        if v == "":
            data[k] = "None"
    return data


def clean_comment(comment):
    """
    Clean the comment
    """
    try:
        name = comment.author.name
    except:
        name = "None"

    data = {
        "author": name,
        "body": comment.body,
        "ups": comment.ups,
        "fullname": comment.fullname
    }

    for k, v in data.items():
        if v == "":
            data[k] = "None"
    return data


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


async def main():
    tic = time.perf_counter()
    assert os.getenv('REDDIT_CLIENT_ID') is not None
    kinds = ['hot', 'new', 'top']
    data = await asyncio.gather(*[data_for_subreddit('wallstreetbets', f"{kind}") for kind in kinds])

    comments = data[0][1]
    raw_comments_list = [(c['body'], c['ups']) for c in comments]
    tickers = []
    for comment in raw_comments_list:
        filtered = filter_by_tickers(comment[0])
        if filtered is not None:
            for f in filtered:
                tickers.append(f)
    print(f"looked through {len(raw_comments_list)} total comments and found {len(tickers)} ticker symbols")
    return(Counter(tickers))
    toc = time.perf_counter()
    print(f"{toc - tic:0.4f} seconds")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    try:
        loop.run_forever()
    finally:
        loop.close()
