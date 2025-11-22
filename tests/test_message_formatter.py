"""
Message Formatter Tests
~~~~~~~~~~~~~~~~~~~~~~~

Unit tests for message formatting functionality.
"""

import unittest
from unittest.mock import Mock

from src.message_formatter import format_article, format_article_summary


class TestMessageFormatter(unittest.TestCase):
    """Test cases for message_formatter module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_article = Mock()
        self.sample_article.title = "Breaking News: Major Event"
        self.sample_article.link = "https://example.com/article"
    
    def test_format_article_basic(self):
        """Test basic article formatting."""
        result = format_article(self.sample_article)
        
        self.assertIn("Breaking News: Major Event", result)
        self.assertIn("https://example.com/article", result)
        self.assertIn("Read more", result)
    
    def test_format_article_with_source(self):
        """Test article formatting with source attribution."""
        result = format_article(
            self.sample_article,
            include_source=True,
            source_name="Example News"
        )
        
        self.assertIn("Example News", result)
        self.assertIn("<b>", result)
    
    def test_format_article_summary_truncation(self):
        """Test summary truncation for long text."""
        self.sample_article.get.return_value = "A" * 300
        
        result = format_article_summary(self.sample_article, max_length=100)
        
        self.assertLess(len(result), 400)
        self.assertIn("...", result)


if __name__ == '__main__':
    unittest.main()