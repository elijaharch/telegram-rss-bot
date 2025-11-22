"""
Telegram Poster
~~~~~~~~~~~~~~~

Handles all Telegram Bot API interactions and message posting.
"""

import logging
import telebot

from config.settings import TELEGRAM_BOT_TOKEN
from src.message_formatter import format_article

logger = logging.getLogger(__name__)

_bot_instance = None


def initialize_bot() -> telebot.TeleBot:
    """
    Initialize and return the Telegram bot instance.

    Uses singleton pattern to ensure only one bot instance exists.

    Returns:
        Configured TeleBot instance
    """
    global _bot_instance

    if _bot_instance is None:
        _bot_instance = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
        logger.info("Telegram bot instance created")

    return _bot_instance


def get_bot() -> telebot.TeleBot:
    """
    Get the current bot instance.

    Returns:
        TeleBot instance
    """
    global _bot_instance

    if _bot_instance is None:
        _bot_instance = initialize_bot()

    return _bot_instance


def post_to_channel(channel: str, article) -> bool:
    """
    Post article to specified Telegram channel.

    Args:
        channel: Channel username or ID (e.g., "@channelname")
        article: RSS article entry to post

    Returns:
        True if successful, False otherwise
    """
    bot = get_bot()
    message = format_article(article)

    try:
        bot.send_message(channel, message, parse_mode="HTML")
        logger.info(f"Posted to {channel}: {article.title[:50]}")
        return True

    except telebot.apihelper.ApiException as e:
        logger.error(f"Telegram API error posting to {channel}: {e}")
        return False

    except Exception as e:
        logger.error(f"Unexpected error posting to {channel}: {e}", exc_info=True)
        return False
