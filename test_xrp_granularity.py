"""Test XRP data granularity - verify hourly candles"""
import sys
sys.path.insert(0, '.')

from src.data import get_historical_data
import numpy as np
import pandas as pd

print("=" * 60)
print("Testing XRP Data Granularity and Indicators")
print("=" * 60)

# Test 1: Check data granularity
print("\n✓ Test 1: Data Granularity for XRP (1 day)")
try:
    data = get_historical_data('XRP', days=1)
    print(f"  - Rows returned: {len(data)}")
    print(f"  - Expected: ~24 (hourly candles)")
    
    if len(data) >= 20 and len(data) <= 30:
        print(f"  ✅ PASS: Got {len(data)} candles (expected ~24)")
    else:
        print(f"  ⚠️  WARNING: Got {len(data)} candles instead of ~24")
    
    # Check columns
    required_cols = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    missing = [c for c in required_cols if c not in data.columns]
    if not missing:
        print(f"  ✅ All required columns present: {required_cols}")
    else:
        print(f"  ❌ Missing columns: {missing}")
    
    # Check data types
    print(f"\n  Data types:")
    for col in ['open', 'high', 'low', 'close']:
        dtype = data[col].dtype
        try:
            test_val = float(data[col].iloc[0])
            print(f"    - {col}: {dtype} ✓")
        except:
            print(f"    - {col}: {dtype} ❌ (cannot convert to float)")
    
    # Check OHLC relationships
    print(f"\n  OHLC Relationships:")
    for idx, row in data.tail(3).iterrows():
        valid = (row['low'] <= row['open'] and 
                row['low'] <= row['close'] and 
                row['high'] >= row['open'] and 
                row['high'] >= row['close'])
        symbol = "✓" if valid else "❌"
        print(f"    {symbol} Row {idx}: Open={row['open']:.4f}, High={row['high']:.4f}, Low={row['low']:.4f}, Close={row['close']:.4f}")
    
except Exception as e:
    print(f"  ❌ ERROR: {e}")

# Test 2: Check 90-day data
print("\n✓ Test 2: Data Granularity for XRP (90 days)")
try:
    data = get_historical_data('XRP', days=90)
    print(f"  - Rows returned: {len(data)}")
    print(f"  - Expected: ~{90*24} (hourly candles)")
    
    expected_min = 90 * 24 * 0.8  # Allow 20% variation
    expected_max = 90 * 24 * 1.2
    if len(data) >= expected_min and len(data) <= expected_max:
        print(f"  ✅ PASS: Got {len(data)} candles")
    else:
        print(f"  ⚠️  WARNING: Expected {90*24} candles, got {len(data)}")
        
except Exception as e:
    print(f"  ❌ ERROR: {e}")

# Test 3: Check other cryptos for consistency
print("\n✓ Test 3: Data Granularity for Other Cryptos (1 day)")
for ticker in ['BTC', 'ETH', 'SOL', 'ADA']:
    try:
        data = get_historical_data(ticker, days=1)
        expected = 24
        actual = len(data)
        status = "✅" if 20 <= actual <= 30 else "⚠️"
        print(f"  {status} {ticker}: {actual} candles")
    except Exception as e:
        print(f"  ❌ {ticker}: ERROR - {e}")

print("\n" + "=" * 60)
print("✅ XRP Data Granularity Tests Complete")
print("=" * 60)
