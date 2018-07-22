def init():
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


if __name__ == "__main__":
    init()
