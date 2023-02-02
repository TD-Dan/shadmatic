"""Twitter integration
"""
from modules import ModuleBase
import state

from modules.log import Log

class TweetModule(ModuleBase):
    """Twitter integrations
    """
    name = "tweet"
    short = "tw"
    def load(self):
        super().load()
        log = Log('twitter')
        try:
            import twitter
        except ModuleNotFoundError:
            self.log.error("lib 'python_twitter' not found. Install with 'pip intall python_twitter' ")
            raise ModuleNotFoundError("lib 'python_twitter' not found. Install with 'pip intall python_twitter' ")
        pass

    def unload(self):
        super().unload()
        del self.log
    
    def exec(self, **kwargs):
        command = kwargs.get('command')
        match command:
            case 'get':
                print("Get: "+str(kwargs))

#register to main program as a module
state.modules.append(TweetModule())