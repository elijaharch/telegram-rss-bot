"""
Application Settings
~~~~~~~~~~~~~~~~~~~~

Central configuration for the Telegram RSS Bot.
All environment variables and constants are defined here.
"""

import os
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# Application Configuration
# ============================================================================

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN not found in environment. "
        "Please configure your .env file."
    )

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# ============================================================================
# Feed Monitoring Configuration
# ============================================================================

FETCH_INTERVAL = int(os.getenv('FETCH_INTERVAL', 15))
NEW_ARTICLE_THRESHOLD = int(os.getenv('NEW_ARTICLE_THRESHOLD', 2))

# HTTP request configuration
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 10))
MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))

# ============================================================================
# RSS Feed Sources
# ============================================================================

RSS_FEEDS: Dict[str, List[Dict[str, str]]] = {
    "EN": [
        {
            "url": "https://rss.cnn.com/rss/edition.rss",
            "source": "CNN"
        },
        {
            "url": "https://feeds.bbci.co.uk/news/rss.xml",
            "source": "BBC News"
        },
        {
            "url": "https://www.reuters.com/tools/rss",
            "source": "Reuters"
        }
    ],
    "RU": [
        {
            "url": "https://lenta.ru/rss",
            "source": "Lenta.ru"
        },
        {
            "url": "http://static.feed.rbc.ru/rbc/logical/footer/news.rss",
            "source": "RBC News"
        }
    ]
}

# ============================================================================
# Channel Configuration
# ============================================================================

CHANNEL_FEEDS: Dict[str, Dict] = {
    "@promotesten": {
        "language": "EN",
        "feeds": RSS_FEEDS["EN"]
    },
    "@promotestru": {
        "language": "RU",
        "feeds": RSS_FEEDS["RU"]
    }
}