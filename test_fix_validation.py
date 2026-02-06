#!/usr/bin/env python3
"""Test to validate the RiskAssessment and data fixes - Windows compatible version"""

import sys
sys.path.insert(0, '/content/src')

import numpy as np
import pandas as pd
from src.data import get_historical_data, get_live_price
from src.trading_rules import RiskAssessment

def test_asset(ticker, days=90):
    """Test a single asset"""
    print("\n" + "="*60)
    print(f"Testing {ticker} ({days} days)")
    print("="*60)
    
    # Get live price
    live_price_data = get_live_price(ticker)
    live_price = live_price_data.get('price', 0) if isinstance(live_price_data, dict) else live_price_data
    print(f"Live price from API: ${live_price:.4f}")
    
    # Get historical data
    hist_data = get_historical_data(ticker, days=days)
    
    if hist_data is None or len(hist_data) == 0:
        print(f"FAIL: No historical data available")
        return False
    
    print(f"Historical data shape: {hist_data.shape}")
    print(f"Expected rows: {days * 24} (for hourly candles)")
    print(f"Actual rows: {len(hist_data)}")
    
    prices = hist_data['close'].values
    
    print(f"\nPrice range:")
    print(f"  Min: ${np.min(prices):.4f}")
    print(f"  Max: ${np.max(prices):.4f}")
    print(f"  Mean: ${np.mean(prices):.4f}")
    print(f"  Last (should match live): ${prices[-1]:.4f}")
    
    # Check if price matches live
    price_diff = abs(prices[-1] - live_price)
    price_diff_pct = (price_diff / live_price * 100) if live_price > 0 else 0
    print(f"  Difference from live: ${price_diff:.4f} ({price_diff_pct:.2f}%)")
    
    # Test RiskAssessment
    period = min(30, len(prices) // 3)
    print(f"\nRiskAssessment with period={period}:")
    
    risk_assessment = RiskAssessment(prices, period=period)
    risk_data = risk_assessment.calculate_risk_reward()
    
    print(f"  Entry: ${risk_data['entry']:.4f}")
    print(f"  Support: ${risk_data['support']:.4f}")
    print(f"  Resistance: ${risk_data['resistance']:.4f}")
    print(f"  Risk: ${risk_data['risk']:.4f}")
    print(f"  Reward: ${risk_data['reward']:.4f}")
    print(f"  Ratio: {risk_data['ratio']:.2f}")
    
    # Validation
    valid = True
    
    # Check if price is reasonable for the asset
    if ticker in ["BTC", "ETH", "SOL", "ADA", "XRP", "DOT"]:
        # Crypto should be in normal range
        if prices[-1] < 0.01 or prices[-1] > 1000000:
            print(f"  WARNING: Price seems out of range for {ticker}")
            valid = False
    elif ticker in ["EUR", "GBP", "JPY", "AUD"]:
        # Forex should be < 1000
        if prices[-1] < 0.0001 or prices[-1] > 10000:
            print(f"  WARNING: Price seems out of range for {ticker}")
            valid = False
    elif ticker == "XAU":
        # Gold should be reasonable
        if prices[-1] < 500 or prices[-1] > 5000:
            print(f"  WARNING: Price seems out of range for {ticker}")
            valid = False
    
    # Check support < entry < resistance
    if not (risk_data['support'] < risk_data['entry'] < risk_data['resistance']):
        print(f"  FAIL: Support/Entry/Resistance order is wrong")
        valid = False
    else:
        print(f"  OK: Support < Entry < Resistance order is correct")
    
    # Check if ratio is meaningful (not 0 or N/A)
    if risk_data['ratio'] < 0.01:
        print(f"  WARNING: Ratio is very low ({risk_data['ratio']:.4f})")
    else:
        print(f"  OK: Ratio is meaningful ({risk_data['ratio']:.2f})")
    
    # Check if we have sufficient data
    if len(hist_data) < (days * 24 * 0.8):  # At least 80% of expected
        print(f"  WARNING: Not enough historical data ({len(hist_data)} < {days * 24 * 0.8})")
        valid = False
    else:
        print(f"  OK: Sufficient historical data")
    
    return valid

# Test all assets
print("\n" + "="*60)
print("TESTING ALL ASSETS")
print("="*60)

tickers = ["BTC", "ETH", "EUR", "XAU"]
results = {}

for ticker in tickers:
    try:
        results[ticker] = test_asset(ticker, days=90)
    except Exception as e:
        print(f"\nFAIL: Error testing {ticker}: {str(e)}")
        results[ticker] = False

# Summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
for ticker, passed in results.items():
    status = "PASS" if passed else "FAIL"
    print(f"{ticker}: {status}")

all_passed = all(results.values())
print("\n" + ("All tests passed!" if all_passed else "Some tests failed"))
