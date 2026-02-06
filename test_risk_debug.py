"""Diagnose Risk Assessment issues"""
from src.data import get_historical_data, get_live_price
from src.trading_rules import RiskAssessment
import numpy as np

# Test BTC
print('Testing BTC 90 days:')
data = get_historical_data('BTC', days=90)
print(f'  Shape: {data.shape}')
print(f'  Expected: 90*24 = 2160 rows')
prices = data['close'].values
print(f'  Min price: {prices.min():.2f}')
print(f'  Max price: {prices.max():.2f}')
print(f'  Last price: {prices[-1]:.2f}')

# Test RiskAssessment
print('\nTesting RiskAssessment:')
ra = RiskAssessment(prices, period=30)
result = ra.calculate_risk_reward()
print(f'  Entry: {result["entry"]:.2f}')
print(f'  Support: {result["support"]:.2f}')
print(f'  Resistance: {result["resistance"]:.2f}')
print(f'  Risk: {result["risk"]:.2f}')
print(f'  Reward: {result["reward"]:.2f}')
print(f'  Ratio: {result["ratio"]:.2f}')

# Test EUR
print('\nTesting EUR 90 days:')
data = get_historical_data('EUR', days=90)
print(f'  Shape: {data.shape}')
prices = data['close'].values
print(f'  Min price: {prices.min():.4f}')
print(f'  Max price: {prices.max():.4f}')
print(f'  Last price: {prices[-1]:.4f}')

ra = RiskAssessment(prices, period=30)
result = ra.calculate_risk_reward()
print(f'  Entry: {result["entry"]:.4f}')
print(f'  Support: {result["support"]:.4f}')
print(f'  Resistance: {result["resistance"]:.4f}')
print(f'  Risk: {result["risk"]:.4f}')
print(f'  Reward: {result["reward"]:.4f}')
print(f'  Ratio: {result["ratio"]:.4f}')
