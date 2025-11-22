"""
Utility Functions
~~~~~~~~~~~~~~~~~

Provides helper functions for HTTP requests, RSS parsing,
and date/time operations.
"""

import logging
from datetime import datetime, timedelta
from typing import Optional

import pytz
import requests
import feedparser
import backoff
from dateutil import parser as dateutil_parser
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config.settings import REQUEST_TIMEOUT, MAX_RETRIES

logger = logging.getLogger(__name__)


class RSSFetchError(Exception):
    """Raised when RSS feed cannot be fetched."""
    pass


def create_http_session() -> requests.Session:
    """
    Create an HTTP session with retry logic.

    Configures automatic retries for failed requests with exponential backoff.
    Handles common server errors (500, 502, 503, 504) gracefully.

    Returns:
        Configured requests.Session instance
    """
    session = requests.Session()

    retry_strategy = Retry(
        total=MAX_RETRIES,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET", "POST", "OPTIONS"]
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session


@backoff.on_exception(
    backoff.expo,
    requests.exceptions.RequestException,
    max_tries=5,
    max_time=30
)
def fetch_rss_feed(url: str, timeout: int = REQUEST_TIMEOUT) -> feedparser.FeedParserDict:
    """
    Fetch and parse an RSS feed with automatic retry logic.

    Implements exponential backoff for failed requests and includes
    user agent spoofing to bypass basic bot detection.

    Args:
        url: RSS feed URL to fetch
        timeout: Maximum seconds to wait for response

    Returns:
        Parsed feed data structure

    Raises:
        RSSFetchError: If feed cannot be fetched after all retries
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return feedparser.parse(response.content)

    except requests.exceptions.Timeout:
        logger.warning(f"Request timeout for {url}")
        return feedparser.FeedParserDict({"entries": []})

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return feedparser.FeedParserDict({"entries": []})


def parse_publish_date(date_string: str) -> Optional[datetime]:
    """
    Parse article publication date with timezone handling.

    Args:
        date_string: Date string in various RSS formats

    Returns:
        Parsed datetime in UTC, or None if parsing fails
    """
    try:
        parsed_date = dateutil_parser.parse(date_string)
        return parsed_date.astimezone(pytz.UTC)
    except Exception as e:
        logger.warning(f"Date parse error for '{date_string}': {e}")
        return None


def is_article_recent(published_time: str, threshold_minutes: int) -> bool:
    """
    Check if article was published within the time threshold.

    Prevents posting old articles when bot starts or restarts.

    Args:
        published_time: Article publication timestamp
        threshold_minutes: Maximum age in minutes for article to be considered recent

    Returns:
        True if article is recent, False otherwise
    """
    published_date = parse_publish_date(published_time)
    if not published_date:
        return False

    current_time = datetime.now(pytz.UTC)
    age = current_time - published_date

    return age <= timedelta(minutes=threshold_minutes)