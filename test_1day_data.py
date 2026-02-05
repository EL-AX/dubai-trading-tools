#!/usr/bin/env python
"""Test 1 jour de données pour tous les actifs"""

from src.data import get_historical_data

actifs = ["BTC", "ETH", "EUR", "GBP", "XAU"]

print("=" * 70)
print("TEST: 1 JOUR DE FLUCTUATION POUR TOUS LES ACTIFS")
print("=" * 70)

for ticker in actifs:
    print(f"\n{ticker}:")
    data = get_historical_data(ticker, days=1)
    
    print(f"   Nombre de candles: {len(data)}")
    if len(data) > 0:
        print(f"   Première ligne: {data.iloc[0]}")
        print(f"   Dernière ligne: {data.iloc[-1]}")
        print(f"   Colonnes: {list(data.columns)}")
    else:
        print(f"   ⚠️ AUCUNE DONNÉE")

print("\n" + "=" * 70)
print("✅ Test complet")
print("=" * 70)
