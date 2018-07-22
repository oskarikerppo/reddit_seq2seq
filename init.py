import re
import os
import argparse


def init_creds():
    user = input("Reddit username: ")
    passwd = input("Reddit password: ")
    api_key = input("API key: ")
    api_secret = input("API secret: ")
    with open("secret.py", "w") as f:
        s = 'USERNAME = "%s" \n' \
            'PASSWORD = "%s" \n' \
            'USER_AGENT = "asd" \n' \
            'API_KEY = "%s" \n' \
            'API_SECRET = "%s"\n' % (user, passwd, api_key, api_secret)
        f.write(s)


def init_config():
    with open("config.py", "r") as f:
        s = f.read()
        root_dir = os.path.abspath(".")
        s = re.sub(r"ROOT_DIR = \"(.*?)\"", "ROOT_DIR = \"%s\"" % root_dir, s)
        with open("config.py", "w") as g:
            g.write(s)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Initialization script for reddit_seq2seq')
    parser.add_argument('--config_only', action="store_true",
                        help='if provided, secret.py won\'t be initialized')

    args = parser.parse_args()

    if not args.config_only:
        init_creds()
    init_config()
