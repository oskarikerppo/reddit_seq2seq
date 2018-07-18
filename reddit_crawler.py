import praw
import secret


def download_comments(db_conn, db_cursor, sub="all"):
    """Crawl a subredddit and store comment trees.

    Keyword arguments:
    sub -- the subreddit to crawl (default "all")
    """
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

    def iterate_comment_tree(comment, parent_id):
        if comment:
            save_comment(comment, parent_id)
            for reply in comment.replies:
                iterate_comment_tree(reply, comment.id)

    # TODO: adjust the limit=10 part
    for submission in reddit.subreddit(sub).hot(limit=10):
        submission.comments.replace_more(limit=None)
        for top_level_comment in submission.comments:
            iterate_comment_tree(top_level_comment, None)
        db_conn.commit()
