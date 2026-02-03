# 🚀 AI Market Hunter - Dubai Edition

**Assistant de trading éducatif professionnel pour crypto/or/forex**

Version: **4.1 (MVT - Minimum Viable Template)**  
Statut: ✅ Complet et conforme au cahier des charges

---

## 📋 Vue d'ensemble

AI Market Hunter est un outil d'analyse technique éducatif conçu pour les traders passionnés des Émirats Arabes Unis. C'est **NON un robot de trading** - c'est un assistant pour prendre de meilleures décisions.

### ✅ Ce que vous pouvez faire :
- 📊 Analyser 5 indicateurs techniques en temps réel
- 🔔 Configurer des alertes personnalisées
- 📈 Backtester des stratégies sur données historiques
- 📚 Apprendre les fondamentaux du trading
- 🎨 Interface moderne et intuitive

### ❌ Ce que vous NE pouvez PAS faire :
- ❌ Exécuter automatiquement des trades
- ❌ Accéder à vos comptes brokers
- ❌ Recevoir de conseil financier direct
- ❌ Garantir des profits

---

## 🎯 Fonctionnalités principales

### 1️⃣ Dashboard - Analyse Technique
- **Graphique Candlestick interactif** (Plotly)
- **Indicateurs superposés** :
  - 📊 **RSI (14)** - Momentum et zones de suracheté/survendu
  - 📈 **EMA 12/26** - Tendances rapides et lentes
  - 📉 **MACD** - Détection des changements de tendance
  - 🔼 **Bollinger Bands** - Volatilité et support/résistance
  - 📊 **Volume Profile** - Zones d'accumulation/distribution
- Support multi-actifs : **BTC-USD, XAU-USD, ETH-USD**
- Signaux combinés automatiques (ACHAT/PRUDENCE/NEUTRE)

### 2️⃣ Système d'alertes
- **Configuration personnalisable** : Seuils RSI, croisements, volume
- **Historique consultable** : Filtrage, horodatage, gestion automatique
- **Multi-actifs** : Surveille vos actifs préférés

### 3️⃣ Backtesting éducatif
- **2 stratégies** : RSI + EMA Crossover
- **Résultats complets** : Taux de réussite, Max Drawdown, Equity curve
- **Support** : 30-365 jours de données

### 4️⃣ Authentification & Profils
- Système de compte sécurisé (hashage SHA-256)
- Sauvegarde des configurations
- Données locales (RGPD/SCA compliant)

### 5️⃣ Guide & Tutoriels
- 📚 Démarrage rapide
- 🧮 Formules mathématiques (LaTeX)
- ❓ FAQ complète

---

## 🛠️ Architecture technique

```
src/
├── indicators.py      # Calculs d'indicateurs natifs
├── data.py            # Génération de données mock
├── auth.py            # Authentification utilisateurs
├── alerts.py          # Moteur d'alertes
└── backtesting.py     # Engine de backtesting

Stack: Streamlit + Plotly + Pandas + NumPy + Pytz
Python: 3.10+
```

---

## 📥 Installation

```bash
# 1. Cloner le projet
git clone <repo>
cd dubai-trading-tools

# 2. Environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# 3. Dépendances
pip install -r requirements.txt

# 4. Lancer
streamlit run app.py
```

Accédez à `http://localhost:8501`

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
