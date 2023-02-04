"""Twitter integration
"""
import time
import json

from modules import ModuleBase
from modules.command import ProgramCommand
import state

from modules.log import Log


class TweetModule(ModuleBase):
    """Twitter integration
    Allows fetching of tweets and comments from twitter and extracting addresses from them.
    """
    name = "twitter"
    short = "tw"
    api = None
    commands = [
        ProgramCommand('get_tweet',
                        required_kwargs = {'id':"Tweet ID (from twitter.com/<username>/status/<TWEET_ID>)"}, 
                        optional_kwargs = {'bearer':'Twitter bearer token', 
                                           'out':'Output file name. Supported filetypes: .json'}),
        ProgramCommand('get_comments',
                        required_kwargs = {'id':"Tweet ID (from twitter.com/<username>/status/<TWEET_ID>)"},
                        optional_kwargs = {'bearer':'Twitter bearer token', 
                                           'out':'Output file name. Supported filetypes: .json .txt'})
    ]

    def load(self):
        super().load()
        self.twitlog = Log('twitter')
        try:
            import tweepy
        except ModuleNotFoundError:
            raise ModuleNotFoundError("lib 'tweepy' not found. Install with 'pip install tweepy' ")
        
    def open_twitter_api(self,bearer=None):
        if self.api:
            return
        else:
            try:
                import tweepy
            except ModuleNotFoundError:
                raise ModuleNotFoundError("lib 'tweepy' not found. Install with 'pip install tweepy' ")
            if bearer:
                bearer_token = bearer
            else:
                print("Input twitter bearer token:")
                bearer_token = input()

            self.api = tweepy.Client(bearer_token,return_type=dict)

    def unload(self):
        super().unload()
        del self.twitlog
    
    def get_tweet(self, **kwargs):
        bearer_token = kwargs.get('bearer')
        self.open_twitter_api(bearer=bearer_token)

        id = kwargs.get('id')
        out = kwargs.get('out',"tweet.json")
        self.twitlog.info("Getting tweet "+id)
        tweet = self.api.get_tweet(id)
        print(tweet)
        self.twitlog.info("Outputting to "+out)
        pass
    
    def get_comments(self,**kwargs):
        bearer_token = kwargs.get('bearer')
        self.open_twitter_api(bearer=bearer_token)

        import tweepy

        id = kwargs.get('id')
        out = kwargs.get('out',"comments.json")
        self.twitlog.info("Getting comments for "+id)
        next_token = None
        results_per_query = 100
        max_queries = 100
        replies = None
        for qn in range(0, max_queries):
            try:
                if next_token:
                    response = self.api.search_recent_tweets('in_reply_to_tweet_id:'+id, max_results=results_per_query, expansions='author_id', pagination_token=next_token)
                    replies+=response['data']
                else:
                    response = self.api.search_recent_tweets('in_reply_to_tweet_id:'+id, expansions='author_id', max_results=results_per_query)
                    replies = response['data']
                meta = response['meta']

                got_str = "Query nr."+str(qn)+", total tweets fetched: "+str(len(replies))
                self.twitlog.info(got_str)
                print(got_str)
                if qn==0:
                    print(replies[0]['id']+": "+replies[0]['text'])
                print("...")
                print(replies[-1]['id']+": "+replies[-1]['text'])
                try:
                    next_token = meta['next_token']
                except KeyError:
                    print("End of results.")
                    break
            except tweepy.errors.TooManyRequests:
                print("Too many requests. Waiting for 1 min. (Ctrl-C to cancel)")
                step=5
                for n in range(0,60,step):
                    print("."+str(n), end='')
                    time.sleep(step)
        

        self.twitlog.info("Outputting to "+out)
        jsn_str = json.dumps(replies, indent=3)
        outfile = open(out,'w')
        outfile.write(jsn_str)
        outfile.close()

#register to main program as a module
state.modules.append(TweetModule())