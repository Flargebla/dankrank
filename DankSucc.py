import praw, os, requests, datetime, json, logging, threading, urllib.parse
from Dank import Dank
from io import open as iopen
from multiprocessing.pool import ThreadPool
from time import sleep

class DankSucc:

    # reddit - The Reddit API Instance for accessing Reddit data
    # subreddits - The subtreddits that will be pulled from
    # danks - The list of Danks that were succ'd
    # dps - The Dos, anks per subreddit to succ
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
            danks = self.reddit.subreddit(sr).search(query="",time_filter="day")
            for dank in danks:
                time_made = datetime.datetime.fromtimestamp(dank.created)
                earliest_time = datetime.datetime.now() - datetime.timedelta(hours=4)
                if time_made < earliest_time:
                    while threading.active_count() > 15:
                        self.logger.info("ThreadPool is full... waiting")
                        sleep(0.5)
                    self.logger.info("Processing a post: <"+dank.url+", "+str(dank.ups)+">")
                    t = threading.Thread(target=self.__grab_dank, args=(dank,sr,time_made))
                    threads.append(t)
                    t.start()
                else:
                    self.logger.info("A dank has been deemed unripe")
        self.logger.info("Waiting for all threads to finish")
        for thread in threads:
            thread.join()
        self.logger.info("Succing complete")
        self.calculate_scores()

    # Save all the pulled Danks to disk
    def persist(self):
        self.logger.info("Starting the persist()")
        for d in self.danks:
            img_req = requests.get(d.url)
            if img_req.status_code == requests.codes.ok:
                try:
                    with iopen("danks/"+d.filename, 'wb') as f:
                        f.write(img_req.content)
                except PermissionError:
                    self.logger.info("PermissionError: Failed to write")
                    self.kill_dank(d)
            else:
                self.logger.info("Failed to grab image from: "+d.url)
        self.logger.info("Persisting complete")

    # Remove a dank from both the list and disk
    def kill_dank(self, dank):
        self.logger.info("Killing a dank: "+dank.url)
        self.danks.remove(dank)
        os.remove("danks/"+dank.filename)

    # Calculate post scores
    def calculate_scores(self):
        max_score = max([d.score for d in self.danks])
        min_score = min([d.score for d in self.danks])
        scale = 100 / (max_score-min_score)
        for d in self.danks:
            d.score = d.score * scale

    # Create a Dank and pull the image
    def __grab_dank(self, dank, sr, time_posted):
        d = Dank(dank.url, dank.ups, self.reddit.subreddit(sr), time_posted)
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
        
