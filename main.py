import config
import reddit_crawler
import argparse
import sqlite3

if __name__ == "__main__":
    db_conn = sqlite3.connect(config.COMMENT_DB)
    db_cursor = db_conn.cursor()

    db_conn.close()

    parser = argparse.ArgumentParser(
        description='A seq2seq comment generator trained on Reddit comments.')
    parser.add_argument('--crawl_sub', type=str,
                        help='Specify a subreddit to crawl. In order to crawl" \
                        "/r/sub" provide "sub" as an argument.')

    args = parser.parse_args()
    if args.crawl_sub:
        reddit_crawler.download_comments(args.crawl_sub)
