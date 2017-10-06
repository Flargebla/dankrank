import praw, requests, json
from Dank import Dank
from io import open as iopen

class DankSucc:

    # reddit - The Reddit API Instance for accessing Reddit data
    # subreddits - The subtreddits that will be pulled from
    # danks - The list of Danks that were succ'd
    # dps - The Danks per subreddit to succ
    def __init__(self, subreddit_string, dps=50):
        self.subreddits = [sr for sr in subreddit_string.split(",")]
        self.danks = []
        self.dps = dps
        with open("creds.json") as cfg:
            self.config = json.load(cfg)
        self.reddit = self.__init_reddit()

    # Pull all images and upvote data from Reddit
    def succ(self):
        for sr in self.subreddits:
            danks = self.reddit.subreddit(sr).hot(limit=self.dps)
            for dank in danks:
                d = Dank(dank.url, dank.ups, self.reddit.subreddit(sr))
                self.danks.append(d)

    # Save all the pulled Danks to disk
    def persist(self):
        for d in self.danks:
            img_req = requests.get(d.url)
            if img_req.status_code == requests.codes.ok:
                with iopen("danks/"+d.filename, 'wb') as f:
                    f.write(img_req.content)

    # Return the list of currently held Danks
    def grab_danks(self):
        return self.danks


    # Initialize the Reddit instance
    def __init_reddit(self):
        reddit_cfg = self.config["reddit"]
        return praw.Reddit(**reddit_cfg)
        
