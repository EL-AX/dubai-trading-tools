# 🚀 Dubai Trading Tools - Supernova Edition

**Assistant de trading professionnel avec IA & données cryptos en temps réel**

Version: **5.0 (Supernova - Production Ready)**  
Statut: ✅ **Déploiement complet**

---

## 🌟 Nouvelle Version Supernova - Changements Majeurs

### ✨ **Améliorations v5.0:**

1. **⚙️ Menu Paramètres Complet** ✅
   - **Activer/Désactiver alertes**
   - **Sélectionner devise préférée** (USD, EUR, GBP)
   - **Choisir style des bougies** (classic, boxy, thin)
   - Paramètres sauvegardés dans profil utilisateur
   - **Application immédiate** sans recharge

2. **📰 Actualités IA en Temps Réel** (Cache 2h)
   - OpenAI GPT-5 insights trading
   - DeepMind RL pour options
   - Anthropic Claude 4 fraude detection
   - Solana AI agents
   - MIT market prediction
   - Moltbook.com community news
   - **HTML tags nettoyés** (pas d'artefacts)

3. **💰 Animation Prix Temps Réel** (Comme montre de sport)
   - Mise à jour fluide des cryptos (BTC, ETH, SOL, ADA, XRP, DOT)
   - Change 24h visible (vert ↑/rouge ↓)
   - **Conversion devise** appliquée (€, £, $)
   - Timestamp HH:MM:SS
   - Refresh automatique

4. **🔐 Authentification Améliorée**
   - Inscription → Email de vérification → Code validation
   - Accès au dashboard après vérification
   - Streamlit SMTP configuré natif

5. **📊 Données Réelles Synchronisées**
   - CoinGecko API (Bitcoin, Ethereum, Solana, Cardano, Ripple, Polkadot)
   - ExchangeRate API (EUR, GBP, JPY)
   - Or (XAU) en temps réel
   - **Cache cohérent** avec fallback prices
   - **Données historiques** 60 jours

6. **🎨 Candlesticks Optimisés**
   - **60 jours** d'historique (vs 10 avant)
   - **Épaisseur réduite** (width=2, vs 4)
   - Meilleure lisibilité et précision
   - Tous les actifs synchronisés

---

## 📋 Vue d'ensemble

Dubai Trading Tools est un assistant de trading **PROFESSIONNEL** pour analyser les marchés crypto, forex, et or. 

### ✅ Ce que vous pouvez faire :
- 📊 **Analyser** crypto/forex/or en temps réel
- 🔔 **Alertes RSI** Overbought/Oversold
- 📰 **Lire actualités IA** impactant les marchés
- 💰 **Voir prix** mis à jour chaque 5min
- 📈 **Signaux trading** basés sur 4 indicateurs
- 🎯 **Risk/Reward** calcul automatique

### ❌ Ce que vous NE pouvez PAS faire :
- ❌ Exécuter des trades automatiquement
- ❌ Accéder à vos brokers
- ❌ Garantir des profits

---

## 🎯 Fonctionnalités principales

### 1️⃣ **Dashboard - Analyse Technique**
- **Graphique Candlestick** professionnel (vert/rouge)
- **60 jours d'historique** (données riches)
- **Indicateurs superposés** :
  - 📊 **RSI (14)** - Momentum (Overbought >70 / Oversold <30)
  - 📈 **MACD** - Changements de tendance
  - 🔼 **Bollinger Bands** - Volatilité
  - 💰 **Volume bars** - Pression acheteur/vendeur
- **Support multi-actifs** : BTC, ETH, SOL, ADA, XRP, DOT, EUR, GBP, JPY, AUD, XAU

### 2️⃣ **Prix en Temps Réel** 🔄
- 💰 Mise à jour fluide avec conversion devise (USD/EUR/GBP)
- 📊 Change 24h visible
- ⏱️ Timestamp HH:MM:SS
- 🔘 Bouton rafraîchissement manuel
- 🔄 **Fallback prices** si API rate-limited

### 3️⃣ **Actualités IA** 📰 (Cache 2h)
- 🤖 OpenAI, DeepMind, Anthropic, Moltbook
- 💡 Impact direct sur marchés (BTC +5%, ETH +8%)
- 🔗 Liens sources authentiques
- ✨ **HTML nettoyé** (pas d'artefacts)
- 🌍 Bilingue FR/EN

### 4️⃣ **Paramètres Utilisateur** ⚙️ ✅
- **Activer/désactiver les alertes**
- **Devise préférée** : USD, EUR, GBP
- **Style des bougies** : classic, boxy, thin
- Sauvegardés dans profil utilisateur
- Application immédiate

### 5️⃣ **Alertes Intelligentes** 🚨
- RSI Overbought (>70) / Oversold (<30)
- Volatilité 24h (>5%)
- Affichage temps réel dashboard
- Historique complet

### 6️⃣ **Authentification** 🔐
- Inscription avec email
- Code de vérification (6 chiffres)
- Expiration 1h
- Dashboard accès sécurisé

### 7️⃣ **Signaux Trading** 🎯
- Composite 4 indicateurs
- STRONG_BUY (80-100) → BUY → NEUTRAL → SELL → STRONG_SELL (0-20)
- Risk/Reward ratio calculé

---

## 🛠️ Architecture technique

```
src/
├── auth.py            # Authentification SMTP + vérification
├── data.py            # CoinGecko + ExchangeRate APIs (2-5min cache)
├── alerts.py          # Moteur alertes RSI + volatilité
├── indicators.py      # RSI, MACD, Bollinger Bands
├── cache.py           # Gestion cache TTL
└── trading_rules.py   # Signaux composites

Stack: Streamlit + Plotly + Pandas + NumPy + Requests
Python: 3.10+
Cache: 2-5min pour cryptos, 2h pour actualités
```

---

## 📥 Installation

### Prérequis
- Python 3.10+
- Git
- Compte GitHub

### Étapes

```bash
# 1. Cloner le projet
git clone https://github.com/EL-AX/dubai-trading-tools.git
cd dubai-trading-tools

# 2. Environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# 3. Installer dépendances
pip install -r requirements.txt

# 4. Configurer .env (optionnel - SMTP)
cp .env.example .env
# Éditer .env avec vos credentials SMTP

# 5. Lancer l'app
streamlit run app.py
```

L'app s'ouvre sur `http://localhost:8501`

---

## 🔧 Configuration SMTP (Optionnel)

Pour l'envoi d'emails de vérification:

```bash
# Créer .env dans le root
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=votre-email@gmail.com
SMTP_PASSWORD=votre-app-password
EMAIL_FROM=votre-email@gmail.com
```

Sans .env, les codes sont sauvegardés localement dans `data/outbox/`

---

## 📊 Données & APIs

- **Cryptos**: CoinGecko API (Bitcoin, Ethereum, Solana, Cardano, Ripple, Polkadot)
- **Forex**: exchangerate.host API (EUR, GBP, JPY, AUD)
- **Or**: goldprice.org API (XAU)
- **Actualités**: OpenAI, DeepMind, Anthropic, Moltbook.com, MIT, CoinTelegraph

**Cache & Fallback:**
- Cryptos & Forex: 5 minutes (fallback prices si API rate-limited)
- Actualités IA: 2 heures
- Données historiques: 60 jours de candlesticks
- **Graceful degradation**: Affiche toujours les prix même en cas d'outage API

---

## 🚀 Déploiement

### Streamlit Cloud
```bash
git push origin main
# Va sur https://streamlit.io/ et déploie
```

### Docker
```bash
docker build -t dubai-trading-tools .
docker run -p 8501:8501 dubai-trading-tools
```

### Heroku / Railway
- Push vers Procfile
- Set environment variables SMTP_*

---

## 📚 Documentation

- [DEMARRAGE_RAPIDE.md](DEMARRAGE_RAPIDE.md) - Tutoriel démarrage
- [SPECIFICATIONS_DETAILLEES.md](SPECIFICATIONS_DETAILLEES.md) - Tech specs complètes
- [CONFORMITE_CAHIER_CHARGES.md](CONFORMITE_CAHIER_CHARGES.md) - Checklist fonctionnalités

---

## 🔐 Sécurité

- ✅ Passwords hashés SHA-256
- ✅ Emails vérifiés (SMTP sécurisé)
- ✅ Tokens expiration 1h
- ✅ Données locales (no cloud)
- ✅ HTTPS ready

---

## 📝 Licence

MIT License - Utilisation libre à des fins éducatives

---

## 👤 Auteur

**EL-AX** - GitHub: https://github.com/EL-AX

---

## 🎉 Supernova Features Highlights

✨ **Ce qui rend cette version extraordinaire:**

1. **Actualités IA en Temps Réel** - Des insights OpenAI, DeepMind, Anthropic
2. **Animation Prix** - Mise à jour fluide comme une montre de sport
3. **Authentification Pro** - Email vérification intégrée
4. **Données Réelles** - CoinGecko + ExchangeRate APIs synchronisées
5. **Thème Automatique** - Suit le système d'exploitation
6. **Candlesticks Classiques** - Vert/rouge profesionnels visibles
7. **Alertes Intelligentes** - RSI + volatilité en temps réel

---

**Prêt à trader comme un pro? 🚀** Ouvre l'app et explore!


---

## 🚀 Utilisation

1. **Inscrivez-vous** avec votre email
2. **Connectez-vous**
3. **Dashboard** - Analysez les données en temps réel
4. **Alertes** - Configurez vos seuils
5. **Backtesting** - Testez des stratégies
6. **Guide** - Apprenez les fondamentaux

---

## 🧪 Tests

```bash
python tests/test_indicators.py
```

✅ RSI / MACD / Bollinger testés et validés

---

## 📊 Indicateurs

| Indicateur | Période | Utilité |
|-----------|---------|---------|
| **RSI** | 14 | Momentum / Suracheté/survendu |
| **EMA** | 12/26 | Tendances rapides/lentes |
| **MACD** | 12/26/9 | Changements de tendance |
| **Bollinger** | 20/2σ | Volatilité |
| **Volume Profile** | Dynamique | Zones d'accumulation |

---

## ⚠️ Disclaimer

- **Outil éducatif uniquement** - Pas conseil financier
- **Pas d'exécution d'ordres** - Interface éducative
- **Données simulées** - Ne pas utiliser en temps réel
- **Trading = risque** - Consultez un professionnel

---

## 🔐 Sécurité

✅ Mots de passe hashés (SHA-256)  
✅ Données locales JSON  
✅ RGPD & SCA compliant  
✅ Aucun accès internet obligatoire  

❌ Pas de connexion broker  
❌ Pas d'exécution de trades  

---

## 📞 Support

- 📧 Email: eloadx5@gmail.com
- 🐛 Issues: GitHub Issues

---

**AI Market Hunter** © 2026  
*Dubai Edition - Optimisé pour le marché UAE*
