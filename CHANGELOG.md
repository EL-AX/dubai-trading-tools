# Changelog - Dubai Trading Tools

## [5.0] - 2026-02-03 - Supernova Release 🚀

### ✨ **Majors Features Added**

#### Actualités IA en Temps Réel
- Intégration actualités OpenAI, DeepMind, Anthropic, Solana AI Labs, MIT, Moltbook.com
- 6 actualités IA impactant les marchés
- Bilingue FR/EN
- Cache 2h pour performance
- Liens authentiques vers sources

#### Animation Prix Temps Réel
- Affichage fluide comme montre de sport
- Timestamp HH:MM:SS mise à jour
- Change 24h visible (vert/rouge)
- Bouton rafraîchissement manuel
- CoinGecko + ExchangeRate APIs réelles

#### Authentification Améliorée
- Flux: Inscription → Email Vérification → Code Validation → Dashboard
- Code de vérification 6 chiffres
- Expiration 1h
- Resend fonctionnalité
- Streamlit SMTP intégré

#### Données Réelles Synchronisées
- CoinGecko API: BTC, ETH, SOL, ADA, XRP, DOT
- ExchangeRate API: EUR, GBP, JPY, AUD (problème EUR résolu)
- Or (XAU) en temps réel
- Cache cohérent: 5min cryptos, 2h actualités

#### Thème Automatique
- Retrait toggle manuel
- Détection prefers-color-scheme OS
- CSS media queries adaptées

#### Candlesticks Professionnels
- Vert/rouge classiques bien visibles
- Synchronisation avec vraies données
- Volume bars colorées

#### Alertes Gérées Correctement
- RSI Overbought (>70) / Oversold (<30)
- Volatilité 24h (>5%)
- Affichage temps réel dashboard
- Historique + message complet

### 🔧 **Technical Improvements**

- `src/auth.py`: Nouveau flux vérification avec email + code expiry
- `src/data.py`: 2h cache, CoinGecko + fallback, EUR fixé
- `src/alerts.py`: Alertes améliorées avec sévérité + message
- `app.py`: Animation prix, actualités IA, thème système, candlesticks professionnels
- `.env.example`: Configuration SMTP complète
- `requirements.txt`: python-dotenv, pytz ajoutés

### 📚 **Documentation**

- README.md: Mise à jour complète v5.0
- Supernova features highlights

### ✅ **Tests & Validation**

- Syntax check: ✅
- Compilation: ✅
- Git commit: b2de862
- Push GitHub: ✅

---

## [4.1] - Previous Version

Voir commits antérieurs

---

**Version Actuelle:** 5.0 Supernova
**Date:** 3 Février 2026
**Status:** Production Ready 🚀
