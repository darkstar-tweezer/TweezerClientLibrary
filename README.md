## Introduction

Tweezer provides APIs to scrape data from web pages.

1. Twitter Advanced Search

Allows you to scrape tweets returned from twitter advanced search.

## Quick Start

Say you want to scrape tweets using the twitter advanced search.

### Using GET request

#### Construct your search URL

1. Go to twitter [advanced search](https://twitter.com/search-advanced) in your favorite browser, construct your search query and hit `search`.
2. Copy over the URL generated. For example, mine was: <https://twitter.com/search?l=en&q=%40RickAndMorty%20since%3A2019-01-01%20until%3A2019-07-13&src=typd>
3. Replace the `twitter.com` with `dark-tweezer.herokuapp.com`.

`Result`: <https://dark-tweezer.herokuapp.com/search?l=en&q=%40RickAndMorty%20since%3A2019-01-01%20until%3A2019-07-13&src=typd>

#### Download tweets from browser

Paste <https://dark-tweezer.herokuapp.com/search?l=en&q=%40RickAndMorty%20since%3A2019-01-01%20until%3A2019-07-13&src=typd> into your broswer and wait for the download to complete. 

You should have a file called `tweets.json`.

#### Download/view tweets from CLI

**Download to a file**

```bash
$ curl "https://dark-tweezer.herokuapp.com/search?l=en&q=%40RickAndMorty%20since%3A2019-01-01%20until%3A2019-07-13&src=typd" -o pickle_rick.json
curl "https://dark-tweezer.herokuapp.com/search?l=en&q=%40RickAndMorty%20since%3A2019-01-01%20until%3A2019-07-13&src=typd" -o pickle_rick.json
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


$ cat pickle_rick.json | wc -l
11816

# This means we have `11814` tweets. 1 line for list start and 1 for list end.
```

**Just view tweets**

```bash
curl "https://dark-tweezer.herokuapp.com/search?l=en&q=%40RickAndMorty%20since%3A2019-01-01%20until%3A2019-07-13&src=typd"
```

## Using APIs in code

TODO
