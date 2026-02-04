"""© 2025-2026 ELOADXFAMILY - Tous droits réservés
Technical Indicators - RSI, MACD, Bollinger Bands, and more"""
import numpy as np
import pandas as pd

def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return None
    
    deltas = np.diff(prices)
    seed = deltas[:period+1]
    up = seed[seed >= 0].sum() / period
    down = -seed[seed < 0].sum() / period
    
    rs = up / down if down != 0 else 0
    rsi = 100 - 100 / (1 + rs) if rs >= 0 else 0
    
    rsis = np.zeros_like(prices)
    rsis[period] = rsi
    
    for i in range(period + 1, len(prices)):
        delta = deltas[i - 1]
        if delta > 0:
            up = (up * (period - 1) + delta) / period
            down = down * (period - 1) / period
        else:
            up = up * (period - 1) / period
            down = (down * (period - 1) - delta) / period
        
        rs = up / down if down != 0 else 0
        rsis[i] = 100 - 100 / (1 + rs) if rs >= 0 else 0
    
    return rsis

def calculate_macd(prices, fast=12, slow=26, signal=9):
    ema_fast = calculate_ema(prices, fast)
    ema_slow = calculate_ema(prices, slow)
    macd_line = ema_fast - ema_slow
    signal_line = calculate_ema(macd_line, signal)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def calculate_ema(prices, period):
    if len(prices) < period:
        return np.array([np.nan] * len(prices))
    
    ema = np.zeros_like(prices)
    multiplier = 2 / (period + 1)
    
    ema[:period] = np.mean(prices[:period])
    
    for i in range(period, len(prices)):
        ema[i] = prices[i] * multiplier + ema[i - 1] * (1 - multiplier)
    
    return ema

def calculate_bollinger_bands(prices, period=20, std_dev=2):
    if len(prices) < period:
        return None, None, None
    
    sma = np.convolve(prices, np.ones(period) / period, mode='valid')
    pad = len(prices) - len(sma)
    sma = np.pad(sma, (pad, 0), mode='edge')
    
    deviations = np.zeros_like(prices)
    for i in range(period - 1, len(prices)):
        deviations[i] = np.std(prices[i - period + 1:i + 1])
    
    upper_band = sma + (deviations * std_dev)
    lower_band = sma - (deviations * std_dev)
    
    return sma, upper_band, lower_band

def calculate_volatility(prices, period=20):
    if len(prices) < period:
        return None
    
    returns = np.diff(np.log(prices))
    volatility = np.zeros_like(prices)
    
    for i in range(period - 1, len(prices)):
        volatility[i] = np.std(returns[i - period + 1:i + 1])
    
    return volatility

def calculate_trend(prices, period=20):
    """Calcule la tendance sur les prix
    
    Retourne:
    - Array de -1 (baissier), 0 (neutre), 1 (haussier) pour chaque prix
    - [] si pas assez de données (fallback gracieux)
    """
    if prices is None or len(prices) == 0:
        return []
    
    # Adapter la période si pas assez de données
    if len(prices) < period:
        period = max(2, len(prices) // 2)
    
    trend = np.zeros(len(prices), dtype=int)
    
    # Remplir les premières valeurs avec la tendance simple (prix montant/baissant)
    for i in range(1, min(period, len(prices))):
        if prices[i] > prices[i-1]:
            trend[i] = 1
        elif prices[i] < prices[i-1]:
            trend[i] = -1
        else:
            trend[i] = 0
    
    # Calculer la tendance sur la période complète pour les données restantes
    for i in range(period, len(prices)):
        window = prices[i - period + 1:i + 1]
        if len(window) > 0:
            slope = (window[-1] - window[0]) / len(window)
            trend[i] = 1 if slope > 0 else (-1 if slope < 0 else 0)
    
    return trend
