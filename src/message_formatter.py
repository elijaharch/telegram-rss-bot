"""
Message Formatter
~~~~~~~~~~~~~~~~~

Handles formatting of RSS articles into Telegram messages.
"""

from typing import Optional


def format_article(article, include_source: bool = False, source_name: Optional[str] = None) -> str:
    """
    Format RSS article for Telegram posting.
    
    Creates HTML-formatted message with article title and link.
    
    Args:
        article: RSS feed entry object
        include_source: Whether to include source attribution
        source_name: Name of the news source
        
    Returns:
        HTML-formatted message string
    """
    title = article.title
    link = article.link
    
    if include_source and source_name:
        return (
            f"<b>{source_name}</b>\n"
            f"{title}\n"
            f"<a href='{link}'>Read more</a>"
        )
    
    return f"{title}\n<a href='{link}'>Read more</a>"


def format_article_summary(article, max_length: int = 200) -> str:
    """
    Format article with summary text.
    
    Args:
        article: RSS feed entry object
        max_length: Maximum length for summary
        
    Returns:
        Formatted message with summary
    """
    title = article.title
    link = article.link
    summary = article.get("summary", "")
    
    if summary and len(summary) > max_length:
        summary = summary[:max_length] + "..."
    
    message = f"<b>{title}</b>\n"
    if summary:
        message += f"\n{summary}\n"
    message += f"\n<a href='{link}'>Read more</a>"
    
    return message