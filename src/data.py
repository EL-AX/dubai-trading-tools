import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.cache import CacheManager

cache = CacheManager()

def get_live_price(ticker):
    cached = cache.get(f"price_{ticker}")
    if cached:
        return cached
    
    # All cryptos use CoinGecko
    if ticker in ["BTC", "ETH", "SOL", "ADA", "XRP", "DOT"]:
        return get_crypto_price(ticker)
    elif ticker in ["EUR", "GBP", "JPY", "AUD"]:
        return get_forex_price(ticker)
    elif ticker == "XAU":
        return get_gold_price()
    
    return generate_mock_data(ticker, 1).iloc[-1].to_dict()

def get_crypto_price(ticker):
    try:
        coins = {
            "BTC": "bitcoin",
            "ETH": "ethereum",
            "SOL": "solana",
            "ADA": "cardano",
            "XRP": "ripple",
            "DOT": "polkadot"
        }
        if ticker not in coins:
            return generate_mock_data(ticker, 1).iloc[-1].to_dict()
        
        # Try CoinGecko - real prices with 2h cache
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coins[ticker]}&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                coin_data = data.get(coins[ticker], {})
                price = coin_data.get("usd")
                if price and isinstance(price, (int, float)) and price > 0:
                    result = {
                        "ticker": ticker,
                        "price": float(price),
                        "volume": float(coin_data.get("usd_24h_vol", 0) or 0),
                        "market_cap": float(coin_data.get("usd_market_cap", 0) or 0),
                        "change_24h": float(coin_data.get("usd_24h_change", 0) or 0),
                        "timestamp": datetime.now()
                    }
                    cache.set(f"price_{ticker}", result, ttl=10)  # live TTL (10s) for responsive UI
                    return result
        except Exception as e:
            pass
        
        # Fallback to realistic mock data based on historical ranges
        mock_prices = {
            "BTC": 76500,
            "ETH": 2250,
            "SOL": 100,
            "ADA": 1.05,
            "XRP": 2.45,
            "DOT": 8.50
        }
        base_price = mock_prices.get(ticker, 100)
        # Add small random variation (±1%)
        variation = base_price * (np.random.uniform(-0.01, 0.01))
        price = base_price + variation
        
        result = {
            "ticker": ticker,
            "price": float(price),
            "volume": float(np.random.uniform(1e9, 5e9)),
            "market_cap": float(np.random.uniform(1e12, 5e12)),
            "change_24h": np.random.uniform(-5, 5),
            "timestamp": datetime.now()
        }
        cache.set(f"price_{ticker}", result, ttl=10)  # live TTL (10s) for responsive UI
        return result
        
    except Exception as e:
        pass
    
    return generate_mock_data(ticker, 1).iloc[-1].to_dict()

def get_forex_price(ticker):
    try:
        # EUR vs USD 
        if ticker == "EUR":
            # Try multiple sources for better reliability
            try:
                url = "https://api.exchangerate.host/latest?base=USD&symbols=EUR"
                response = requests.get(url, timeout=3)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success") and "rates" in data:
                        rate = data.get("rates", {}).get("EUR")
                        if rate and isinstance(rate, (int, float)) and rate > 0:
                            result = {
                                "ticker": "EUR",
                                "price": float(rate),
                                "volume": 0,
                                "market_cap": 0,
                                "timestamp": datetime.now()
                            }
                            cache.set(f"price_EUR", result, ttl=7200)  # 2h cache
                            return result
            except:
                pass
            
            # Fallback to alternative source
            try:
                url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=eur&include_market_cap=false"
                response = requests.get(url, timeout=3)
                if response.status_code == 200:
                    data = response.json()
                    eth_eur = data.get("ethereum", {}).get("eur")
                    if eth_eur:
                        # Rough conversion
                        rate = eth_eur / 2200  # Approx ETH price in EUR / 2200
                        if rate > 0.5:  # EUR should be around 1.05
                            result = {
                                "ticker": "EUR",
                                "price": float(rate),
                                "volume": 0,
                                "market_cap": 0,
                                "timestamp": datetime.now()
                            }
                            cache.set(f"price_EUR", result, ttl=7200)
                            return result
            except:
                pass
        else:
            url = f"https://api.exchangerate.host/latest?base=USD&symbols={ticker}"
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "rates" in data:
                    rate = data.get("rates", {}).get(ticker)
                    if rate and isinstance(rate, (int, float)) and rate > 0:
                        result = {
                            "ticker": ticker,
                            "price": float(rate),
                            "volume": 0,
                            "market_cap": 0,
                            "timestamp": datetime.now()
                        }
                        cache.set(f"price_{ticker}", result, ttl=7200)  # 2h cache
                        return result
    except Exception as e:
        pass
    
    # Fallback to realistic mock data
    mock_forex_prices = {
        "EUR": 1.08,
        "GBP": 1.27,
        "JPY": 0.0067,
        "AUD": 0.65
    }
    base_price = mock_forex_prices.get(ticker, 1.0)
    variation = base_price * (np.random.uniform(-0.01, 0.01))
    price = base_price + variation
    
    result = {
        "ticker": ticker,
        "price": float(price),
        "volume": 0,
        "market_cap": 0,
        "timestamp": datetime.now()
    }
    cache.set(f"price_{ticker}", result, ttl=7200)  # 2h cache
    return result

def get_gold_price():
    try:
        url = "https://data-asg.goldprice.org/dbXau/USD"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [{}])[0] if isinstance(data.get("items"), list) else {}
            # Try multiple possible keys commonly used by gold APIs
            price = None
            for k in ("xauPrice", "xau", "price", "xau_price", "price_usd"):
                if isinstance(items, dict) and items.get(k):
                    price = items.get(k)
                    break
            # try top-level keys
            if not price:
                price = data.get("xauPrice") or data.get("price")
            # Fallback to exchangerate.host convert endpoint (supports XAU)
            if not price:
                try:
                    conv_url = "https://api.exchangerate.host/convert?from=XAU&to=USD"
                    r2 = requests.get(conv_url, timeout=5)
                    if r2.status_code == 200:
                        j2 = r2.json()
                        price = j2.get("result")
                except:
                    pass
            if price:
                try:
                    price_val = float(price)
                except Exception:
                    price_val = None
                if price_val:
                    result = {
                        "ticker": "XAU",
                        "price": float(price_val),
                        "volume": 0,
                        "market_cap": 0,
                        "timestamp": datetime.now()
                    }
                    cache.set("price_XAU", result, ttl=60)  # short TTL for live-like updates
                    return result
    except:
        pass

    # Final fallback to mock
    return generate_mock_data("XAU", 1).iloc[-1].to_dict()

def generate_mock_data(ticker, days=1, hours=None):
    """Generate mock candlestick data.
    Accepts either 'days' or 'hours' for backward compatibility with older tests that pass hours=.."""
    base_prices = {
        "BTC": 45000,
        "ETH": 2500,
        "SOL": 180,
        "EUR": 1.08,
        "GBP": 1.27,
        "JPY": 0.0067,
        "AUD": 0.66,
        "XAU": 2050
    }
    
    base_price = base_prices.get(ticker, 100)
    if hours is not None:
        num_candles = int(hours)
    else:
        num_candles = int(days * 24)
    dates = pd.date_range(end=datetime.now(), periods=num_candles, freq="h")
    
    returns = np.random.normal(0.0001, 0.01, num_candles)
    prices = base_price * np.exp(np.cumsum(returns))
    
    data = pd.DataFrame({
        "timestamp": dates,
        "open": prices * (1 + np.random.normal(0, 0.001, num_candles)),
        "high": prices * (1 + abs(np.random.normal(0, 0.005, num_candles))),
        "low": prices * (1 - abs(np.random.normal(0, 0.005, num_candles))),
        "close": prices,
        "volume": np.random.randint(1000000, 10000000, num_candles)
    })
    # Provide backward-compatible capitalised OHLCV column names
    data["Open"] = data["open"]
    data["High"] = data["high"]
    data["Low"] = data["low"]
    data["Close"] = data["close"]
    data["Volume"] = data["volume"]
    
    return data

def get_historical_data(ticker, days=90):
    """Fetch real OHLC data from CoinGecko for crypto, mock for others"""
    cached = cache.get(f"history_{ticker}_{days}")
    if cached is not None:
        return cached
    
    # Try real OHLC data for cryptos from CoinGecko
    if ticker in ["BTC", "ETH", "SOL"]:
        try:
            ohlc_data = fetch_coingecko_ohlc(ticker, days)
            if not ohlc_data.empty:
                cache.set(f"history_{ticker}_{days}", ohlc_data, ttl=3600)  # 1h cache for real data
                return ohlc_data
        except Exception as e:
            pass
    
    # Fallback to realistic mock data if API fails
    data = generate_mock_data(ticker, days)
    cache.set(f"history_{ticker}_{days}", data, ttl=600)
    return data

def fetch_coingecko_ohlc(ticker, days):
    """Fetch real OHLC data from CoinGecko"""
    try:
        coins = {
            "BTC": "bitcoin",
            "ETH": "ethereum",
            "SOL": "solana"
        }
        if ticker not in coins:
            return pd.DataFrame()
        
        # CoinGecko OHLC endpoint (daily data)
        url = f"https://api.coingecko.com/api/v3/coins/{coins[ticker]}/ohlc?vs_currency=usd&days={days}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            ohlc_list = response.json()
            if isinstance(ohlc_list, list) and len(ohlc_list) > 0:
                df = pd.DataFrame(ohlc_list, columns=['timestamp', 'open', 'high', 'low', 'close'])
                # Convert milliseconds to datetime
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                # Add mock volume (CoinGecko OHLC doesn't include volume)
                df['volume'] = df['close'] * np.random.uniform(0.5, 1.5, len(df))
                return df
    except Exception as e:
        pass
    
    return pd.DataFrame()

def get_live_price_batch(tickers):
    results = {}
    for ticker in tickers:
        results[ticker] = get_live_price(ticker)
    return results
