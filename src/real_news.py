"""© 2025-2026 ELOADXFAMILY - Tous droits réservés
Real News API - Fetch actual news from Twitter/X, Reddit, RSS feeds"""

import requests
import feedparser
from datetime import datetime, timedelta
from src.cache import CacheManager

cache = CacheManager()

def get_reddit_crypto_news(limit=10):
    """Fetch crypto news from Reddit r/cryptocurrency"""
    try:
        # Using PRAW requires authentication - alternative: use unofficial Reddit API or RSS
        url = "https://www.reddit.com/r/cryptocurrency/hot.json"
        headers = {'User-Agent': 'Dubai-Trading-Tools/1.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            news = []
            
            for post in posts[:limit]:
                try:
                    post_data = post.get('data', {})
                    news.append({
                        "titre": post_data.get('title', '')[:100],
                        "resume": post_data.get('selftext', '')[:200] or post_data.get('url', ''),
                        "source": "Reddit r/cryptocurrency",
                        "sentiment": "neutral",  # Would need NLP for real sentiment
                        "symbol": "ALL",
                        "date": datetime.fromtimestamp(post_data.get('created_utc', 0)).isoformat(),
                        "url": f"https://reddit.com{post_data.get('permalink', '')}"
                    })
                except:
                    pass
            
            return news
    except Exception as e:
        print(f"Reddit news error: {e}")
    
    return []

def get_rss_crypto_news(limit=10):
    """Fetch crypto news from RSS feeds (CoinDesk, CoinTelegraph, etc)"""
    feeds = [
        "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "https://cointelegraph.com/feed/",
    ]
    
    news = []
    try:
        for feed_url in feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:limit//len(feeds)]:
                    news.append({
                        "titre": entry.get('title', '')[:100],
                        "resume": entry.get('summary', '')[:200] or entry.get('description', ''),
                        "source": feed.feed.get('title', 'RSS Feed'),
                        "sentiment": "neutral",
                        "symbol": "BTC,ETH,CRYPTO",
                        "date": entry.get('published', datetime.now().isoformat()),
                        "url": entry.get('link', '')
                    })
            except:
                pass
    except Exception as e:
        print(f"RSS news error: {e}")
    
    return news[:limit]

def get_coingecko_trending():
    """Fetch trending coins from CoinGecko - real market data"""
    try:
        url = "https://api.coingecko.com/api/v3/search/trending"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            coins = data.get('coins', [])
            news = []
            
            for coin in coins[:7]:
                try:
                    item = coin.get('item', {})
                    news.append({
                        "titre": f"🔥 {item.get('name', '')} #{item.get('market_cap_rank', 'N/A')} trending",
                        "resume": f"Symbol: {item.get('symbol', '').upper()} - Price: ${item.get('price_btc', 0):.2f}",
                        "source": "CoinGecko Trending",
                        "sentiment": "bullish",
                        "symbol": item.get('symbol', 'CRYPTO').upper(),
                        "date": datetime.now().isoformat(),
                        "url": item.get('url', '')
                    })
                except:
                    pass
            
            return news
    except Exception as e:
        print(f"CoinGecko trending error: {e}")
    
    return []

def get_all_real_news():
    """Combine all real news sources"""
    cache_key = "real_news_all"
    
    # Check cache first (10 min for news)
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    all_news = []
    
    # Get from all sources
    all_news.extend(get_coingecko_trending())
    all_news.extend(get_rss_crypto_news(5))
    all_news.extend(get_reddit_crypto_news(5))
    
    # Remove duplicates by title
    seen = set()
    unique_news = []
    for item in all_news:
        title = item.get('titre', '')
        if title not in seen:
            seen.add(title)
            unique_news.append(item)
    
    # Cache for 10 minutes
    cache.set(cache_key, unique_news[:20], ttl=600)
    
    return unique_news[:20]
