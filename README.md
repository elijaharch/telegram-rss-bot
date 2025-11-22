# 🤖 Telegram RSS News Bot

A Python bot that monitors RSS feeds and automatically posts new articles to configured Telegram channels in real-time.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## ✨ Features

- Monitors multiple RSS feeds simultaneously
- Multi-language support (English & Russian)
- Real-time article detection and posting
- Automatic retry logic with exponential backoff
- Comprehensive logging
- Error handling and crash recovery

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- A Telegram Bot Token ([How to get one](https://core.telegram.org/bots#6-botfather))
- Telegram channels where the bot is an administrator

### Installation

1. **Clone the repository**
```bash
   git clone https://github.com/yourusername/telegram-rss-bot.git
   cd telegram-rss-bot
```

2. **Create a virtual environment**
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
   cp .env.example .env
   # Edit .env and add your TELEGRAM_BOT_TOKEN
```

5. **Run the bot**
```bash
   python bot.py
```

## ⚙️ Configuration

### Adding RSS Feeds

Edit the `RSS_FEEDS` dictionary in `bot.py`:
```python
RSS_FEEDS = {
    "EN": [
        {"url": "https://example.com/rss", "source": "Example News"}
    ],
    "RU": [
        {"url": "https://example.ru/rss", "source": "Пример Новостей"}
    ]
}
```

### Configuring Channels

Edit the `CHANNEL_FEEDS` dictionary:
```python
CHANNEL_FEEDS = {
    "@yourchannel": {"language": "EN", "feeds": RSS_FEEDS["EN"]},
}
```

### Adjusting Settings

- `FETCH_INTERVAL`: Time between feed checks (seconds)
- `NEW_ARTICLE_THRESHOLD_MINUTES`: How recent articles must be to post

## 📖 Usage

Once running, the bot will:
1. Check configured RSS feeds every 15 seconds
2. Detect articles published within the last 2 minutes
3. Automatically post new articles to the appropriate channels
4. Log all activities to `bot.log`

## 🐛 Troubleshooting

### Bot doesn't post articles
- Verify the bot is an administrator in your channel
- Check that RSS feed URLs are accessible
- Review logs in `bot.log` for errors

### Connection errors
- The bot includes automatic retry logic
- Check your internet connection
- Verify RSS feed URLs are correct

## 🙏 Acknowledgments

- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) - Telegram Bot API wrapper
- [feedparser](https://github.com/kurtmckee/feedparser) - RSS feed parser

