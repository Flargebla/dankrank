from urllib.parse import urlsplit
import logging

class Dank:

    # url - The URL that the image can be found at
    # filename - The filename of the image
    # updoots - The number of upvotes the Dank earned
    # score - The normalized score
    # subreddit - The subreddit where the Dank originated
    # filetype - The type of the image file
    def __init__(self, url, upvotes, sub, created):
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s %(levelname)s %(message)s",
                            filename="debugging.log",
                            filemode="w")
        self.logger = logging.getLogger("Dank")
        self.url = url
        self.created_at = created
        self.filename = urlsplit(self.url)[2].split('/')[-1]
        self.updoots = upvotes
        self.subreddit = sub
        self.score = self.__calculate_initial_score()
        self.filetype = self.__detect_filetype()

    # Calculate the initial score
    def __calculate_initial_score(self):
        return self.updoots / self.subreddit.subscribers

    # Determine the filetype
    def __detect_filetype(self):
        return self.filename.split(".")[-1].upper()
