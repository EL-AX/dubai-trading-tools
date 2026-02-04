#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de synchronisation prix-graphes - TOUS les tickers
VALIDATION: Chaque dernière valeur historique = prix actuel (tolerance 2%)
"""

import sys
import pandas as pd
from src.data import (
    fetch_gold_historical, fetch_coingecko_ohlc, fetch_forex_historical,
    get_gold_price, get_live_price, get_crypto_price, get_forex_price
)

def test_price_sync():
    """Test that historical data last close ≈ live price for ALL tickers"""
    
    # ALL tickers in the application
    all_tickers = {
        "CRYPTO": ["BTC", "ETH", "SOL", "ADA", "XRP", "DOT"],
        "FOREX": ["EUR", "GBP", "JPY", "AUD"],
        "COMMODITIES": ["XAU"]
    }
    
    results = {}
    
    print("\n" + "="*70)
    print("SYNCHRONISATION COMPLÈTE - TOUS LES TICKERS")
    print("="*70)
    
    # Test CRYPTO
    print("\n" + "="*70)
    print("🔐 CRYPTO (Bitcoin, Ethereum, Solana, Cardano, Ripple, Polkadot)")
    print("="*70)
    
    for ticker in all_tickers["CRYPTO"]:
        results[ticker] = {"historical": None, "live": None, "sync": False}
        print(f"\n▶ {ticker}")
        try:
            crypto_data = fetch_coingecko_ohlc(ticker, days=30)
            live_crypto_data = get_crypto_price(ticker)
            live_crypto = live_crypto_data.get('price', 0) if isinstance(live_crypto_data, dict) else live_crypto_data
            
            if len(crypto_data) > 0:
                last_historical = crypto_data.iloc[-1]['close']
                
                results[ticker]["historical"] = last_historical
                results[ticker]["live"] = live_crypto
                
                if live_crypto > 0:
                    diff_pct = abs(last_historical - live_crypto) / live_crypto * 100
                    is_synced = diff_pct < 2.0
                    results[ticker]["sync"] = is_synced
                    
                    print(f"  ✓ Dernier prix historique: ${last_historical:.2f}")
                    print(f"  ✓ Prix actuel (API):       ${live_crypto:.2f}")
                    print(f"  ✓ Différence:              {diff_pct:.2f}%")
                    print(f"  ✓ Synchronisé?            {'OUI ✓' if is_synced else 'NON ✗'}")
            else:
                print("  ✗ Pas de données historiques")
        except Exception as e:
            print(f"  ✗ Erreur: {str(e)}")
    
    # Test FOREX
    print("\n" + "="*70)
    print("💱 FOREX (Euro, Livre Sterling, Yen, Dollar Australien)")
    print("="*70)
    
    for ticker in all_tickers["FOREX"]:
        results[ticker] = {"historical": None, "live": None, "sync": False}
        print(f"\n▶ {ticker}")
        try:
            forex_data = fetch_forex_historical(ticker, days=30)
            
            if len(forex_data) > 0:
                last_historical = forex_data.iloc[-1]['close']
                
                # Get live forex price
                live_forex_data = get_forex_price(ticker)
                live_forex = live_forex_data.get('price', 0) if isinstance(live_forex_data, dict) else live_forex_data
                
                results[ticker]["historical"] = last_historical
                results[ticker]["live"] = live_forex
                
                if live_forex > 0:
                    diff_pct = abs(last_historical - live_forex) / live_forex * 100
                    is_synced = diff_pct < 2.0
                    results[ticker]["sync"] = is_synced
                    
                    print(f"  ✓ Dernier prix historique: ${last_historical:.4f}")
                    print(f"  ✓ Prix actuel (API):       ${live_forex:.4f}")
                    print(f"  ✓ Différence:              {diff_pct:.2f}%")
                    print(f"  ✓ Synchronisé?            {'OUI ✓' if is_synced else 'NON ✗'}")
            else:
                print("  ✗ Pas de données historiques")
        except Exception as e:
            print(f"  ✗ Erreur: {str(e)}")
    
    # Test COMMODITIES
    print("\n" + "="*70)
    print("⭐ MATIÈRES PREMIÈRES (Or)")
    print("="*70)
    
    for ticker in all_tickers["COMMODITIES"]:
        results[ticker] = {"historical": None, "live": None, "sync": False}
        print(f"\n▶ {ticker}")
        try:
            gold_data = fetch_gold_historical(days=30)
            live_gold = get_gold_price()
            
            if len(gold_data) > 0:
                last_historical = gold_data.iloc[-1]['close']
                live_price = live_gold.get('price', 0) if isinstance(live_gold, dict) else live_gold
                
                results[ticker]["historical"] = last_historical
                results[ticker]["live"] = live_price
                
                if live_price > 0:
                    diff_pct = abs(last_historical - live_price) / live_price * 100
                    is_synced = diff_pct < 2.0
                    results[ticker]["sync"] = is_synced
                    
                    print(f"  ✓ Dernier prix historique: ${last_historical:.2f}")
                    print(f"  ✓ Prix actuel (API):       ${live_price:.2f}")
                    print(f"  ✓ Différence:              {diff_pct:.2f}%")
                    print(f"  ✓ Synchronisé?            {'OUI ✓' if is_synced else 'NON ✗'}")
            else:
                print("  ✗ Pas de données historiques")
        except Exception as e:
            print(f"  ✗ Erreur: {str(e)}")
    
    # Summary
    print("\n" + "="*70)
    print("📊 RÉSUMÉ GLOBAL DE SYNCHRONISATION")
    print("="*70)
    
    synced_count = sum(1 for r in results.values() if r["sync"])
    total_count = len(results)
    
    print(f"\n🔐 CRYPTO ({len([r for k, r in results.items() if k in all_tickers['CRYPTO']])} tickers):")
    for ticker in all_tickers["CRYPTO"]:
        status = "✓ SYNCED" if results[ticker]["sync"] else "✗ OUT OF SYNC"
        print(f"  {ticker}: {status}")
    
    print(f"\n💱 FOREX ({len([r for k, r in results.items() if k in all_tickers['FOREX']])} tickers):")
    for ticker in all_tickers["FOREX"]:
        status = "✓ SYNCED" if results[ticker]["sync"] else "✗ OUT OF SYNC"
        print(f"  {ticker}: {status}")
    
    print(f"\n⭐ COMMODITIES ({len([r for k, r in results.items() if k in all_tickers['COMMODITIES']])} tickers):")
    for ticker in all_tickers["COMMODITIES"]:
        status = "✓ SYNCED" if results[ticker]["sync"] else "✗ OUT OF SYNC"
        print(f"  {ticker}: {status}")
    
    print(f"\n{'='*70}")
    print(f"TOTAL: {synced_count}/{total_count} tickers synchronisés")
    print(f"{'='*70}")
    
    if synced_count == total_count:
        print("\n✓✓✓ TOUS LES PRIX SONT PARFAITEMENT SYNCHRONISÉS! ✓✓✓")
        print("L'application est cohérente et en parfait accord!")
        return True
    else:
        print(f"\n⚠ {total_count - synced_count} tickers ne sont pas encore synchronisés")
        return False

if __name__ == "__main__":
    success = test_price_sync()
    sys.exit(0 if success else 1)


