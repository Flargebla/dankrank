from urllib.parse import urlsplit

class Dank:

    # url - The URL that the image can be found at
    # filename - The filename of the image
    # updoots - The number of upvotes the Dank earned
    # score - The normalized score
    # subreddit - The subreddit where the Dank originated
    def __init__(self, url, upvotes, sub):
        self.url = url
        self.filename = urlsplit(self.url)[2].split('/')[-1]
        self.updoots = upvotes
        self.subreddit = sub
        self.score = self.__calculate_score()

    # Calculate the Dank score
    def __calculate_score(self):
        return self.updoots / self.subreddit.subscribers

