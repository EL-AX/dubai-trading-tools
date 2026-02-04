"""© 2025-2026 ELOADXFAMILY - Tous droits réservés
WebSocket Real-Time Price Feeds - Flux temps réel avec Binance, CoinCap, Coinbase

Implémente:
- Binance WebSocket: Flux de prix, trades, OHLC
- CoinCap WebSocket: Prix simples et rapides
- Support pour futures et spot markets
"""

import websocket
import json
import threading
import time
from datetime import datetime
from collections import deque
from src.cache import CacheManager

cache = CacheManager()

class BinanceWebSocketFeed:
    """Flux WebSocket Binance pour données temps réel"""
    
    def __init__(self):
        self.prices = {}
        self.trades = deque(maxlen=100)
        self.running = False
        self.ws = None
        
    def start_ticker_feed(self, symbols=None):
        """Démarrer flux de ticker prix en temps réel
        
        Args:
            symbols: Liste de symbols (ex: ['BTCUSDT', 'ETHUSDT'])
        """
        if symbols is None:
            symbols = ['BTCUSDT', 'ETHUSDT', 'SOLusdt']
        
        # Créer les canaux (ex: btcusdt@ticker)
        channels = ''.join([f'{symbol.lower()}@ticker/' for symbol in symbols]).rstrip('/')
        url = f"wss://stream.binance.com:9443/stream?streams={channels}"
        
        def on_message(ws, message):
            try:
                data = json.loads(message)
                stream_data = data.get('data', {})
                symbol = stream_data.get('s', '')
                price = float(stream_data.get('c', 0))  # Close price
                
                if symbol and price > 0:
                    self.prices[symbol] = {
                        'price': price,
                        'timestamp': datetime.now().isoformat(),
                        'bid': float(stream_data.get('b', 0)),
                        'ask': float(stream_data.get('a', 0)),
                        'volume': float(stream_data.get('v', 0))
                    }
                    # Cache pour 10 secondes
                    cache.set(f"binance_price_{symbol}", self.prices[symbol], ttl=10)
            except Exception as e:
                pass
        
        def on_error(ws, error):
            pass
        
        def on_close(ws, close_status_code, close_msg):
            self.running = False
        
        def on_open(ws):
            self.running = True
        
        try:
            self.ws = websocket.WebSocketApp(
                url,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
                on_open=on_open
            )
            
            # Exécuter en thread séparé
            thread = threading.Thread(target=self.ws.run_forever, daemon=True)
            thread.start()
            return True
        except Exception as e:
            return False
    
    def get_price(self, symbol):
        """Obtenir le prix actuel du symbol
        
        Args:
            symbol: Symbol Binance (ex: 'BTCUSDT')
            
        Returns:
            dict avec prix et métadonnées
        """
        cached = cache.get(f"binance_price_{symbol}")
        if cached:
            return cached
        return self.prices.get(symbol, {})
    
    def stop(self):
        """Arrêter le flux WebSocket"""
        if self.ws:
            self.ws.close()
            self.running = False

class CoinCapWebSocketFeed:
    """Flux WebSocket CoinCap - Super simple et rapide"""
    
    def __init__(self):
        self.prices = {}
        self.running = False
        self.ws = None
    
    def start_price_feed(self, assets=None):
        """Démarrer flux de prix CoinCap
        
        Args:
            assets: Liste des assets (ex: ['bitcoin', 'ethereum', 'solana'])
        """
        if assets is None:
            assets = ['bitcoin', 'ethereum', 'solana', 'cardano', 'ripple']
        
        assets_str = ','.join(assets)
        url = f"wss://ws.coincap.io/prices?assets={assets_str}"
        
        def on_message(ws, message):
            try:
                data = json.loads(message)
                for asset, price in data.items():
                    try:
                        price_float = float(price)
                        if price_float > 0:
                            self.prices[asset] = {
                                'price': price_float,
                                'timestamp': datetime.now().isoformat(),
                                'source': 'coincap'
                            }
                            cache.set(f"coincap_price_{asset}", self.prices[asset], ttl=5)
                    except:
                        pass
            except Exception as e:
                pass
        
        def on_error(ws, error):
            pass
        
        def on_close(ws, close_status_code, close_msg):
            self.running = False
        
        def on_open(ws):
            self.running = True
        
        try:
            self.ws = websocket.WebSocketApp(
                url,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
                on_open=on_open
            )
            
            thread = threading.Thread(target=self.ws.run_forever, daemon=True)
            thread.start()
            return True
        except Exception as e:
            return False
    
    def get_price(self, asset):
        """Obtenir le prix d'un asset
        
        Args:
            asset: Asset name (ex: 'bitcoin')
            
        Returns:
            dict avec prix
        """
        cached = cache.get(f"coincap_price_{asset}")
        if cached:
            return cached
        return self.prices.get(asset, {})
    
    def stop(self):
        """Arrêter le flux"""
        if self.ws:
            self.ws.close()
            self.running = False

class CoinbaseWebSocketFeed:
    """Flux WebSocket Coinbase - Données publiques"""
    
    def __init__(self):
        self.prices = {}
        self.trades = deque(maxlen=50)
        self.running = False
        self.ws = None
    
    def start_ticker_feed(self, product_ids=None):
        """Démarrer flux de ticker Coinbase
        
        Args:
            product_ids: Liste des product IDs (ex: ['BTC-USD', 'ETH-USD'])
        """
        if product_ids is None:
            product_ids = ['BTC-USD', 'ETH-USD', 'SOL-USD']
        
        url = "wss://ws-feed.exchange.coinbase.com"
        
        def on_message(ws, message):
            try:
                data = json.loads(message)
                if data.get('type') == 'ticker':
                    product_id = data.get('product_id', '')
                    price = float(data.get('price', 0))
                    
                    if product_id and price > 0:
                        self.prices[product_id] = {
                            'price': price,
                            'timestamp': data.get('time', datetime.now().isoformat()),
                            'bid': float(data.get('best_bid', 0)),
                            'ask': float(data.get('best_ask', 0)),
                            'volume_24h': float(data.get('volume_24h', 0))
                        }
                        cache.set(f"coinbase_price_{product_id}", self.prices[product_id], ttl=10)
                
                elif data.get('type') == 'match':
                    self.trades.append(data)
            except Exception as e:
                pass
        
        def on_error(ws, error):
            pass
        
        def on_close(ws, close_status_code, close_msg):
            self.running = False
        
        def on_open(ws):
            self.running = True
            # Envoyer subscribe message
            subscribe_msg = {
                "type": "subscribe",
                "product_ids": product_ids,
                "channels": ["ticker", "match"]
            }
            ws.send(json.dumps(subscribe_msg))
        
        try:
            self.ws = websocket.WebSocketApp(
                url,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
                on_open=on_open
            )
            
            thread = threading.Thread(target=self.ws.run_forever, daemon=True)
            thread.start()
            return True
        except Exception as e:
            return False
    
    def get_price(self, product_id):
        """Obtenir le prix d'un product
        
        Args:
            product_id: Product ID (ex: 'BTC-USD')
            
        Returns:
            dict avec prix et données
        """
        cached = cache.get(f"coinbase_price_{product_id}")
        if cached:
            return cached
        return self.prices.get(product_id, {})
    
    def get_recent_trades(self, product_id=None, limit=10):
        """Obtenir les trades récents"""
        return list(self.trades)[-limit:]
    
    def stop(self):
        """Arrêter le flux"""
        if self.ws:
            self.ws.close()
            self.running = False

# Instances globales (singleton pattern)
_binance_feed = None
_coincap_feed = None
_coinbase_feed = None

def get_binance_feed():
    """Obtenir instance du flux Binance"""
    global _binance_feed
    if _binance_feed is None:
        _binance_feed = BinanceWebSocketFeed()
    return _binance_feed

def get_coincap_feed():
    """Obtenir instance du flux CoinCap"""
    global _coincap_feed
    if _coincap_feed is None:
        _coincap_feed = CoinCapWebSocketFeed()
    return _coincap_feed

def get_coinbase_feed():
    """Obtenir instance du flux Coinbase"""
    global _coinbase_feed
    if _coinbase_feed is None:
        _coinbase_feed = CoinbaseWebSocketFeed()
    return _coinbase_feed

def initialize_realtime_feeds():
    """Initialiser tous les flux temps réel"""
    try:
        # Binance
        binance = get_binance_feed()
        binance.start_ticker_feed(['BTCUSDT', 'ETHUSDT', 'SOLUSDT'])
        
        # CoinCap
        coincap = get_coincap_feed()
        coincap.start_price_feed(['bitcoin', 'ethereum', 'solana'])
        
        return True
    except Exception as e:
        return False

def cleanup_feeds():
    """Arrêter tous les flux"""
    if _binance_feed:
        _binance_feed.stop()
    if _coincap_feed:
        _coincap_feed.stop()
    if _coinbase_feed:
        _coinbase_feed.stop()
