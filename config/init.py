"""
Configuration Module
~~~~~~~~~~~~~~~~~~~~

Exports all configuration variables for easy import throughout the application.
"""

from .settings import (
    TELEGRAM_BOT_TOKEN,
    RSS_FEEDS,
    CHANNEL_FEEDS,
    FETCH_INTERVAL,
    NEW_ARTICLE_THRESHOLD,
    LOG_LEVEL
)

__all__ = [
    'TELEGRAM_BOT_TOKEN',
    'RSS_FEEDS',
    'CHANNEL_FEEDS',
    'FETCH_INTERVAL',
    'NEW_ARTICLE_THRESHOLD',
    'LOG_LEVEL'
]