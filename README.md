## Introduction

Tweezer provides APIs to generate data sets.

1. `Twitter Advanced Search`: Allows you to scrape tweets returned from twitter advanced search.

## Quick Start

Say you want to scrape tweets using the twitter advanced search.

### Get your license key

Note, if you do not have a license key, you will probably never get one. Please do not request me for one.
Even if I end up seeing your email (I won't), I will ignore it.

`LICENSE_KEY`: "XXX"

### Construct your search URL

1. Go to [twitter advanced search](https://twitter.com/search-advanced), construct your search query and hit `search`.
2. Copy over the URL generated.
3. Replace the `twitter.com` with `dark-tweezer.herokuapp.com`.
4. Add you license key to the end of the url. Like this: `&k=LICENSE_KEY`

For example, 

`Twitter URL`: <https://twitter.com/search?l=en&q=%40RickAndMorty%20since%3A2019-01-01%20until%3A2019-07-13&src=typd>

`Modified URL`: <https://dark-tweezer.herokuapp.com/search?l=en&q=%40RickAndMorty%20since%3A2019-01-01%20until%3A2019-07-13&src=typd&k=XXX>

### Download tweets from browser

Paste the `Modified URL` from the above step into your broswer and wait for the download to complete. 

You should have a file called `tweets.json` in your downloads directory.

### Download tweets from CLI

Assuming you have [curl](https://curl.haxx.se/download.html) installed. You can really use other similar tool.

**Download to a file**

```bash
$ curl "https://dark-tweezer.herokuapp.com/search?l=en&q=%40RickAndMorty%20since%3A2019-01-01%20until%3A2019-07-13&src=typd&k=XXX" -o tweets.json
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 4179k    0 4179k    0     0   152k      0 --:--:--  0:00:27 --:--:--  134k
```

### Example contents of tweets.json

```javascript
[{
        "id": 1125083484425478145,
        "text": "Wait, Rick can actually be outsmarted? #RickandMorty @RickandMorty @AdultSwimUKpic.twitter.com/2iYLOWKsAy",
        "lang": "en",
        "username": "E4Tweets",
        "time": "2019-05-05 17:03:00",
        "permalink": "https://twitter.com/E4Tweets/status/1125083484425478145",
        "is_reply": false,
        "parent_id": null,
        "replies": 0,
        "retweets": 0,
        "favorites": 5
    },
    {
        "id": 1124957464137490432,
        "text": "Mr. Smith from the Matrix is like Mr. Meeseeks from @RickandMorty pic.twitter.com/BbIH0EGaNN",
        "lang": "en",
        "username": "TheVibeDealer3",
        "time": "2019-05-05 08:42:14",
        "permalink": "https://twitter.com/TheVibeDealer3/status/1124957464137490432",
        "is_reply": false,
        "parent_id": null,
        "replies": 0,
        "retweets": 0,
        "favorites": 2
    },
    {
        "id": 1125162848357888001,
        "text": "Ummm... This is outside my CVS!?\n#RickAndMorty @RickandMorty pic.twitter.com/lXVsJZSrEm",
        "lang": "en",
        "username": "Forest__Corgi",
        "time": "2019-05-05 22:18:22",
        "permalink": "https://twitter.com/Forest__Corgi/status/1125162848357888001",
        "is_reply": false,
        "parent_id": null,
        "replies": 0,
        "retweets": 0,
        "favorites": 4
    }
]
```

## APIs in code

`WARNING`: These code examples work only with >= python 3.6

### Twitter Advanced Search

`Premise`: I want to print out all the popular tweets from the last 2 months mentioning my favorite tv should RickAndMorty.

**Create a file called example.py in your virtual environment**

```python
from aiohttp import ClientSession
from aiohttp.client import ClientTimeout
from asyncio import get_event_loop
from textwrap import wrap
from time import time
from tweezer.client import search, Tweet

# Default timeout is 5 min.
# For long scraping tasks this is not enough.
_TIMEOUT = ClientTimeout(total=(15*60))


def _tweet_filter(tweet: Tweet) -> bool:
    # 1. Should be in english.
    # 2. Should be popular.
    # 3. Should not be a reply.
    return tweet.lang == "en" and \
           tweet.retweets > 1000 and \
           tweet.replies > 1000 and \
           tweet.favorites > 1000 and \
           not tweet.is_reply


def _print_tweet(tweet: Tweet) -> None:
    # Header of the tweet
    print(f"\t{'-' * 80}\n")

    # Print out the body of the tweet
    print(f"\t@{tweet.username} - {tweet.time}")
    print()

    text_lines = wrap(tweet.text, break_long_words=False)
    print(f"\t{' ' * 5} {text_lines[0] if text_lines else tweet.text}")
    for line in text_lines[1:]:
        print(f"\t{' ' * 5} {line}")

    # Print out the footer of the tweet
    print()
    print(f"\t{tweet.replies} replies - {tweet.retweets} retweets - {tweet.favorites} likes\n")

    # Print the links to the tweets
    print(f"\tTweet Link:   {tweet.permalink}")
    if tweet.is_reply:
        print(f"\tReplying to:  https://twitter.com/statuses/{tweet.parent_id}")

    # I like generous white spacing.
    print()


async def main():
    # Search parameters.
    search_params = {"date": ["2019-05-01", "2019-07-13"],
                     "lang": "en",
                     "mention": ["RickAndMorty"],
                     "k": "XXX"}  # Add your license key

    # Use the client session to make requests to tweezer.
    async with ClientSession(timeout=_TIMEOUT) as session:
        # Just cause you are interested in performance, just like me.
        start_time = time()
        total_tweets = 0

        # Print out all the tweets that is being returned back from the server
        async for tweet in search(session, search_params):
            total_tweets += 1

            # Filter out the tweets that you are not interested in.
            if not _tweet_filter(tweet):
                continue

            # Print the tweet that matches our search criteria.
            _print_tweet(tweet)

        # Print out the stats for the search
        total_time = time() - start_time
        print(f"\t{'-' * 80}\n")
        print(f"\tStats\n\t{'=' * 5}")
        print(f"\tTotal tweets received: {total_tweets}")
        print(f"\tTotal time:            {total_time:4.2f} s")
        print(f"\tTweets per second:     {(total_tweets / total_time):4.2f} tps")

if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(main())
    
```

**Run the example script**

```bash
python example.py
```

**Result**

```text
	--------------------------------------------------------------------------------

	@adultswim - 2019-05-15 15:01:19

	      We heard some of you were interested in this information.
	      #WarnerMediaUpfront @rickandmorty pic.twitter.com/UkUINBmw9a

	3409 replies - 100477 retweets - 199071 likes

	Tweet Link:   https://twitter.com/adultswim/status/1128676741139062787

	--------------------------------------------------------------------------------

	@RickandMorty - 2019-05-15 15:01:01

	      November. Rick and Morty is returning in November. #WarnerMediaUpfront
	      @adultswimpic.twitter.com/GCkuw7RxOa

	4987 replies - 115399 retweets - 251446 likes

	Tweet Link:   https://twitter.com/RickandMorty/status/1128676665301839872

	--------------------------------------------------------------------------------

	@ChrisEvans - 2019-06-04 21:11:59

	      There isn’t another show on television like @RickandMorty. It’s a true
	      original. And it’s awesome.

	4804 replies - 34591 retweets - 249933 likes

	Tweet Link:   https://twitter.com/ChrisEvans/status/1136017779545595906

	--------------------------------------------------------------------------------

	Stats
	=====
	Total tweets received: 5225
	Total time:            11.58 s
	Tweets per second:     451.19 tps
```

## NOTE

Both the client library and the tweezer URL are solely for my academic use. You may use the client library as an inspiration for something else, but **without a license key you are prohibited from using the tweezer URL**.
