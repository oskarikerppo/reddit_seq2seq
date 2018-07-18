import secret
import config
import praw
import argparse
import sqlite3

db_conn, db_cursor = None, None


def download_comments(sub="all"):
    """Crawl a subredddit and store comment trees.

    Keyword arguments:
    sub -- the subreddit to crawl (default "all")
    """
    # Log in
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


if __name__ == "__main__":
    db_conn = sqlite3.connect(config.COMMENT_DB)
    db_cursor = db_conn.cursor()
    db_cursor.execute(
        "create table if not exists comments "
        "(reddit_id text,"
        "body text,"
        "parent integer)"
    )

    parser = argparse.ArgumentParser(
        description='A seq2seq comment generator trained on Reddit comments.')
    parser.add_argument('--crawl_sub', type=str,
                        help='Specify a subreddit to crawl. In order to crawl" \
                        "/r/sub" provide "sub" as an argument.')

    args = parser.parse_args()
    if args.crawl_sub:
        download_comments(args.crawl_sub)

    db_conn.close()
