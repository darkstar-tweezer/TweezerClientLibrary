import logging

from aiohttp import ClientSession
from asyncio import sleep
from random import random
from tweezer import Tweet, TWEEZER_URL
from typing import Dict, Iterator
from ujson import loads


_DEFAULT_CONN_RETRIES = 10


class TweezerBusyError(RuntimeError):
    """
    An exception thrown when the server is busy and
    client cannot successfully create a connection before it runs out of retries.
    """
    pass


async def search(session: ClientSession, params: Dict[str, str],
                 url=TWEEZER_URL, max_retries=_DEFAULT_CONN_RETRIES):
    """
    Make a request to search for tweets.
    :param session: Session to use to make the requests.
    :param params: A dictionary containing the search parameters.
    :param url Override the endpoint to tweezer, if you require.
    :param max_retries Number of retires to establish a connection.
    :return: An asynchronous generator that yields back search tweets.
    """
    sleeper = _sleep_generator()
    retries = 0

    while True:
        # Make a request and await response back from the server
        response = await session.post(f"{url}/search", json=params)

        # The server is busy!
        # We got to backoff and retry
        if response.status == 503:
            # Check if we have exhausted our retries
            if retries >= max_retries:
                raise TweezerBusyError(f"Cannot establish a connection after {retries} retries.")

            # Backoff and sleep for sometime waiting for the server to become free
            text = await response.text()
            sleep_time = next(sleeper)
            retries += 1
            logging.warning(f"Server busy: {text}. "
                            f"Sleeping for {sleep_time:2.2f} s. "
                            f"Retry Count: {retries}")
            await sleep(sleep_time)
            continue

        # Unknown status code! Just error out
        elif response.status != 200:
            text = await response.text()
            raise Exception(f"Non- retry-able exception. Status: {response.status}\n{text}")

        break  # We have successfully opened the stream.

    # Read tweets from the stream, decode and yield them back
    async for serialized_tweet in response.content:
        yield Tweet(**loads(serialized_tweet.decode()))


def _sleep_generator(interval: int = 1.5) -> Iterator[int]:
    while True:
        yield interval + random()
