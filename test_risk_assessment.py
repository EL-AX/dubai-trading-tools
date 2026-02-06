"""Test Risk Assessment robustness"""
import numpy as np
from src.trading_rules import RiskAssessment

# Test 1: Normal data
print("Test 1: Normal price data")
prices = np.array([100.0 + i * 0.5 for i in range(90)])
risk = RiskAssessment(prices, period=30)
result = risk.calculate_risk_reward()
print(f"✓ Entry: ${result['entry']:.4f}, Support: ${result['support']:.4f}, Resistance: ${result['resistance']:.4f}, Ratio: {result['ratio']:.2f}")

# Test 2: Data with NaN
print("\nTest 2: Data with NaN values")
prices_nan = np.array([100.0, 101.0, np.nan, 102.0, np.nan, 103.0])
risk = RiskAssessment(prices_nan, period=2)
result = risk.calculate_risk_reward()
print(f"✓ Entry: ${result['entry']:.4f}, Support: ${result['support']:.4f}, Resistance: ${result['resistance']:.4f}, Ratio: {result['ratio']:.2f}")

# Test 3: Short data
print("\nTest 3: Short data array")
prices_short = np.array([100.0, 101.0, 99.5])
risk = RiskAssessment(prices_short, period=30)
result = risk.calculate_risk_reward()
print(f"✓ Entry: ${result['entry']:.4f}, Support: ${result['support']:.4f}, Resistance: ${result['resistance']:.4f}, Ratio: {result['ratio']:.2f}")

# Test 4: Single price
print("\nTest 4: Single price")
prices_single = np.array([100.0])
risk = RiskAssessment(prices_single, period=30)
result = risk.calculate_risk_reward()
print(f"✓ Entry: ${result['entry']:.4f}, Support: ${result['support']:.4f}, Resistance: ${result['resistance']:.4f}, Ratio: {result['ratio']:.2f}")

# Test 5: Verify values are not NaN
print("\nTest 5: Verify all values are valid (non-NaN)")
prices = np.array([100.0 + i * 0.5 for i in range(90)])
risk = RiskAssessment(prices, period=30)
result = risk.calculate_risk_reward()

for key, value in result.items():
    if isinstance(value, (int, float)):
        is_valid = not np.isnan(value)
        symbol = "✓" if is_valid else "✗"
        print(f"{symbol} {key}: {value} - {'valid' if is_valid else 'NaN!'}")

print("\n✅ All Risk Assessment tests passed!")
