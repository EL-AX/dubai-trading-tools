#!/usr/bin/env python3
"""Debug EUR data generation"""

import sys
sys.path.insert(0, '.')

from src.data import get_historical_data, generate_and_sync_mock_data, fetch_forex_historical
import pandas as pd

print("="*60)
print("Testing EUR data generation")
print("="*60)

# Try fetch_forex_historical directly
print("\n1. Testing fetch_forex_historical():")
try:
    forex_data = fetch_forex_historical("EUR", 90)
    if forex_data is not None and not forex_data.empty:
        print(f"   Shape: {forex_data.shape}")
        print(f"   Min close: {forex_data['close'].min():.4f}")
        print(f"   Max close: {forex_data['close'].max():.4f}")
        print(f"   Last close: {forex_data['close'].iloc[-1]:.4f}")
        print(f"   Sample:\n{forex_data[['timestamp', 'close']].head()}")
    else:
        print("   Returned None or empty")
except Exception as e:
    print(f"   ERROR: {e}")

# Try generate_and_sync_mock_data
print("\n2. Testing generate_and_sync_mock_data('EUR', 90):")
try:
    mock_data = generate_and_sync_mock_data("EUR", 90)
    print(f"   Shape: {mock_data.shape}")
    print(f"   Min close: {mock_data['close'].min():.4f}")
    print(f"   Max close: {mock_data['close'].max():.4f}")
    print(f"   Last close: {mock_data['close'].iloc[-1]:.4f}")
    print(f"   Sample:\n{mock_data[['timestamp', 'close']].head()}")
except Exception as e:
    print(f"   ERROR: {e}")

# Get full historical
print("\n3. Testing get_historical_data('EUR', 90):")
try:
    hist_data = get_historical_data("EUR", 90)
    print(f"   Shape: {hist_data.shape}")
    print(f"   Min close: {hist_data['close'].min():.4f}")
    print(f"   Max close: {hist_data['close'].max():.4f}")
    print(f"   Last close: {hist_data['close'].iloc[-1]:.4f}")
    print(f"   Sample:\n{hist_data[['timestamp', 'close']].head()}")
    print(f"   Tail:\n{hist_data[['timestamp', 'close']].tail()}")
except Exception as e:
    print(f"   ERROR: {e}")
