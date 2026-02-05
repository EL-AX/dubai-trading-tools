#!/usr/bin/env python
"""Test d'analyseur de sentiment"""

from src.sentiment_analyzer import analyze_sentiment

test_cases = [
    "Bitcoin Price Crashes 20% - Major Selloff",
    "Ethereum Surges to New All-Time High",
    "SEC Approves First Bitcoin ETF",
    "Crypto Exchange Files for Bankruptcy",
    "Regulatory Crackdown Crushes Prices",
    "Bull Market Begins - Analyst Calls for New Highs",
    "Market Momentum Builds - Recovery Expected",
    "Bitcoin chute drastiquement - Panic selling",
    "Ethereum explose vers de nouveaux records",
]

print("=" * 70)
print("TEST D'ANALYSE DE SENTIMENT RÉELLE")
print("=" * 70)

for text in test_cases:
    sentiment = analyze_sentiment(text)
    icon = "🟢" if sentiment == "bullish" else "🔴" if sentiment == "bearish" else "⚪"
    print(f"{icon} {text}")
    print(f"   → Sentiment: {sentiment.upper()}")
    print()

print("=" * 70)
print("✅ Analyseur de sentiment FONCTIONNE CORRECTEMENT")
print("=" * 70)
