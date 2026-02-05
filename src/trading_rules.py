"""© 2025-2026 ELOADXFAMILY - Tous droits réservés
Trading Rules & Risk Management - Core trading logic"""
import numpy as np
from src.indicators import calculate_rsi, calculate_macd, calculate_bollinger_bands, calculate_trend

class TradingRules:
    def __init__(self, prices):
        try:
            self.prices = np.array(prices) if prices is not None else np.array([])
            self.rsi = calculate_rsi(self.prices)
            self.macd, self.signal, self.histogram = calculate_macd(self.prices)
            self.bb_mid, self.bb_upper, self.bb_lower = calculate_bollinger_bands(self.prices)
            self.trend = calculate_trend(self.prices)
            
            # Asegurar que todos los arrays son válidos (no None, no vacíos, no NaN)
            self._validate_arrays()
        except Exception:
            # En caso de error, inicializar con valores por defecto
            self.prices = np.array([])
            self.rsi = np.array([50])
            self.macd = np.array([0])
            self.signal = np.array([0])
            self.histogram = np.array([0])
            self.bb_mid = np.array([0])
            self.bb_upper = np.array([0])
            self.bb_lower = np.array([0])
            self.trend = np.array([0])
    
    def _validate_arrays(self):
        """Valider et corriger tous les arrays pour éviter NaN, None, ou vides"""
        # Corriger RSI
        if self.rsi is None or len(self.rsi) == 0:
            self.rsi = np.array([50])
        self.rsi = np.nan_to_num(self.rsi, nan=50)
        
        # Corriger MACD
        if self.macd is None or len(self.macd) == 0:
            self.macd = np.array([0])
        self.macd = np.nan_to_num(self.macd, nan=0)
        
        # Corriger Signal
        if self.signal is None or len(self.signal) == 0:
            self.signal = np.array([0])
        self.signal = np.nan_to_num(self.signal, nan=0)
        
        # Corriger Histogram
        if self.histogram is None or len(self.histogram) == 0:
            self.histogram = np.array([0])
        self.histogram = np.nan_to_num(self.histogram, nan=0)
        
        # Corriger Bollinger Bands
        if self.bb_mid is None or len(self.bb_mid) == 0:
            self.bb_mid = np.array([0])
        self.bb_mid = np.nan_to_num(self.bb_mid, nan=0)
        
        if self.bb_upper is None or len(self.bb_upper) == 0:
            self.bb_upper = np.array([0])
        self.bb_upper = np.nan_to_num(self.bb_upper, nan=0)
        
        if self.bb_lower is None or len(self.bb_lower) == 0:
            self.bb_lower = np.array([0])
        self.bb_lower = np.nan_to_num(self.bb_lower, nan=0)
        
        # Corriger Trend
        if self.trend is None or len(self.trend) == 0:
            self.trend = np.array([0])
        self.trend = np.nan_to_num(self.trend, nan=0)
    
    def rsi_signal(self):
        try:
            if self.rsi is None or len(self.rsi) == 0:
                return 50
            current_rsi = float(self.rsi[-1])
            if current_rsi > 70:
                return 20
            elif current_rsi < 30:
                return 80
            else:
                return 50
        except (TypeError, ValueError, IndexError):
            return 50
    
    def macd_signal(self):
        try:
            if self.histogram is None or len(self.histogram) == 0:
                return 50
            current = float(self.histogram[-1])
            if current > 0:
                previous = float(self.histogram[-2]) if len(self.histogram) > 1 else current
                return 70 if current > previous else 50
            else:
                previous = float(self.histogram[-2]) if len(self.histogram) > 1 else current
                return 30 if current < previous else 50
        except (TypeError, ValueError, IndexError):
            return 50
    
    def bollinger_signal(self):
        try:
            if self.prices is None or len(self.prices) == 0:
                return 50
            current_price = float(self.prices[-1])
            upper = float(self.bb_upper[-1]) if self.bb_upper is not None and len(self.bb_upper) > 0 else current_price
            lower = float(self.bb_lower[-1]) if self.bb_lower is not None and len(self.bb_lower) > 0 else current_price
            
            if current_price > upper:
                return 30
            elif current_price < lower:
                return 70
            else:
                return 50
        except (TypeError, ValueError, IndexError):
            return 50
    
    def trend_signal(self):
        try:
            if self.trend is None or len(self.trend) == 0:
                return 50
            current_trend = float(self.trend[-1])
            if current_trend > 0:
                return 70
            elif current_trend < 0:
                return 30
            else:
                return 50
        except (TypeError, ValueError, IndexError):
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

    # Backwards-compatible alias
    def generate_composite_signal(self):
        return self.get_composite_signal()
    
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
        try:
            # Extraer RSI de forma segura
            rsi_val = 50
            if self.rules.rsi is not None and len(self.rules.rsi) > 0:
                rsi_val = float(self.rules.rsi[-1])
            rsi_val = np.nan_to_num(rsi_val, nan=50)
            
            # Extraer MACD de forma segura
            macd_val = 0
            if self.rules.histogram is not None and len(self.rules.histogram) > 0:
                macd_val = float(self.rules.histogram[-1])
            macd_val = np.nan_to_num(macd_val, nan=0)
            
            # Extraer Trend de forma segura
            trend_val = 0
            if self.rules.trend is not None and len(self.rules.trend) > 0:
                trend_val = float(self.rules.trend[-1])
            trend_val = np.nan_to_num(trend_val, nan=0)
            
            return {
                "rsi": rsi_val,
                "macd": macd_val,
                "bollinger": self._get_bollinger_position(),
                "trend": trend_val,
                "signal": self.get_signal_text()
            }
        except Exception:
            # En cas d'erreur, retourner des valeurs par défaut
            return {
                "rsi": 50,
                "macd": 0,
                "bollinger": 0,
                "trend": 0,
                "signal": "NEUTRAL"
            }
    
    def _get_bollinger_position(self):
        """Return position between Bollinger bands (-100 to 100)"""
        try:
            if self.rules.prices is None or len(self.rules.prices) == 0:
                return 0.0
            if self.rules.bb_upper is None or self.rules.bb_lower is None or len(self.rules.bb_upper) == 0:
                return 0.0
            
            current = float(self.rules.prices[-1])
            upper = float(self.rules.bb_upper[-1])
            lower = float(self.rules.bb_lower[-1])
            
            # Gérer les valeurs NaN
            if np.isnan(current) or np.isnan(upper) or np.isnan(lower):
                return 0.0
            
            if upper == lower:
                return 0.0
            
            # Position from lower (-100) to upper (+100)
            position = ((current - lower) / (upper - lower)) * 200 - 100
            result = float(np.clip(position, -100, 100))
            
            # Vérifier que le résultat n'est pas NaN
            if np.isnan(result):
                return 0.0
            
            return result
        except (TypeError, ValueError, IndexError):
            return 0.0

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
