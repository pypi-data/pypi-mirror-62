# mynews_bot
By Rajarshi Ghosh <rajarshig89@gmail.com>

Introduction
------------
mynews_bot is a python command line application. It's objective is to collect news from various sources (using corresponding RSS feeds) & provide a terminal interface for viewing the collected data.

Usage
------------
```
usage: mynews_bot.py [-h] [-s SOURCE] [-t TOP] [-v]

Get news items from multiple news sources

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        Name of the news source. Available options are: TOI,
                        NYT, IT, GNEWS, QUINT, REDDIT, BBC, BUZZFEED,
                        ALJAZEERA, YAHOONEWS, CNN, GUARDIAN, WASHINGTON_POST,
                        CNBC, REUTERS, INDEPENDENT, BUSINESS_STANDARD
  -t TOP, --top TOP     Count of news items to show from top order. Default:
                        10
  -v, --version         show program's version number and exit
```

Example
------------
- Get news for source BBC
```
mynews_bot -s BBC
```
- Get top 5 news for source CNBC
```
mynews_bot -s CNBC -t 5
``` 
- Get news from all sources
```
mynews_bot -t 2
```
## News Sources
- Times Of India [https://timesofindia.indiatimes.com/rss.cms](https://timesofindia.indiatimes.com/rss.cms)
- New York Times [https://archive.nytimes.com/www.nytimes.com/services/xml/rss/index.html](https://archive.nytimes.com/www.nytimes.com/services/xml/rss/index.html)
- India Today [https://www.indiatoday.in/rss](https://www.indiatoday.in/rss)
- Google News
- Quint
- Reddit
- BBC
- Buzzfeed
- AlJazeera
- Yahoo News
- CNN
- Guardian
- Washington Post
- CNBC
- Reuters
- Independent
- Business Standard
