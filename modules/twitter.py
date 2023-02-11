"""Twitter integration
"""
import time
import json

from modules import ModuleBase, fileio
from modules.command import ProgramCommand
import state

from modules.log import Log


class TweetModule(ModuleBase):
    """Twitter integration
    Allows fetching of tweets and comments from twitter and extracting addresses from them.
    """
    name = "twitter"
    short = "tw"
    client_as_app = None
    client_as_user = None

    commands = [
        ProgramCommand('get_tweet', help="Get a single tweet.",
                        required_kwargs = {'id':"Tweet ID (from twitter.com/<username>/status/<TWEET_ID>)"}, 
                        optional_kwargs = {'bearer':'Twitter bearer token. Default none, input will be requested from user.', 
                                           'out':"Output file name. Supported filetypes: .json . Default 'tweet.json'"}),
        ProgramCommand('get_comments', help="Get all comments of a tweet.",
                        required_kwargs = {'id':"Tweet ID (from twitter.com/<username>/status/<TWEET_ID>)"},
                        optional_kwargs = {'bearer':'Twitter bearer token. Default none, input will be requested from user.', 
                                           'out':"Output file name. Supported filetypes: .json . Default 'comments.json'"}),
        ProgramCommand('get_addresses', help="Collects and cleans up shimmer addresses from comments file.",
                        optional_kwargs = {'in':"Input file name. Supported filetypes: .json . Default 'comments.json'",
                                           'out':"Output file name. Supported filetypes: .json .txt . Default 'addresses.txt'"}),
        ProgramCommand('block_users', help="Blocks users.",
                        required_kwargs = {'users':"user id(s) / Input file name. ids can be single id or multiple ids separated with ';' (no space!).\
                                            Supported filetypes: .txt . Default none, input will be requested from user."},
                        optional_kwargs = {'consumer_key':'Twitter consumer key (aka. API key). Default none, input will be requested from user.', 
                                           'consumer_secret':'Twitter consumer key secret (aka. API secret). Default none, input will be requested from user.',
                                           'access_token':'Twitter access token (aka. authentication token). Default none, input will be requested from user.',
                                           'access_token_secret':'Twitter access secret (aka. authentication secret). Default none, input will be requested from user.'}),
    ]

    def load(self):
        super().load()
        self.twitlog = Log('twitter')
        try:
            import tweepy
        except ModuleNotFoundError:
            raise ModuleNotFoundError("lib 'tweepy' not found. Install with 'pip install tweepy' ")
        
    def open_twitter_api_as_app(self,bearer_token=None):
        if self.client_as_app:
            return
        else:
            try:
                import tweepy
            except ModuleNotFoundError:
                raise ModuleNotFoundError("lib 'tweepy' not found. Install with 'pip install tweepy' ")

            if not bearer_token:
                print("Input twitter bearer token:")
                bearer_token = input()

            self.client_as_app = tweepy.Client(bearer_token,return_type=dict)

    def open_twitter_api_as_user(self, consumer_key=None, consumer_secret=None, access_token=None, access_token_secret=None):
        if self.client_as_user:
            return
        else:
            try:
                import tweepy
            except ModuleNotFoundError:
                raise ModuleNotFoundError("lib 'tweepy' not found. Install with 'pip install tweepy' ")
            if not consumer_key:
                print("Input twitter consumer key:")
                consumer_key = input()
                print("Input twitter consumer secret:")
                consumer_secret = input()
                print("Input twitter access key:")
                access_token = input()
                print("Input twitter access secret:")
                access_token_secret = input()
                if not consumer_key or not consumer_secret or not access_token or not access_token_secret:
                    raise state.InvalidInput("Invalid credentials.")
                
            self.client_as_user = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret,
                                                access_token=access_token, access_token_secret=access_token_secret,
                                                return_type=dict)

    def unload(self):
        super().unload()
        del self.twitlog
    
    def get_tweet(self, **kwargs):
        bearer_token = kwargs.get('bearer')
        self.open_twitter_api_as_app(bearer_token=bearer_token)

        id = kwargs.get('id')
        out = kwargs.get('out',"tweet.json")
        self.twitlog.info("Getting tweet "+id)
        tweet = self.client_as_app.get_tweet(id)
        print(tweet)
        self.twitlog.info("Outputting to "+out)
        pass
    
    def get_comments(self,**kwargs):
        bearer_token = kwargs.get('bearer')
        self.open_twitter_api_as_app(bearer_token=bearer_token)

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
                    response = self.client_as_app.search_recent_tweets('in_reply_to_tweet_id:'+id, max_results=results_per_query, expansions='author_id', pagination_token=next_token)
                    replies+=response['data']
                else:
                    response = self.client_as_app.search_recent_tweets('in_reply_to_tweet_id:'+id, expansions='author_id', max_results=results_per_query)
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
        jsn_str = json.dumps(replies, indent=3,ensure_ascii=False)
        outfile = open(out,'w', encoding="utf-8")
        outfile.write(jsn_str)
        outfile.close()
    
    def get_addresses(self,**kwargs):
        in_str = kwargs.get('in',"comments.json")
        out_str = kwargs.get('out',"addresses.txt")
        
        infile = open(in_str,'r', encoding="utf-8")
        json_str = infile.read()
        infile.close()
        json_list = json.loads(json_str)

        self.twitlog.info('loaded '+str(len(json_list))+" comments from '"+in_str+"'")

        self.twitlog.info("Finding addresses...")

        all_authors = {} # as {'author'=[address, address..]}
        all_addresses = {} # as {'address'=[author, author..]}

        no_address_found = [] # in format [{entry}{entry}...]
        invalid_addresses = [] # in format [{entry}{entry}...]

        #construct a list of valid author and address entries
        for entry in json_list:
            author = entry['author_id']
            text:str = entry['text']
            words = text.split()
            address = None
            for word in words:
                if word.startswith("smr1"):
                    address = word
            if not address:
                no_address_found.append(entry)
                self.twitlog.warning("No address found in "+str(entry))
                continue
            if len(address) != 63:
                invalid_addresses.append(entry)
                self.twitlog.warning("Invalid address found in "+str(entry))
                continue        
            if not author in all_authors:
                all_authors[author] = [address]
            else:
                all_authors[author].append(address)

            if not address in all_addresses:
                all_addresses[address] = [author]
            else:
                all_addresses[address].append(author)

        print("found "+str(len(all_authors))+" unique authors with valid addresses")
        print("found "+str(len(all_addresses))+" unique addresses")

        #print(all_authors)
        #print(all_addresses)
        
        self.twitlog.info("Filtering addresses...")
        abuse_authors = []
        abuse_addresses = []
        clean_addresses = [] # in format [address,address,...]


        # filter out authors submitting multiple addresses and blacklist such authors
        for author in all_authors:
            if len(all_authors[author]) > 1:
                format_str = "author '"+author+"' submitted multiple addresses: "
                for addr in all_authors[author]:
                    format_str += addr+" "
                    abuse_addresses.append(addr)
                self.twitlog.warning(format_str)
                abuse_authors.append(author)
       
        # filter out multiple authors submitting same address and blacklist the authors
        for address in all_addresses:
            if len(all_addresses[address]) > 1:
                format_str = "address '"+address+"' submitted by multiple authors: "
                for auth in all_addresses[address]:
                    format_str += auth+" "
                    abuse_authors.append(auth)
                self.twitlog.warning(format_str)
                abuse_addresses.append(address)
            else:
                if all_addresses[address] in abuse_authors:
                    self.twitlog.warning("address author in abuse list, removing otherwice valid address.")
                else:
                    clean_addresses.append(address)
                
        self.twitlog.warning("Found "+str(len(abuse_authors))+" abusive users. Writing to abuse_users.txt.")
        fileio.write_list_to_file(abuse_authors, 'abuse_users.txt', confirm_overwrite=True, fail_silently=True)

        self.twitlog.warning("Found "+str(len(abuse_addresses))+" abused addresses. Writing to abuse_addresses.txt")
        fileio.write_list_to_file(abuse_addresses, 'abuse_addresses.txt', confirm_overwrite=True, fail_silently=True)

        try:
            fileio.write_list_to_file(clean_addresses, out_str, confirm_overwrite=True)
        except state.ProgramCancel:
            self.twitlog("File write aborted by user.")

        #idea: offer to block offending authors from twitter automatically
        #idea2: filter out bot entries by comparing old tweets. Flag all accounts posting more than n% addresses all the time


    def block_users(self,**kwargs):
        import tweepy
        users:str = kwargs.get('users')
        consumer_key = kwargs.get('consumer_key')
        consumer_secret = kwargs.get('consumer_secret')
        access_token = kwargs.get('access_token')
        access_token_secret = kwargs.get('access_token_secret')
        self.open_twitter_api_as_user(consumer_key=consumer_key, consumer_secret=consumer_secret,
                                                access_token=access_token, access_token_secret=access_token_secret,)

        if users.endswith(".txt"):
            users_list = fileio.read_list_from_file(users)
        else:
            users_list = users.split(';')
        for user in users_list:
            try:
                self.twitlog.info("Blocking user '"+user+"'")
                print("Blocking user '"+user+"'")
                response = self.client_as_user.block(user)
                print(response)
            except tweepy.Unauthorized:
                self.twitlog.error("Unauthorized credentials. Check your twitter api keys.")
                raise state.ProgramCancel()
        

#register to main program as a module
state.modules.append(TweetModule())