import secret
import praw
import argparse


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

    for submission in reddit.subreddit(sub).hot(limit=10): # TODO: adjust the limit=10 part
        print("Title: %s" % submission.title)
        submission.comments.replace_more(limit=0) # TODO: Adjust replace_more
        for top_level_comment in submission.comments:
            iterate_inorder(top_level_comment, save_comment)

def iterate_inorder(tree, func):
    """Preform an inorder tree traversal and apply a function to each node.

    Keyword arguments:
    tree -- the data tree
    func -- the function to apply to each entry
    """
    # TODO: Write the iteration loop.
    pass

def save_comment(comment):
    """Save a comment to the database specified in config.py.

    Keyword arguments:
    comment -- the comment to save
    """
    # TODO: Write save function.
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='A seq2seq comment generator trained on Reddit comments.')
    parser.add_argument('--crawl_sub', type=str,
                        help='Specify a subreddit to crawl. In order to crawl" \
                        "/r/sub" provide "sub" as an argument.')

    args = parser.parse_args()
    print(args.crawl_sub)
