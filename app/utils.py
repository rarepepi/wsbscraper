
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
