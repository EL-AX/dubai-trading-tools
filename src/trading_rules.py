import numpy as np
from src.indicators import calculate_rsi, calculate_macd, calculate_bollinger_bands, calculate_trend

class TradingRules:
    def __init__(self, prices):
        self.prices = prices
        self.rsi = calculate_rsi(prices)
        self.macd, self.signal, self.histogram = calculate_macd(prices)
        self.bb_mid, self.bb_upper, self.bb_lower = calculate_bollinger_bands(prices)
        self.trend = calculate_trend(prices)
    
    def rsi_signal(self):
        if self.rsi is None or len(self.rsi) == 0:
            return 50
        current_rsi = self.rsi[-1]
        if current_rsi > 70:
            return 20
        elif current_rsi < 30:
            return 80
        else:
            return 50
    
    def macd_signal(self):
        if self.histogram is None or len(self.histogram) == 0:
            return 50
        if self.histogram[-1] > 0:
            return 70 if self.histogram[-1] > self.histogram[-2] else 50
        else:
            return 30 if self.histogram[-1] < self.histogram[-2] else 50
    
    def bollinger_signal(self):
        if self.prices is None or len(self.prices) == 0:
            return 50
        current_price = self.prices[-1]
        if current_price > self.bb_upper[-1]:
            return 30
        elif current_price < self.bb_lower[-1]:
            return 70
        else:
            return 50
    
    def trend_signal(self):
        if self.trend is None or len(self.trend) == 0:
            return 50
        current_trend = self.trend[-1]
        if current_trend > 0:
            return 70
        elif current_trend < 0:
            return 30
        else:
            return 50

class SmartSignals:
    def __init__(self, prices):
        self.rules = TradingRules(prices)
    
    def get_composite_signal(self):
        rsi_score = self.rules.rsi_signal()
        macd_score = self.rules.macd_signal()
        bb_score = self.rules.bollinger_signal()
        trend_score = self.rules.trend_signal()
        
        composite = (rsi_score + macd_score + bb_score + trend_score) / 4
        return composite
    
    def get_signal_text(self):
        score = self.get_composite_signal()
        if score >= 80:
            return "STRONG BUY"
        elif score >= 60:
            return "BUY"
        elif score >= 40:
            return "NEUTRAL"
        elif score >= 20:
            return "SELL"
        else:
            return "STRONG SELL"
    
    def get_detailed_signals(self):
        return {
            "rsi": self.rules.rsi_signal(),
            "macd": self.rules.macd_signal(),
            "bollinger": self.rules.bollinger_signal(),
            "trend": self.rules.trend_signal(),
            "composite": self.get_composite_signal(),
            "signal": self.get_signal_text()
        }

class RiskAssessment:
    def __init__(self, prices, period=50):
        self.prices = prices
        self.period = period
    
    def find_support(self):
        if len(self.prices) < self.period:
            return self.prices.min()
        return self.prices[-self.period:].min()
    
    def find_resistance(self):
        if len(self.prices) < self.period:
            return self.prices.max()
        return self.prices[-self.period:].max()
    
    def calculate_risk_reward(self, entry_price=None):
        if entry_price is None:
            entry_price = self.prices[-1]
        
        support = self.find_support()
        resistance = self.find_resistance()
        
        risk = entry_price - support
        reward = resistance - entry_price
        
        ratio = reward / risk if risk > 0 else 0
        
        return {
            "entry": entry_price,
            "support": support,
            "resistance": resistance,
            "risk": risk,
            "reward": reward,
            "ratio": ratio
        }
