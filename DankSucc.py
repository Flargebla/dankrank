import praw, requests, json, time, logging, threading, urllib.parse
from Dank import Dank
from io import open as iopen
from multiprocessing.pool import ThreadPool

class DankSucc:

    # reddit - The Reddit API Instance for accessing Reddit data
    # subreddits - The subtreddits that will be pulled from
    # danks - The list of Danks that were succ'd
    # dps - The Danks per subreddit to succ
    def __init__(self, subreddit_string):
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s %(levelname)s %(message)s",
                            filename="debugging.log",
                            filemode="w")
        self.logger = logging.getLogger("DankRank")
        self.subreddits = [sr for sr in subreddit_string.split(",")]
        self.danks = []
        self.logger.info("Loading credentials")
        with open("creds.json") as cfg:
            self.config = json.load(cfg)
        self.reddit = self.__init_reddit()

    # Pull all images and upvote data from Reddit
    def succ(self):
        self.logger.info("Starting the succ()")
        threads = []
        for sr in self.subreddits:
            self.logger.info("Pulling from: r/"+sr)
            danks = self.reddit.subreddit(sr).search(query="",time_filter="hour")
            for dank in danks:
                while threading.active_count() > 20:
                    self.logger.info("ThreadPool is full... waiting")
                    time.sleep(0.5)
                self.logger.info("Processing a post: <"+dank.url+", "+str(dank.ups)+">")
                t = threading.Thread(target=self.__grab_dank, args=(dank,sr,))
                threads.append(t)
                t.start()
        for thread in threads:
            thread.join()

    # Save all the pulled Danks to disk
    def persist(self):
        self.logger.info("Starting the persist()")
        for d in self.danks:
            img_req = requests.get(d.url)
            if img_req.status_code == requests.codes.ok:
                with iopen("danks/"+d.filename, 'wb') as f:
                    f.write(img_req.content)

    # Create a Dank and pull the image
    def __grab_dank(self, dank, sr):
        d = Dank(dank.url, dank.ups, self.reddit.subreddit(sr))
        self.danks.append(d)

    # Return the list of currently held Danks
    def grab_danks(self):
        return self.danks

    # Validate a Dank
    def __is_valid_dank(self, dank):
        valid_types = ["jpg","png","gif","svg"]
        filename = (urllib.parse.urlsplit(dank.url)[2].split('/')[-1])
        extension = filename.split(".")[-1].lower()
        if extension in filename:
            return True
        else:
            self.logger.info("Invalid extension identified: "+extension)
            return False

    # Initialize the Reddit instance
    def __init_reddit(self):
        reddit_cfg = self.config["reddit"]
        self.logger.info("Creating a Reddit instance with: "+str(reddit_cfg))
        return praw.Reddit(**reddit_cfg)
        
