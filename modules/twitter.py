"""Twitter integration
"""
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

    commands = [
        ProgramCommand('get_tweet',
                        required_kwargs = {'id':"Tweet ID (from twitter.com/<username>/status/<TWEET_ID>)"}, optional_kwargs = {'out':'Output file name. Supported filetypes: .json'}),
        ProgramCommand('get_comments',
                        required_kwargs = {'id':"Tweet ID (from twitter.com/<username>/status/<TWEET_ID>)"}, optional_kwargs = {'out':'Output file name. Supported filetypes: .json .txt'})
    ]

    def load(self):
        super().load()
        self.twitlog = Log('twitter')
        try:
            import tweepy
        except ModuleNotFoundError:
            raise ModuleNotFoundError("lib 'tweepy' not found. Install with 'pip install tweepy' ")
        oauth1_user_handler = tweepy.OAuth1UserHandler(
        "Pdsqcs5dCE1ux7VqbyibmAPv7", "ieWK0c8aRnonhbMIVbhtekJPMdZfZDGbzQZklQcZxrQc71dx4v",
        callback="oob"
        )
        print(oauth1_user_handler.get_authorization_url())
        
        verifier = input("Input PIN: ")
        access_token, access_token_secret = oauth1_user_handler.get_access_token(
            verifier
        )

        print(access_token)
        print(access_token_secret)
    
    def unload(self):
        super().unload()
        del self.twitlog
    
    def get_tweet(self, **kwargs):
        id = kwargs.get('id')
        out = kwargs.get('out',"tweet.json")
        self.twitlog.info("Getting tweet "+id)
        self.twitlog.info("Outputting to "+out)
        pass
    
    def get_comments(self,**kwargs):
        id = kwargs.get('id')
        out = kwargs.get('out',"comments.json")
        self.twitlog.info("Getting comments for "+id)
        self.twitlog.info("Outputting to "+out)
        pass

#register to main program as a module
state.modules.append(TweetModule())