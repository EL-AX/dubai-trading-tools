#!/usr/bin/env python3
"""
Test de Perfection - Vérifier tous les prix
"""
from src.data import get_live_price

cryptos = ['BTC', 'ETH', 'SOL', 'ADA', 'XRP', 'DOT']

print("=" * 60)
print("TEST: Tous les Cryptos Affichent les Prix Réels")
print("=" * 60)

for crypto in cryptos:
    price_info = get_live_price(crypto)
    price = price_info.get('price', 0)
    status = "✅" if price > 0 else "❌"
    print(f"{status} {crypto}: ${price:,.2f}")

print("=" * 60)
print("✅ Test complet!")
