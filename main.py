"""
Telegram RSS Bot
"""

import logging
import threading
import sys

from src.feed_handler import run_monitor_with_recovery
from src.telegram_poster import initialize_bot
from config.settings import CHANNEL_FEEDS, FETCH_INTERVAL, NEW_ARTICLE_THRESHOLD

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def display_startup_info():
    """Display startup configuration information."""
    info = f"""
{'='*60}
Telegram RSS Bot
{'='*60}
Configuration:
  - Channels monitored: {len(CHANNEL_FEEDS)}
  - Check interval: {FETCH_INTERVAL}s
  - Article threshold: {NEW_ARTICLE_THRESHOLD}min
{'='*60}
"""
    print(info)


def main():
    """Initialize and start the bot."""
    display_startup_info()
    
    logger.info("Initializing bot components...")
    
    try:
        # Initialize Telegram bot
        bot = initialize_bot()
        logger.info("Bot initialized successfully")
        
        # Start feed monitoring thread
        monitor_thread = threading.Thread(
            target=run_monitor_with_recovery,
            daemon=True,
            name="FeedMonitor"
        )
        monitor_thread.start()
        logger.info("Feed monitor started")
        
        # Start bot polling
        logger.info("Bot is now running. Press CTRL+C to stop.")
        bot.infinity_polling()
        
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()