# reddit_seq2seq
A seq2seq RNN trained on Reddit comments.

## Getting started

1. Install the dependencies.
2. Run `init.py` and provide your credentials.
You need to obtain valid credentials by [creating a Reddit account](https://www.reddit.com/login) and
[creating a Reddit app](https://github.com/reddit-archive/reddit/wiki/OAuth2).

3. Run `python main.py --crawl_sub [sub]` to crawl the subreddit `[sub]` and start storing the comment trees for training.
