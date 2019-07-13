from dataclasses import dataclass
from typing import Optional

# Access to the tweezer APIs
TWEEZER_URL = "https://dark-tweezer.herokuapp.com"


@dataclass(frozen=True, eq=True)
class Tweet:
    """
    An object representing the contents of a tweet.
    """
    id: int
    text: str
    lang: str
    username: str
    time: str
    permalink: str
    is_reply: bool
    parent_id: Optional[int]
    replies: int
    retweets: int
    favorites: int
