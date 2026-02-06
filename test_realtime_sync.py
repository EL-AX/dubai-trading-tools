"""Test real-time data synchronization"""
import sys
sys.path.insert(0, '.')

from src.data import get_live_price, get_historical_data
from src.indicators import calculate_rsi
from src.trading_rules import SmartSignals, RiskAssessment
import numpy as np

print("=" * 60)
print("Testing Real-Time Data Synchronization")
print("=" * 60)

tickers = ["BTC", "ETH", "EUR", "XAU"]

for ticker in tickers:
    print(f"\n✓ Testing {ticker}:")
    try:
        # Get live price
        live_data = get_live_price(ticker)
        live_price = live_data.get('price', 0) if isinstance(live_data, dict) else float(live_data)
        
        print(f"  Live Price: ${live_price:.4f}")
        
        # Get historical data
        hist_data = get_historical_data(ticker, days=30)
        if hist_data is not None and len(hist_data) > 0:
            hist_price = hist_data['close'].iloc[-1]
            print(f"  Last Historical: ${hist_price:.4f}")
            
            # Check sync
            diff = abs(hist_price - live_price) / live_price * 100
            if diff > 5:
                print(f"  ⚠️  WARNING: Prices differ by {diff:.2f}%")
            else:
                print(f"  ✅ Prices synchronized (diff: {diff:.2f}%)")
            
            # Calculate signals
            prices = hist_data['close'].values
            prices = np.nan_to_num(prices, nan=live_price)
            prices[-1] = live_price  # Sync
            
            smart_signals = SmartSignals(prices)
            signals = smart_signals.get_detailed_signals()
            
            print(f"  Signals:")
            print(f"    - RSI: {signals['rsi']:.1f}")
            print(f"    - MACD: {signals['macd']:.4f}")
            print(f"    - Bollinger: {signals['bollinger']:.1f}")
            print(f"    - Trend: {signals['trend']:.1f}")
            print(f"    - Signal: {signals['signal']}")
            
            # Check for NaN
            has_nan = False
            for key, val in signals.items():
                if isinstance(val, (int, float)) and np.isnan(val):
                    print(f"    ❌ {key} is NaN!")
                    has_nan = True
            
            if not has_nan:
                print(f"    ✅ All signals are valid (no NaN)")
        else:
            print(f"  ❌ No historical data available")
            
    except Exception as e:
        print(f"  ❌ ERROR: {e}")

print("\n" + "=" * 60)
print("✅ Real-Time Synchronization Test Complete")
print("=" * 60)
