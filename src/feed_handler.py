"""
RSS Feed Handler
~~~~~~~~~~~~~~~~

Manages RSS feed monitoring, article discovery, and posting coordination.
"""

import time
import logging
from typing import Dict, List, Set

from src.utils import fetch_rss_feed, is_article_recent
from src.telegram_poster import post_to_channel
from config.settings import (
    CHANNEL_FEEDS,
    FETCH_INTERVAL,
    NEW_ARTICLE_THRESHOLD,
    RSS_FEEDS
)

logger = logging.getLogger(__name__)

# Track posted articles to prevent duplicates
posted_articles: Dict[str, Set[str]] = {
    lang: set() for lang in RSS_FEEDS
}


def discover_new_articles(language: str, feeds: List[Dict[str, str]]) -> List:
    """
    Discover new articles from configured RSS feeds.
    
    Filters articles based on:
    - Publication time (must be recent)
    - Uniqueness (not previously posted)
    
    Args:
        language: Language code for feed group
        feeds: List of feed configurations
        
    Returns:
        List of new article entries ready for posting
    """
    new_articles = []
    
    for feed_config in feeds:
        feed_url = feed_config["url"]
        feed_name = feed_config["source"]
        
        logger.debug(f"Checking {feed_name} ({feed_url})")
        
        feed_data = fetch_rss_feed(feed_url)
        
        for article in feed_data.entries:
            published_time = article.get("published")
            
            if not published_time:
                continue
            
            if not is_article_recent(published_time, NEW_ARTICLE_THRESHOLD):
                continue
            
            if article.link in posted_articles[language]:
                continue
            
            new_articles.append(article)
            posted_articles[language].add(article.link)
            logger.info(f"New article discovered: {article.title[:60]}")
    
    return new_articles


def monitor_feeds():
    """
    Main monitoring loop for RSS feeds.
    
    Continuously checks all configured feeds and posts new articles
    to their respective channels.
    """
    logger.info("Starting feed monitoring loop")
    
    while True:
        for channel, config in CHANNEL_FEEDS.items():
            language = config["language"]
            feeds = config["feeds"]
            
            logger.debug(f"Scanning {language} feeds for {channel}")
            
            try:
                new_articles = discover_new_articles(language, feeds)
                
                if new_articles:
                    logger.info(f"Found {len(new_articles)} new article(s) for {channel}")
                    
                    for article in new_articles:
                        post_to_channel(channel, article)
                        time.sleep(1)  # Rate limiting
                        
            except Exception as e:
                logger.error(f"Error processing {language} feeds: {e}", exc_info=True)
        
        logger.debug(f"Sleeping for {FETCH_INTERVAL} seconds")
        time.sleep(FETCH_INTERVAL)


def run_monitor_with_recovery():
    """
    Wrapper for monitor_feeds with automatic crash recovery.
    
    Ensures the monitoring loop continues running even if exceptions occur.
    """
    while True:
        try:
            monitor_feeds()
        except Exception as e:
            logger.critical(f"Monitor loop crashed: {e}", exc_info=True)
            logger.info("Restarting monitor in 5 seconds...")
            time.sleep(5)