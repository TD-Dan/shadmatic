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
                        required_kwargs = ['id'], optional_kwargs = ['out']),
        ProgramCommand('get_comments',
                        required_kwargs = ['id'], optional_kwargs = ['out'])
    ]

    def load(self):
        super().load()
        self.twitlog = Log('twitter')
        try:
            import twitter
        except ModuleNotFoundError:
            self.twitlog.error("lib 'python_twitter' not found. Install with 'pip intall python_twitter' ")
            raise ModuleNotFoundError("lib 'python_twitter' not found. Install with 'pip intall python_twitter' ")
    
    def unload(self):
        super().unload()
        del self.twitlog
    
    def get_tweet(self, **kwargs):
        id = kwargs.get('id')
        out = kwargs.get('out')
        self.twitlog.info("Getting tweet "+id)
        self.twitlog.info("Outputting to "+out)
        pass
    
    def get_comments(self,**kwargs):
        id = kwargs.get('id')
        out = kwargs.get('out')
        self.twitlog.info("Getting comments for "+id)
        self.twitlog.info("Outputting to "+out)
        pass

#register to main program as a module
state.modules.append(TweetModule())