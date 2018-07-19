import praw
import secret
import config
import sqlite3


def download_comments(sub="all", submission_norepeat=True):
    """
    Crawl a subredddit and store comment trees.

    Args:
        sub: the subreddit to crawl (default "all")
        submission_norepeat: if set to true all submissions will only
                             be processed once

    Returns:
        None

    Raises:
        None
    """
    db_conn = sqlite3.connect(config.COMMENT_DB)
    db_cursor = db_conn.cursor()

    db_cursor.execute(
        "create table if not exists comments"
        "(reddit_id not null unique, parent, body)"
    )

    db_cursor.execute(
        "create table if not exists posts"
        "(reddit_id not null unique)"
    )

    reddit = praw.Reddit(client_id=secret.API_KEY,
                         client_secret=secret.API_SECRET,
                         user_agent=secret.USER_AGENT,
                         username=secret.USERNAME,
                         password=secret.PASSWORD)

    def save_comment(comment, parent_id):
        db_cursor.execute(
            "insert into comments (reddit_id, body, parent)"
            "values (?, ?, ?)",
            (comment.id, comment.body, parent_id)
        )

    def traverse_comment_tree(comment, parent_id):
        if comment:
            save_comment(comment, parent_id)
            for reply in comment.replies:
                traverse_comment_tree(reply, comment.id)

    def is_new_submission(submssion):
        db_cursor.execute(
            "select * from posts where reddit_id = (?)", (submission.id,))
        if len(db_cursor.fetchall()) > 0:
            return False
        else:
            db_cursor.execute(
                "insert into posts (reddit_id) values (?)", (submission.id,))
            db_conn.commit()
            return True

    for submission in reddit.subreddit(sub).hot(limit=None):
        if submission_norepeat:
            if not is_new_submission(submission):
                continue
        submission.comments.replace_more(limit=None)
        for top_level_comment in submission.comments:
            traverse_comment_tree(top_level_comment, None)
        db_conn.commit()
    db_conn.close()


def comment_reply_pairs():
    """
    Retrieve comments and replies to them from the local storage.

    Args:
        None

    Returns:
        An iterator of tuples (comment, reply)

    Raises:
        None
    """
    with sqlite3.connect(config.COMMENT_DB) as db_conn:
        db_cursor = db_conn.cursor()
        db_cursor.execute(
            "select a.body, b.body "
            "from comments as a "
            "inner join "
            "(select * from comments where parent is not null) b "
            "on a.reddit_id = b.parent")
        return db_cursor
