"""© 2025-2026 ELOADXFAMILY - Tous droits réservés
Technical Indicators - RSI, MACD, Bollinger Bands, and more"""
import numpy as np
import pandas as pd

def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        # Retourner un array avec valeur neutre (50)
        return np.array([50] * len(prices)) if len(prices) > 0 else np.array([50])
    
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
    try:
        if prices is None or len(prices) == 0:
            return np.array([0]), np.array([0]), np.array([0])
        
        ema_fast = calculate_ema(prices, fast)
        ema_slow = calculate_ema(prices, slow)
        
        # Asegurar que no hay NaN
        ema_fast = np.nan_to_num(ema_fast, nan=np.mean(prices))
        ema_slow = np.nan_to_num(ema_slow, nan=np.mean(prices))
        
        macd_line = ema_fast - ema_slow
        signal_line = calculate_ema(macd_line, signal)
        signal_line = np.nan_to_num(signal_line, nan=0)
        
        histogram = macd_line - signal_line
        
        # Retourner arrays de même taille que l'input
        return (np.nan_to_num(macd_line, nan=0),
                np.nan_to_num(signal_line, nan=0),
                np.nan_to_num(histogram, nan=0))
    except Exception:
        # En cas d'erreur, retourner des arrays de zéros
        return np.zeros_like(prices), np.zeros_like(prices), np.zeros_like(prices)

def calculate_ema(prices, period):
    if len(prices) < period:
        # Retourner un array avec la moyenne des prix disponibles au lieu de NaN
        return np.full_like(prices, np.mean(prices) if len(prices) > 0 else 0, dtype=float)
    
    ema = np.zeros_like(prices, dtype=float)
    multiplier = 2 / (period + 1)
    
    ema[:period] = np.mean(prices[:period])
    
    for i in range(period, len(prices)):
        ema[i] = prices[i] * multiplier + ema[i - 1] * (1 - multiplier)
    
    return ema

def calculate_bollinger_bands(prices, period=20, std_dev=2):
    if len(prices) < period:
        # Retourner des arrays neutres si pas assez de données
        neutral = np.full_like(prices, prices[-1] if len(prices) > 0 else 0, dtype=float)
        return neutral, neutral * 1.02, neutral * 0.98
    
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
        # Retourner un array de volatilité neutre (0.02)
        return np.full_like(prices, 0.02, dtype=float)
    
    returns = np.diff(np.log(prices))
    volatility = np.zeros_like(prices)
    
    for i in range(period - 1, len(prices)):
        volatility[i] = np.std(returns[i - period + 1:i + 1])
    
    return volatility

def calculate_trend(prices, period=20):
    """Calcule la tendance sur les prix
    
    Retourne:
    - Array de -1 (baissier), 0 (neutre), 1 (haussier) pour chaque prix
    - Retourne TOUJOURS un array (jamais vide)
    """
    if prices is None or len(prices) == 0:
        return np.array([0])  # Retourner au minimum [0]
    
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
    
    return trend if len(trend) > 0 else np.array([0])  # Garantir non-vide
