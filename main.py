import config
import reddit_crawler
import argparse
import sqlite3

if __name__ == "__main__":
    db_conn = sqlite3.connect(config.COMMENT_DB)
    db_cursor = db_conn.cursor()

    db_conn.close()

    example_text = '''
examples:

    python main.py --crawl_sub dankmemes --crawl_limit 10
    '''

    parser = argparse.ArgumentParser(
        description='A seq2seq comment generator trained on Reddit comments.',
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--crawl_sub', metavar="sub", type=str,
                        help='the subreddit to crawl (all by default)')
    parser.add_argument('--crawl_limit', metavar="n", type=int,
                        help='the number of posts to process '
                        '(unlimited by default)')

    args = parser.parse_args()
    if args.crawl_sub:
        if args.crawl_limit:
            reddit_crawler.download_comments(sub=args.crawl_sub,
                                             crawl_limit=args.crawl_limit)
        else:
            reddit_crawler.download_comments(args.crawl_sub)
