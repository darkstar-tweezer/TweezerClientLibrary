## Introduction

Tweezer provides APIs to scrape data from web pages.

1. `Twitter Advanced Search`: Allows you to scrape tweets returned from twitter advanced search.

## Quick Start

Say you want to scrape tweets using the twitter advanced search.

### Construct your search URL

1. Go to twitter [advanced search](https://twitter.com/search-advanced) in your favorite browser, construct your search query and hit `search`.
2. Copy over the URL generated.
3. Replace the `twitter.com` with `dark-tweezer.herokuapp.com`.

For example, 

`My twitter URL`: <https://twitter.com/search?l=en&q=%40RickAndMorty%20since%3A2019-01-01%20until%3A2019-07-13&src=typd>

`Modified URL`: <https://dark-tweezer.herokuapp.com/search?l=en&q=%40RickAndMorty%20since%3A2019-01-01%20until%3A2019-07-13&src=typd>

### Download tweets from browser

Paste the `Modified URL` from the above step into your broswer and wait for the download to complete. 

You should have a file called `tweets.json` in your downloads directory.

### Download/view tweets from CLI

Assuming you have [curl](https://curl.haxx.se/download.html) installed.

**Download to a file**

```bash
$ curl "https://dark-tweezer.herokuapp.com/search?l=en&q=%40RickAndMorty%20since%3A2019-01-01%20until%3A2019-07-13&src=typd" -o pickle_rick.json
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 4179k    0 4179k    0     0   152k      0 --:--:--  0:00:27 --:--:--  134k

$ less pickle_rick.json
[
{"id":1130315793994899457,"text":"Today was a lay in bed and read day, punctuated by naps and some episodes of @RickandMorty. Also I slept with this book under my pillow at some points for, you know, osmosis pic.twitter.com/KvEP9UIgqy","lang":"en","username":"RicciFlat","time":"2019-05-20 03:34:20","permalink":"https://twitter.com/RicciFlat/status/1130315793994899457","is_reply":false,"parent_id":null,"replies":1,"retweets":1,"favorites":5},
{"id":1130508514173104131,"text":"I see you, Google. @Google @RickandMorty pic.twitter.com/Aq7B6wxIR9","lang":"en","username":"hollymonkster","time":"2019-05-20 16:20:08","permalink":"https://twitter.com/hollymonkster/status/1130508514173104131","is_reply":false,"parent_id":null,"replies":0,"retweets":0,"favorites":0},
{"id":1130317185551884289,"text":"Now that #GameOfThrones is over I can\u2019t wait for @RickandMorty pic.twitter.com/TnTk5H7tRa","lang":"en","username":"kramsta1","time":"2019-05-20 03:39:51","permalink":"https://twitter.com/kramsta1/status/1130317185551884289","is_reply":false,"parent_id":null,"replies":0,"retweets":0,"favorites":1},
{"id":1130264590498111493,"text":"Drake and Josh is trending!? Let's get @DrakeBell & @ItsJoshPeck to notice my rendition of their hit tv show's theme song. RT, LIKE & @ Drake & Josh let's make this go viral @RickandMorty \n\nSong: https://soundcloud.com/afrodope/girl-next-door-prod\u00a0\u2026\nArtist: @malcolmflexedpic.twitter.com/QdfqnTb0nc","lang":"en","username":"chiefmemelord","time":"2019-05-20 00:10:52","permalink":"https://twitter.com/chiefmemelord/status/1130264590498111493","is_reply":false,"parent_id":null,"replies":0,"retweets":0,"favorites":0},
{"id":1130575520234651648,"text":"Counting the days! @RickandMorty pic.twitter.com/iW15qKCVni","lang":"en","username":"nalhilal","time":"2019-05-20 20:46:23","permalink":"https://twitter.com/nalhilal/status/1130575520234651648","is_reply":false,"parent_id":null,"replies":0,"retweets":0,"favorites":1},
...
...
]

$ cat pickle_rick.json | wc -l
11816

# This means we have `11814` tweets. 1 line for list start and 1 for list end.
```

**Just view tweets**

```bash
$ curl "https://dark-tweezer.herokuapp.com/search?l=en&q=%40RickAndMorty%20since%3A2019-01-01%20until%3A2019-07-13&src=typd"
[
{"id":1125083484425478145,"text":"Wait, Rick can actually be outsmarted? #RickandMorty @RickandMorty @AdultSwimUKpic.twitter.com/2iYLOWKsAy","lang":"en","username":"E4Tweets","time":"2019-05-05 17:03:00","permalink":"https://twitter.com/E4Tweets/status/1125083484425478145","is_reply":false,"parent_id":null,"replies":0,"retweets":0,"favorites":5},
{"id":1124957464137490432,"text":"Mr. Smith from the Matrix is like Mr. Meeseeks from @RickandMorty pic.twitter.com/BbIH0EGaNN","lang":"en","username":"TheVibeDealer3","time":"2019-05-05 08:42:14","permalink":"https://twitter.com/TheVibeDealer3/status/1124957464137490432","is_reply":false,"parent_id":null,"replies":0,"retweets":0,"favorites":2},
{"id":1125162848357888001,"text":"Ummm... This is outside my CVS!?\n#RickAndMorty @RickandMorty pic.twitter.com/lXVsJZSrEm","lang":"en","username":"Forest__Corgi","time":"2019-05-05 22:18:22","permalink":"https://twitter.com/Forest__Corgi/status/1125162848357888001","is_reply":false,"parent_id":null,"replies":0,"retweets":0,"favorites":4},
...
...
]
```

## APIs in code

### Search with Python: >= 3.6

```python
from aiohttp import ClientSession
from aiohttp.client import ClientTimeout
from asyncio import get_event_loop
from time import time
from tweezer.client import search

# Default timeout is 5 min.
# For long scraping tasks this is not enough.
_TIMEOUT = ClientTimeout(total=(15*60))


async def main():
    # Search parameters.
    search_params = {"date": ["2019-01-01", "2019-07-13"],
                     "lang": "en", 
                     "mention": ["RickAndMorty"]}

    # Use the client session to make requests to tweezer.
    async with ClientSession(timeout=_TIMEOUT) as session:
        # Just cause you like me is interested in performance
        start_time = time()
        total_tweets = 0

        # Print out all the tweets that is being returned back from the server
        async for tweet in search(session, search_params):
            total_tweets += 1

            # Do your thing with the tweet
            print(f"Received: {tweet}")

        total_time = time() - start_time

        print(f"Total tweets received: {total_tweets}")
        print(f"Total time:            {total_time:4.2f} s")
        print(f"Tweets per second:     {(total_tweets / total_time):4.2f} tps")

if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(main())
    
```

**Result**

```text
Received: Tweet(id=1092498190866075649, text="Shout out to the #fisforfamily &  #RickandMorty fans for all of the love you guys sent my way because of my comic mash-up! You're all hella cool & really motivating! @FIFFNetflix @RickandMorty pic.twitter.com/1JPgtvjqKr", lang='en', username='nadiareddyart', time='2019-02-04 19:00:40', permalink='https://twitter.com/nadiareddyart/status/1092498190866075649', is_reply=False, parent_id=None, replies=0, retweets=1, favorites=1)
Received: Tweet(id=1092292469536911360, text='4 dabs later now ready for bed and some @RickandMorty', lang='en', username='Dazed_Jedii', time='2019-02-04 05:23:13', permalink='https://twitter.com/Dazed_Jedii/status/1092292469536911360', is_reply=False, parent_id=None, replies=0, retweets=0, favorites=0)
...
...
Received: Tweet(id=1148623751661129728, text='', lang='und', username='mrsandeo', time='2019-07-09 16:03:37', permalink='https://twitter.com/mrsandeo/status/1148623751661129728', is_reply=True, parent_id=1148623599458234370, replies=0, retweets=0, favorites=1)
Received: Tweet(id=1148467129491963904, text='Para mí si, creo xd', lang='es', username='infernu91419148', time='2019-07-09 05:41:15', permalink='https://twitter.com/infernu91419148/status/1148467129491963904', is_reply=True, parent_id=1148067952496742401, replies=1, retweets=0, favorites=2)
Total tweets received: 11828
Total time:            27.53 s
Tweets per second:     429.64 tps
```

## NOTE

Both the client library and the tweezer URL are solely for my use. **You may not use it**. This is just a personal project in my search for fast html parsing. All of this is run on a single thread with a max of 500MB RAM.
