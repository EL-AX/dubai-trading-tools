"""Quick test to verify all indicators and trading rules work robustly"""
import numpy as np
from src.indicators import calculate_rsi, calculate_macd, calculate_bollinger_bands, calculate_trend
from src.trading_rules import TradingRules, SmartSignals

# Test 1: Empty array
print("Test 1: Empty array")
try:
    empty_prices = np.array([])
    signals = SmartSignals(empty_prices)
    result = signals.get_detailed_signals()
    print(f"✓ Empty array handled: {result}")
except Exception as e:
    print(f"✗ Failed with empty array: {e}")

# Test 2: Single price
print("\nTest 2: Single price")
try:
    single_price = np.array([100.0])
    signals = SmartSignals(single_price)
    result = signals.get_detailed_signals()
    print(f"✓ Single price handled: {result}")
    assert result['rsi'] == 50, "RSI should be 50 for single price"
    assert result['trend'] == 0, "Trend should be 0 for single price"
except Exception as e:
    print(f"✗ Failed with single price: {e}")

# Test 3: Short price array (less than required period)
print("\nTest 3: Short price array")
try:
    short_prices = np.array([100.0, 101.0, 99.5, 102.0])
    signals = SmartSignals(short_prices)
    result = signals.get_detailed_signals()
    print(f"✓ Short array handled: {result}")
    assert isinstance(result['rsi'], (int, float)), "RSI must be numeric"
    assert isinstance(result['macd'], (int, float)), "MACD must be numeric"
    assert isinstance(result['bollinger'], (int, float)), "Bollinger must be numeric"
    assert isinstance(result['trend'], (int, float)), "Trend must be numeric"
    assert isinstance(result['signal'], str), "Signal must be string"
except Exception as e:
    print(f"✗ Failed with short array: {e}")

# Test 4: Normal price array
print("\nTest 4: Normal price array (30 prices)")
try:
    prices = np.array([100.0 + i * 0.5 for i in range(30)])
    signals = SmartSignals(prices)
    result = signals.get_detailed_signals()
    print(f"✓ Normal array handled: {result}")
    assert 0 <= result['rsi'] <= 100, "RSI must be between 0 and 100"
    assert -100 <= result['bollinger'] <= 100, "Bollinger must be between -100 and 100"
    assert isinstance(result['trend'], (int, float)), "Trend must be numeric"
    assert result['signal'] in ["STRONG BUY", "BUY", "NEUTRAL", "SELL", "STRONG SELL"], "Invalid signal"
except Exception as e:
    print(f"✗ Failed with normal array: {e}")

# Test 5: Array with NaN values
print("\nTest 5: Array with NaN values")
try:
    prices_with_nan = np.array([100.0, 101.0, np.nan, 102.0])
    signals = SmartSignals(prices_with_nan)
    result = signals.get_detailed_signals()
    print(f"✓ Array with NaN handled: {result}")
    # Verify no NaN in output
    for key, value in result.items():
        if isinstance(value, (int, float)):
            assert not np.isnan(value), f"{key} contains NaN: {value}"
except Exception as e:
    print(f"✗ Failed with NaN array: {e}")

# Test 6: Test signal text generation
print("\nTest 6: Signal text generation")
try:
    prices = np.array([100.0 + i * 0.5 for i in range(30)])
    signals = SmartSignals(prices)
    signal_text = signals.get_signal_text()
    print(f"✓ Signal text: {signal_text}")
    assert signal_text in ["STRONG BUY", "BUY", "NEUTRAL", "SELL", "STRONG SELL"], "Invalid signal text"
except Exception as e:
    print(f"✗ Failed signal text generation: {e}")

# Test 7: Individual indicators
print("\nTest 7: Individual indicators")
try:
    prices = np.array([100.0 + i * 0.5 for i in range(30)])
    
    # RSI
    rsi = calculate_rsi(prices)
    assert rsi is not None, "RSI should not be None"
    assert len(rsi) > 0, "RSI should not be empty"
    assert not np.isnan(rsi[-1]), "RSI last value should not be NaN"
    print(f"✓ RSI: {rsi[-1]:.2f}")
    
    # MACD
    macd, signal, histogram = calculate_macd(prices)
    assert macd is not None and len(macd) > 0, "MACD should be valid"
    assert signal is not None and len(signal) > 0, "Signal should be valid"
    assert histogram is not None and len(histogram) > 0, "Histogram should be valid"
    print(f"✓ MACD: {macd[-1]:.4f}, Signal: {signal[-1]:.4f}, Histogram: {histogram[-1]:.4f}")
    
    # Bollinger Bands
    mid, upper, lower = calculate_bollinger_bands(prices)
    assert mid is not None and len(mid) > 0, "BB Mid should be valid"
    assert upper is not None and len(upper) > 0, "BB Upper should be valid"
    assert lower is not None and len(lower) > 0, "BB Lower should be valid"
    print(f"✓ Bollinger: Mid={mid[-1]:.2f}, Upper={upper[-1]:.2f}, Lower={lower[-1]:.2f}")
    
    # Trend
    trend = calculate_trend(prices)
    assert trend is not None, "Trend should not be None"
    assert len(trend) > 0, "Trend should not be empty"
    assert not np.isnan(trend[-1]), "Trend last value should not be NaN"
    print(f"✓ Trend: {trend[-1]}")
    
except Exception as e:
    print(f"✗ Failed individual indicators test: {e}")

print("\n" + "="*50)
print("All tests completed!")
print("="*50)
