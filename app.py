"""
╔═══════════════════════════════════════════════════════════════════╗
║                    DUBAI TRADING TOOLS v2.0                       ║
║              © 2025-2026 ELOADXFAMILY - Tous droits réservés       ║
║     Outil d'analyse trading professionnel avec IA et éducation     ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import requests
import time

from src.auth import register_user, login_user, verify_user_email, get_user_settings, save_user_settings, logout, resend_verification_code, init_session_state
from src.alerts import check_alerts, get_alert_history
from src.data import get_live_price, get_historical_data
from src.indicators import calculate_rsi, calculate_macd, calculate_bollinger_bands
from src.trading_rules import SmartSignals, RiskAssessment
from src.tooltips import get_tooltip, format_tooltip_markdown

st.set_page_config(
    page_title="Dubai Trading Tools",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Auto-refresh for live prices - robust approach: click the '🔄' refresh button every 5s
st.markdown("""
<script>
function clickRefresh() {
  try {
    const buttons = Array.from(window.parent.document.querySelectorAll('button'));
    for (const b of buttons) {
      if (b.innerText && b.innerText.trim() === '🔄') { b.click(); break; }
    }
  } catch(e) { /* ignore cross-origin or layout issues */ }
}
setInterval(clickRefresh, 5000);
</script>
""", unsafe_allow_html=True)

def apply_custom_theme():
    """Simple styling - boutons bleu nuit + animations."""
    st.markdown(r"""
    <style>
    @keyframes pulse-green {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    @keyframes pulse-red {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    @keyframes pulse-neutral {
        0% { opacity: 1; }
        50% { opacity: 0.8; }
        100% { opacity: 1; }
    }
    .pulse-green { animation: pulse-green 1.5s ease-in-out infinite; }
    .pulse-red { animation: pulse-red 1.5s ease-in-out infinite; }
    .pulse-neutral { animation: pulse-neutral 1.5s ease-in-out infinite; }
    .stButton > button {
        background-color: #001a4d !important;
        color: white !important;
        border: 2px solid #003d99 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        padding: 10px 20px !important;
    }
    .stButton > button:hover {
        background-color: #003d99 !important;
        border: 2px solid #0055cc !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Simple translator helper (FR/EN)



def show_header():
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        try:
            st.image("logo/IMG-20250824-WA0020.jpg", width=120)
        except:
            st.write("📊")
    with col2:
        st.markdown("<h1 style='text-align: center;'>📈 Dubai Trading Tools</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'>Outil d'analyse et d'aide à la décision pour traders</p>", unsafe_allow_html=True)

def get_ai_news(force_refresh=False):
    """Actualités trading RÉELLES et impactantes basées sur le contenu éducatif"""
    from src.cache import CacheManager
    from src.educational_content import generate_daily_trading_news, IMPACTFUL_NEWS_TEMPLATES
    cache = CacheManager()
    
    user_language = st.session_state.get("user_language", "fr")
    cache_key = f"ai_news_{user_language}"
    
    if not force_refresh:
        try:
            cached_news = cache.get(cache_key)
            if cached_news and isinstance(cached_news, list) and len(cached_news) > 0:
                # Validate cache has correct format
                if all('titre' in item for item in cached_news):
                    return cached_news
        except:
            pass
    
    # Actualités Trading VRAIMENT utiles - basées sur les PDFs éducatifs
    trading_news_data = [
        {
            "titre_fr": "📊 Chandeliers Japonais: Maîtrisez les 19 Patterns Essentiels",
            "titre_en": "📊 Japanese Candlesticks: Master the 19 Essential Patterns",
            "resume_fr": "Doji, Harami, Engulfing: Les patterns qui prédisent les retournements. Apprendre à les identifier pour 80% de fiabilité en plus.",
            "resume_en": "Doji, Harami, Engulfing: Patterns that predict reversals. Learn to identify them for 80% more reliability.",
            "strategie_fr": "Cherchez l'Engulfing haussier après une baisse. Stop loss sous le low. Ratio risque/bénéfice 1:3 minimum.",
            "strategie_en": "Look for bullish Engulfing after a decline. Stop loss below the low. Risk/reward ratio 1:3 minimum.",
            "source": "Dubai Trading Tools - Éducation", "sentiment": "educative", "symbol": "BTC,ETH,SOL"
        },
        {
            "titre_fr": "⚠️ Gestion du Risque: Les 5 Erreurs qui Ruinent les Comptes",
            "titre_en": "⚠️ Risk Management: The 5 Mistakes That Destroy Accounts",
            "resume_fr": "Position trop grande (>2%), pas de stop loss, revenge trading... Évitez ces pièges pour protéger votre capital.",
            "resume_en": "Position too large (>2%), no stop loss, revenge trading... Avoid these traps to protect your capital.",
            "strategie_fr": "Règle 1-2%: Max 1-2% du compte par trade. Stop loss obligatoire AVANT l'entrée. Acceptez les petites pertes.",
            "strategie_en": "1-2% Rule: Max 1-2% per trade. Stop loss BEFORE entry. Accept small losses.",
            "source": "Dubai Trading Tools - Éducation", "sentiment": "warning", "symbol": "ALL"
        },
        {
            "titre_fr": "📈 Stratégies Éprouvées: Support & Résistance + Breakouts",
            "titre_en": "📈 Proven Strategies: Support & Resistance + Breakouts",
            "resume_fr": "Les niveaux qui rebondissent 2-3 fois = zones clés. Attendez cassure + volume pour les meilleurs ratios.",
            "resume_en": "Levels that bounce 2-3 times = key zones. Wait for breakout + volume for best ratios.",
            "strategie_fr": "Tracer support/résistance. Attendre cassure avec volume élevé. Entrée immédiate, stop loss sur l'ancien niveau.",
            "strategie_en": "Draw support/resistance. Wait for breakout with high volume. Immediate entry, stop loss on old level.",
            "source": "Dubai Trading Tools - Éducation", "sentiment": "bullish", "symbol": "BTC,ETH,SOL"
        },
        {
            "titre_fr": "💰 Psychologie du Trading: Discipline > Prédiction",
            "titre_en": "💰 Trading Psychology: Discipline > Prediction",
            "resume_fr": "Peur et Avidité = ennemis du trader. La discipline à suivre les règles = profit long terme garanti.",
            "resume_en": "Fear and Greed = trader's enemies. Discipline to follow rules = guaranteed long-term profit.",
            "strategie_fr": "Créez un plan de trading. Suivez-le 100%. Journal chaque trade. Analysez vos erreurs.",
            "strategie_en": "Create a trading plan. Follow it 100%. Journal every trade. Analyze your mistakes.",
            "source": "Dubai Trading Tools - Éducation", "sentiment": "neutral", "symbol": "ALL"
        },
        {
            "titre_fr": "🎯 Signaux Composites: RSI + MACD + Bollinger = Fiabilité +80%",
            "titre_en": "🎯 Composite Signals: RSI + MACD + Bollinger = 80% Reliability",
            "resume_fr": "Combinez 3 indicateurs = fiabilité multipliée. RSI>70 + MACD positif + prix > Bollinger = STRONG_BUY confirmé.",
            "resume_en": "Combine 3 indicators = reliability multiplied. RSI>70 + MACD positive + price > Bollinger = confirmed STRONG_BUY.",
            "strategie_fr": "Attendez confirmation de tous les 3 avant d'entrer. Diminue les faux signaux de 70%.",
            "strategie_en": "Wait for all 3 confirmation before entering. Reduces false signals by 70%.",
            "source": "Dubai Trading Tools - Éducation", "sentiment": "bullish", "symbol": "BTC,ETH,SOL"
        },
        {
            "titre_fr": "🔄 Divergences: Quand le Prix Monte mais RSI Baisse = Faiblesse",
            "titre_en": "🔄 Divergences: When Price Rises but RSI Falls = Weakness",
            "resume_fr": "Divergence = signal d'inversion majeur. Prix nouveau high mais RSI baisse = retournement baissier proche.",
            "resume_en": "Divergence = major reversal signal. Price new high but RSI falls = bearish reversal coming.",
            "strategie_fr": "Cherchez divergences régulièrement. Meilleures à la 3ème ou 4ème tentative haussière.",
            "strategie_en": "Look for divergences regularly. Best at 3rd or 4th bullish attempt.",
            "source": "Dubai Trading Tools - Éducation", "sentiment": "warning", "symbol": "BTC,ETH,SOL"
        },
        {
            "titre_fr": "💡 Opportunité du Jour: Volatilité Élevée = Meilleurs Ratios R:B",
            "titre_en": "💡 Today's Opportunity: High Volatility = Best R:B Ratios",
            "resume_fr": "Aujourd'hui: Volatilité HAUTE. Augmentez taille position de 25-50% (mais respectez 2% max par trade).",
            "resume_en": "Today: HIGH Volatility. Increase position size 25-50% (but respect 2% max per trade).",
            "strategie_fr": "À volatilité haute: Risquez 2% max. À volatilité basse: Risquez 0.5-1% seulement.",
            "strategie_en": "High volatility: Risk 2% max. Low volatility: Risk 0.5-1% only.",
            "source": "Dubai Trading Tools - Éducation", "sentiment": "bullish", "symbol": "ALL"
        }
    ]
    
    # Format by language
    if user_language == "en":
        news_data = [{
            "titre": news["titre_en"],
            "resume": news["resume_en"],
            "strategie": news["strategie_en"],
            "source": news["source"],
            "sentiment": news["sentiment"],
            "symbol": news["symbol"],
            "date": datetime.now().isoformat()
        } for news in trading_news_data]
    else:  # French
        news_data = [{
            "titre": news["titre_fr"],
            "resume": news["resume_fr"],
            "strategie": news["strategie_fr"],
            "source": news["source"],
            "sentiment": news["sentiment"],
            "symbol": news["symbol"],
            "date": datetime.now().isoformat()
        } for news in trading_news_data]
    
    # Remove exact duplicates by title to prevent repetition
    seen_titles = set()
    unique_news = []
    for item in news_data:
        if item["titre"] not in seen_titles:
            seen_titles.add(item["titre"])
            unique_news.append(item)
    
    # Cache pour 24 heures (actualisé quotidiennement)
    cache.set(cache_key, unique_news, ttl=86400)
    return unique_news

def display_live_price_with_animation(ticker):
    """Display live price with smooth animation updates like a sports watch"""
    price_info = get_live_price(ticker)
    price = price_info.get('price', 0)
    change_24h = price_info.get('change_24h', 0)
    
    # Get currency preference from session
    currency = st.session_state.get("currency", "USD")
    exchange_rate = {
        "USD": 1.0,
        "EUR": 0.92,
        "GBP": 0.82
    }.get(currency, 1.0)
    
    currency_symbol = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£"
    }.get(currency, "$")
    
    # Convert price to selected currency
    converted_price = price * exchange_rate
    
    # Format price with animation effect
    if price > 0:
        price_str = f"{currency_symbol}{converted_price:,.2f}"
        change_str = f"{change_24h:+.2f}%" if change_24h != 0 else "→"
        
        # Color and emoji based on change with animations
        if change_24h > 0:
            color = "🟢"
            emoji = "📈"
            animation = "pulse-green"
        elif change_24h < 0:
            color = "🔴"
            emoji = "📉"
            animation = "pulse-red"
        else:
            color = "⚫"
            emoji = "➡️"
            animation = "pulse-neutral"
        
        return {
            "price": price,
            "price_str": price_str,
            "change_24h": change_24h,
            "change_str": change_str,
            "color": color,
            "emoji": emoji,
            "animation": animation
        }
    else:
        return {
            "price": 0,
            "price_str": "N/A",
            "change_24h": 0,
            "change_str": "N/A",
            "color": "⚫"
        }

def page_tutorial():
    """Tutorial and how-to page"""
    st.title("📚 Comment Utiliser l'Application")
    
    with st.expander("🔐 1. Authentification", expanded=True):
        st.markdown("""
        **Étapes:**
        1. **Inscription**: Créez un compte avec votre email et mot de passe
        2. **Vérification**: Entrez le code de vérification reçu par email (6 chiffres)
        3. **Connexion**: Utilisez vos identifiants pour accéder au tableau de bord
        
        **Conseils de sécurité:**
        - Utilisez un mot de passe fort (minimum 8 caractères)
        - Ne partagez jamais votre code de vérification
        - Déconnectez-vous toujours après chaque session
        """)
    
    with st.expander("📊 2. Tableau de Bord - Votre Centre de Contrôle"):
        st.markdown("""
        **🎯 Sélection des Actifs**
        - Choisissez jusqu'à 8 actifs à analyser simultanément
        - **Crypto**: BTC (Bitcoin), ETH (Ethereum), SOL (Solana), ADA, XRP, DOT
        - **Forex**: EUR, GBP, JPY, AUD (parités de change)
        - **Matières**: XAU (Or / Gold)
        
        **⏱️ Sélection de la Période** (NOUVEAU!)
        - 6 boutons: **1H, 4H, 1D, 1W, 1M, 3M**
        - Cliquez sur une période → le graphe s'actualise automatiquement
        - Adapte la plage de données historiques
        - Réajuste tous les indicateurs pour la période
        
        **💹 Prix en Temps Réel**
        - Prix instantané avec changement 24h
        - Devise convertie selon vos préférences (USD, EUR, GBP)
        - Mise à jour automatique toutes les 5 minutes
        - Indicateurs visuels: 🟢 (hausse), 🔴 (baisse)
        
        **📈 Graphiques Professionnels (XM Style)**
        - Bougies candlestick conformes aux standards professionnels
        - Couleurs: Vert #1bc47d (hausse), Rouge #ff3d3d (baisse)
        - Sélectionnez votre période pour adapter le graphe
        - Volume synchronisé en bas
        - Responsive et optimisé pour mobile
        
        **🚨 Signaux & Alertes**
        - Signaux composites automatiques (STRONG_BUY à STRONG_SELL)
        - Alertes pour RSI, volatilité, changements 24h
        """)
    
    with st.expander("📈 3. Indicateurs Techniques - Comprendre les Signaux"):
        st.markdown("""
        **RSI (Relative Strength Index)**
        - Mesure le momentum de 0 à 100
        - **>70**: Suracheté (vendre potentiellement)
        - **<30**: Survendu (acheter potentiellement)
        - Période: 14 bougies
        
        **MACD (Moving Average Convergence Divergence)**
        - Détecte les changements de tendance
        - **Croisement haussier**: Signal d'achat
        - **Croisement baissier**: Signal de vente
        - Utilise les moyennes mobiles 12 et 26 jours
        
        **Bandes de Bollinger**
        - Montre la volatilité et les niveaux de support/résistance
        - **Prix aux limites**: Potentiel retour à la moyenne
        - Bande supérieure/inférieure = écart-type ±2
        - Utile pour identifier les extrêmes
        
        **Signaux Composites**
        - Combine **4 indicateurs** pour une fiabilité accrue
        - **STRONG_BUY (80-100)**: Signal très bullish
        - **BUY (60-80)**: Signal bullish modéré
        - **NEUTRAL (40-60)**: Pas de direction claire
        - **SELL (20-40)**: Signal bearish modéré
        - **STRONG_SELL (0-20)**: Signal très bearish
        """)
    
    with st.expander("🎯 4. Stratégies de Trading"):
        st.markdown("""
        **Stratégie Simple (Débutants)**
        - Sélectionnez la période 1D pour tendances court-moyen terme
        - Attendez STRONG_BUY (>80) pour acheter
        - Attendez STRONG_SELL (<20) pour vendre
        - Combinez avec les bandes de Bollinger pour confirmation
        
        **Stratégie Avancée (Professionnels)**
        - Utilisez RSI + MACD + Bollinger ensemble
        - Testez différentes périodes (1H pour scalping, 1W pour swing)
        - Cherchez les divergences (prix monte, RSI baisse = signal faible)
        - Identifiez les zones de support/résistance
        - Gérez votre risque avec stop-loss et take-profit
        
        **Gestion du Risque**
        - Risquez jamais >2% du portefeuille par trade
        - Définissez un ratio risque/récompense minimum 1:2
        - Utilisez les alertes pour détecter les mouvements
        - Diversifiez sur plusieurs actifs
        """)
    
    with st.expander("📰 5. Actualités IA - Analyse du Marché"):
        st.markdown("""
        **📊 Sentiment du Marché**
        - Jauge visuelle montrant si marché est haussier ou baissier
        - Pourcentage de news bullish/bearish/neutres
        - Badge global: "TRÈS HAUSSIER" → "NEUTRE" → "TRÈS BAISSIER"
        
        **🔍 Filtres Avancés**
        - Filtrez par **sentiment** (Haussier, Baissier, Neutre)
        - Filtrez par **source** (Reddit, CoinDesk, CoinTelegraph, CoinGecko)
        - Combinez les filtres pour analyses précises
        
        **💹 Sources de News**
        - **Reddit**: Discussions communauté crypto
        - **CoinDesk**: News institutionnelles
        - **CoinTelegraph**: Analyses détaillées
        - **CoinGecko**: Trending et signaux
        
        **💡 Comment utiliser:**
        1. Vérifiez le sentiment global (jauge)
        2. Filtrez pour "Haussier" = opportunités achat
        3. Filtrez pour "Baissier" = prudence/vente
        4. Cliquez les articles intéressants
        5. Combinez avec votre analyse technique
        
        **⚠️ Important**: Les actualités et sentiment ne remplacent PAS votre stratégie!
        """)
    
    with st.expander("🕯️ 6. Patterns & Trading - Maîtrisez les Chandeliers"):
        st.markdown("""
        **📚 19 Chandeliers Japonais Essentiels**
        - Base du trading technique
        - Chaque pattern a un signal (haussier/baissier)
        - Fiabilité notée: ⭐⭐⭐ Haute, ⭐⭐ Moyenne, ⭐ Basse
        
        **📔 Journal de Patterns - Tracker Votre Apprentissage**
        - Ajouter des patterns observés dans le marché
        - Statuts: observé → confirmé → tradé → validé
        - Exportez en CSV pour analyse
        
        **🎯 Quiz Interactif - Testez Vos Connaissances**
        - 5 questions sur les chandeliers
        - Explications complètes pour chaque réponse
        - Score avec conseil basé sur performance
        - Objectif: 100% pour maîtrise complète
        
        **📊 Statistiques d'Apprentissage**
        - Pie chart de vos patterns tracés
        - Barre de progression par sujet
        - Recommandations personnalisées
        - Gestion du risque intégrée
        
        **💰 Calculateur de Position Sizing**
        - Entrez solde du compte, risque %, prix d'entrée/stop
        - Calcule la taille exacte de position
        - Valide si conforme aux règles (max 2% risque)
        
        **⚙️ 5 Stratégies de Trading**
        1. **Simple**: STRONG_BUY/SELL sur RSI
        2. **Avancée**: RSI + MACD + Bollinger
        3. **Gestion Risque**: Position sizing + stop loss
        4. **Psychologie**: 7 règles mentales du pro
        5. **Checklist**: 10 points avant chaque trade
        
        **📝 Comment Progresser**
        1. Étudiez les 19 patterns (onglet Patterns)
        2. Pratiquez le quiz jusqu'à 100%
        3. Trackez les patterns observés
        4. Validez vos observations
        5. Maîtrisez d'abord 2-3 patterns avant d'en apprendre d'autres
        """)
    
    with st.expander("❓ 7. FAQ & Dépannage"):
        st.markdown("""
        **Q: Comment fonctionne le sélecteur de période?**
        A: Cliquez sur 1H, 4H, 1D, 1W, 1M ou 3M → le graphe s'actualise automatiquement avec les données de cette période.
        
        **Q: Comment interpréter le sentiment de news?**
        A: Vert (bullish) = marché positif, Rouge (bearish) = marché négatif, Gris (neutre) = pas de direction. Utilisez comme confirmation avec vos signaux techniques.
        
        **Q: Puis-je exporter mon journal de patterns?**
        A: Oui! Onglet Journal → bouton "Exporter en CSV" → télécharge automatiquement.
        
        **Q: Comment gagner au quiz?**
        A: Étudiez les descriptions de patterns dans l'onglet "Patterns". Répondez aux 5 questions. Visez 100% pour maîtrise complète.
        
        **Q: Pourquoi les prix ne se mettent pas à jour?**
        A: L'app s'actualise toutes les 5 minutes. Attendez ou rechargez la page avec F5.
        
        **Q: Puis-je trader en direct?**
        A: Cette app est un **outil d'analyse**, pas une plateforme de trading. Utilisez Binance, Kraken, XM, etc. pour les vraies positions.
        
        **Q: Mes données sont-elles sécurisées?**
        A: Oui. Mot de passe hashé, emails vérifiés, données encryptées.
        """)
    
    st.divider()
    st.info("💡 **Conseil Pro**: Testez vos stratégies avec les graphiques en papier avant d'investir de l'argent réel. Les performances passées n'indiquent pas les performances futures.")
    
    st.markdown("""
    ---
    ## 📌 Résumé des 4 Sections Principales
    
    | Section | Fonction | Objectif |
    |---------|----------|----------|
    | 📊 **Dashboard** | Graphiques + Indicateurs | Analyser les prix en temps réel |
    | 📰 **Actualités** | Sentiment marché + filtres | Comprendre la psychologie du marché |
    | 🕯️ **Patterns** | 19 chandeliers + Quiz | Apprendre le trading technique |
    | 📚 **Tutoriel** | Documentation complète | Maîtriser tous les outils |
    
    **Bon trading! 🚀**
    """)

def page_login_register():
    """Redesigned login/register flow with email verification integrated"""
    st.markdown("## Connexion / Inscription")
    
    # Check if user just registered (for showing verification code entry on login)
    show_verification_code = st.session_state.get("show_verification_code", False)
    
    tab1, tab2 = st.tabs(["Connexion", "Inscription"])
    
    with tab1:
        st.subheader("Se connecter à votre compte")
        email_input = st.text_input("Email", placeholder="exemple@email.com", key="login_email")
        # Normalize email locally for lookups but keep the raw input in the field
        email = email_input.strip().lower() if email_input else ""
        password = st.text_input("Mot de passe", type="password", placeholder="••••••••", key="login_password")
        
        # Load user to check if verification is required
        from src.auth import load_users
        users = load_users()
        user = users.get(email, {}) if email else {}
        needs_verification = not user.get("verified", False)
        
        if needs_verification and email in users:
            st.info("⚠️ Votre email n'a pas encore été vérifié. Veuillez entrer le code reçu par email.")
            verification_code = st.text_input("Code de vérification (6 chiffres)", placeholder="000000", key="login_ver_code", max_chars=6)
        else:
            verification_code = None
        
        if st.button("Se connecter", key="btn_login", use_container_width=True):
            if email and password:
                if needs_verification and email in users:
                    if not verification_code:
                        st.warning("Veuillez entrer le code de vérification")
                    else:
                        result = login_user(email, password, verification_code)
                        if result["success"]:
                            st.session_state.authenticated = True
                            st.session_state.user_email = email
                            st.session_state.user_name = result["name"]
                            # Show welcome on next run so it survives rerun
                            st.session_state.show_welcome = True
                            st.session_state.just_logged_in_user = result["name"]
                            st.rerun()
                        else:
                            st.error(result["message"])
                else:
                    result = login_user(email, password)
                    if result["success"]:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.session_state.user_name = result["name"]
                        # Show welcome on next run so it survives rerun
                        st.session_state.show_welcome = True
                        st.session_state.just_logged_in_user = result["name"]
                        st.rerun()
                    else:
                        st.error(result["message"])
            else:
                st.warning("Remplissez tous les champs")
        
        # Resend verification code if needed
        if needs_verification and email in users:
            if st.button("📧 Renvoyer le code de vérification", key="btn_resend_login", use_container_width=True):
                resend = resend_verification_code(email)
                if resend.get("success"):
                    st.success("✅ Code renvoyé! Vérifiez votre boîte mail.")
                else:
                    st.error(f"Erreur: {resend.get('message')}")
    
    with tab2:
        st.subheader("Créer un nouveau compte")
        st.markdown("Remplissez les champs ci-dessous pour créer un compte.")
        
        reg_name = st.text_input("Nom complet", placeholder="Jean Dupont", key="reg_name")
        reg_email = st.text_input("Email", placeholder="votre@email.com", key="reg_email")
        reg_password = st.text_input("Mot de passe (min 8 caractères)", type="password", placeholder="••••••••••••", key="reg_password")
        
        if st.button("S'inscrire", key="btn_register", use_container_width=True):
            if reg_name and reg_email and reg_password:
                if len(reg_password) < 8:
                    st.error("❌ Le mot de passe doit faire au moins 8 caractères")
                elif "@" not in reg_email:
                    st.error("❌ Veuillez entrer une adresse email valide")
                else:
                    result = register_user(reg_email, reg_password, reg_name)
                    if result["success"]:
                        st.success("✅ Compte créé avec succès!")
                        st.info(result["message"])
                        
                        # Show next steps
                        st.markdown("""
                        ### Prochaines étapes:
                        1. **Vérifiez votre boîte mail** pour recevoir le code de vérification
                        2. **Retournez à l'onglet Connexion** et entrez votre email
                        3. **Entrez le code** reçu par email (6 chiffres)
                        4. **Connectez-vous** avec votre mot de passe
                        
                        *Si vous ne recevez pas d'email, vérifiez le dossier spam ou cliquez sur "Renvoyer le code"*
                        """)
                        st.balloons()
                    else:
                        st.error(f"❌ Erreur: {result['message']}")
            else:
                st.warning("⚠️ Remplissez tous les champs")

def page_news_ai():
    """Section actualités IA PREMIUM - Intelligence artificielle du marché en temps réel"""
    st.title("📰 Actualités Marché - IA Intelligence Platform")
    
    # Refresh button with status
    col_refresh, col_info = st.columns([1, 4])
    with col_refresh:
        if st.button("🔄 Actualiser", use_container_width=True):
            from src.cache import CacheManager
            cache = CacheManager()
            cache.delete("real_news_all")
            st.rerun()
    with col_info:
        st.info("🤖 IA SENTIMENT ANALYSIS | ✅ Cache 10min | 4 SOURCES RÉELLES | 📊 ANALYSE TEMPS RÉEL | 🚀 POWERED BY ML")
    
    # Get REAL news from real sources
    from src.real_news import get_all_real_news
    news_items = get_all_real_news()
    
    if news_items:
        sentiments = [n.get('sentiment', 'neutral') for n in news_items]
        bullish_count = sentiments.count('bullish')
        bearish_count = sentiments.count('bearish')
        neutral_count = sentiments.count('neutral')
        total_count = len(news_items)
        
        # === TAB 1: MARKET INTELLIGENCE DASHBOARD ===
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🔥 Trending", "📈 Analytics", "📚 All News"])
        
        with tab1:
            st.subheader("🎯 Intelligence Dashboard - Vue Globale du Marché")
            
            # Professional metrics with impact scores
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                bullish_pct = round(bullish_count/total_count*100)
                st.metric("🟢 BULLISH", bullish_count, f"+{bullish_pct}%", delta_color="normal")
                
            with col2:
                bearish_pct = round(bearish_count/total_count*100)
                st.metric("🔴 BEARISH", bearish_count, f"-{bearish_pct}%", delta_color="inverse")
                
            with col3:
                neutral_pct = round(neutral_count/total_count*100)
                st.metric("⚪ NEUTRE", neutral_count, f"{neutral_pct}%")
                
            with col4:
                st.metric("📰 TOTAL", total_count, "articles")
                
            with col5:
                momentum = ((bullish_count - bearish_count) / total_count * 100)
                st.metric("📈 MOMENTUM", f"{momentum:+.1f}%", "Market Force")
            
            st.divider()
            
            # === SENTIMENT GAUGE & MARKET STATE ===
            st.markdown("### 🎬 État du Marché - IA Analysis")
            
            sentiment_balance = ((bullish_count - bearish_count) / total_count * 100) if total_count > 0 else 0
            
            # 3-column layout for gauge
            col_gauge1, col_gauge2, col_gauge3 = st.columns([1, 2, 2])
            
            with col_gauge1:
                st.markdown("**Sentiment Score:**")
                
            with col_gauge2:
                if sentiment_balance > 50:
                    badge = "🚀 EXTRÊMEMENT HAUSSIER"
                    color = "green"
                elif sentiment_balance > 30:
                    badge = "🟢 TRÈS HAUSSIER"
                    color = "green"
                elif sentiment_balance > 10:
                    badge = "📈 HAUSSIER"
                    color = "lightgreen"
                elif sentiment_balance > -10:
                    badge = "⚪ NEUTRE"
                    color = "gray"
                elif sentiment_balance > -30:
                    badge = "📉 BAISSIER"
                    color = "lightcoral"
                elif sentiment_balance > -50:
                    badge = "🔴 TRÈS BAISSIER"
                    color = "red"
                else:
                    badge = "💥 EXTRÊMEMENT BAISSIER"
                    color = "darkred"
                
                st.markdown(f"<h3 style='color:{color}'>{badge}</h3>", unsafe_allow_html=True)
                
            with col_gauge3:
                gauge_value = (sentiment_balance + 100) / 200
                st.progress(min(max(gauge_value, 0), 1), text=f"Force Sentiment: {abs(sentiment_balance):.1f}%")
            
            st.divider()
            
            # === SOURCE ANALYSIS ===
            st.markdown("### 📊 Analyse par Source")
            source_stats = {}
            for n in news_items:
                src = n.get('source', 'Unknown')
                if src not in source_stats:
                    source_stats[src] = {'bullish': 0, 'bearish': 0, 'neutral': 0, 'total': 0}
                source_stats[src][n.get('sentiment', 'neutral')] += 1
                source_stats[src]['total'] += 1
            
            source_cols = st.columns(len(source_stats))
            for col_idx, (source, stats) in enumerate(source_stats.items()):
                with source_cols[col_idx]:
                    source_sentiment = ((stats['bullish'] - stats['bearish']) / stats['total'] * 100) if stats['total'] > 0 else 0
                    st.metric(
                        source,
                        f"{stats['total']} news",
                        f"{source_sentiment:+.0f}%",
                        delta_color="normal" if source_sentiment > 0 else "inverse"
                    )
            
            st.divider()
            
            # === TOP ASSETS ===
            st.markdown("### 💰 Actifs les Plus Mentionnés")
            asset_count = {}
            asset_sentiment = {}
            for n in news_items:
                sym = n.get('symbol', '')
                if sym:
                    if sym not in asset_count:
                        asset_count[sym] = 0
                        asset_sentiment[sym] = []
                    asset_count[sym] += 1
                    asset_sentiment[sym].append(n.get('sentiment', 'neutral'))
            
            if asset_count:
                top_assets = sorted(asset_count.items(), key=lambda x: x[1], reverse=True)[:5]
                asset_cols = st.columns(min(5, len(top_assets)))
                for col_idx, (asset, count) in enumerate(top_assets):
                    with asset_cols[col_idx]:
                        sentiments_for_asset = asset_sentiment[asset]
                        bullish_asset = sentiments_for_asset.count('bullish')
                        bearish_asset = sentiments_for_asset.count('bearish')
                        asset_momentum = ((bullish_asset - bearish_asset) / len(sentiments_for_asset) * 100)
                        
                        st.metric(
                            f"💎 {asset}",
                            f"{count} mentions",
                            f"{asset_momentum:+.0f}%",
                            delta_color="normal" if asset_momentum > 0 else "inverse"
                        )
        
        with tab2:
            st.subheader("🔥 Trending - Actualités CRITIQUES")
            
            # Get highest impact news
            st.markdown("### ⭐ HOT TOPICS - Sujets les Plus Chauds")
            
            # Separate by sentiment
            bullish_news = [n for n in news_items if n.get('sentiment') == 'bullish']
            bearish_news = [n for n in news_items if n.get('sentiment') == 'bearish']
            
            col_bull, col_bear = st.columns(2)
            
            with col_bull:
                st.markdown("#### 🟢 TOP BULLISH")
                if bullish_news:
                    for i, news in enumerate(bullish_news[:3], 1):
                        with st.container(border=True):
                            st.markdown(f"**#{i}. {news.get('titre', 'N/A')}**")
                            st.caption(f"{news.get('source', 'Unknown')} • `{news.get('symbol', 'N/A')}`")
                            st.markdown(f"_{news.get('resume', 'N/A')}_")
                            st.markdown(f"🎯 Impact: **POSITIF**")
                else:
                    st.info("Aucune news bullish pour le moment")
                    
            with col_bear:
                st.markdown("#### 🔴 TOP BEARISH")
                if bearish_news:
                    for i, news in enumerate(bearish_news[:3], 1):
                        with st.container(border=True):
                            st.markdown(f"**#{i}. {news.get('titre', 'N/A')}**")
                            st.caption(f"{news.get('source', 'Unknown')} • `{news.get('symbol', 'N/A')}`")
                            st.markdown(f"_{news.get('resume', 'N/A')}_")
                            st.markdown(f"⚠️ Impact: **NÉGATIF**")
                else:
                    st.info("Aucune news bearish pour le moment")
        
        with tab3:
            st.subheader("📈 Advanced Analytics")
            
            col_anal1, col_anal2 = st.columns(2)
            
            with col_anal1:
                st.markdown("#### 📊 Distribution Sentiment")
                # Create pie chart data
                chart_data = {
                    'Sentiment': ['Bullish', 'Bearish', 'Neutre'],
                    'Count': [bullish_count, bearish_count, neutral_count]
                }
                chart_df = pd.DataFrame(chart_data)
                
                fig_pie = px.pie(
                    chart_df,
                    values='Count',
                    names='Sentiment',
                    color_discrete_map={'Bullish': '#1bc47d', 'Bearish': '#ff3d3d', 'Neutre': '#888888'},
                    title='Répartition du Sentiment'
                )
                fig_pie.update_layout(height=400, showlegend=True)
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col_anal2:
                st.markdown("#### 📰 Distribution par Source")
                source_chart_data = {
                    'Source': list(source_stats.keys()),
                    'Articles': [stats['total'] for stats in source_stats.values()]
                }
                source_chart_df = pd.DataFrame(source_chart_data)
                
                fig_bar = px.bar(
                    source_chart_df,
                    x='Source',
                    y='Articles',
                    color='Articles',
                    color_continuous_scale='Viridis',
                    title='Articles par Source'
                )
                fig_bar.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig_bar, use_container_width=True)
        
        with tab4:
            st.subheader("📚 Toutes les Actualités - Recherche Complète")
            
            # Advanced Filters
            st.markdown("### 🔍 Filtres Avancés")
            filter_cols = st.columns(3)
            
            with filter_cols[0]:
                sentiment_filter = st.multiselect(
                    "📊 Sentiment",
                    ["🟢 Haussier", "🔴 Baissier", "⚪ Neutre"],
                    default=["🟢 Haussier", "🔴 Baissier", "⚪ Neutre"],
                    key="all_sentiment_filter"
                )
            
            with filter_cols[1]:
                sources = sorted(list(set([n.get('source', 'Unknown') for n in news_items])))
                source_filter = st.multiselect(
                    "🌐 Source",
                    sources,
                    default=sources,
                    key="all_source_filter"
                )
            
            with filter_cols[2]:
                all_symbols = set()
                for n in news_items:
                    sym = n.get('symbol', '')
                    if sym:
                        all_symbols.add(sym)
                symbols = sorted(list(all_symbols))
                if symbols:
                    symbol_filter = st.multiselect(
                        "💰 Actif",
                        symbols,
                        default=symbols[:3] if len(symbols) > 3 else symbols,
                        key="all_symbol_filter"
                    )
                else:
                    symbol_filter = []
            
            # Apply filters
            sentiment_map = {"🟢 Haussier": "bullish", "🔴 Baissier": "bearish", "⚪ Neutre": "neutral"}
            selected_sentiments = [sentiment_map.get(s, s) for s in sentiment_filter]
            
            filtered_news = [
                n for n in news_items 
                if n.get('sentiment', 'neutral') in selected_sentiments 
                and n.get('source', 'Unknown') in source_filter
                and (not symbol_filter or n.get('symbol', '') in symbol_filter)
            ]
            
            st.divider()
            st.markdown(f"### 📰 Résultats ({len(filtered_news)}/{total_count})")
            
            # Display all filtered news with better cards
            if filtered_news:
                for idx, news in enumerate(filtered_news, 1):
                    with st.container(border=True):
                        col_info, col_action = st.columns([4, 1])
                        
                        with col_info:
                            # Title with sentiment
                            sentiment_emoji = "🟢" if news.get('sentiment') == 'bullish' else "🔴" if news.get('sentiment') == 'bearish' else "⚪"
                            st.markdown(f"### {sentiment_emoji} {news.get('titre', 'N/A')}")
                            
                            # Content
                            st.markdown(f"{news.get('resume', 'N/A')}")
                            
                            # Metadata
                            col_meta1, col_meta2, col_meta3 = st.columns(3)
                            with col_meta1:
                                st.caption(f"📌 **Source:** {news.get('source', 'Unknown')}")
                            with col_meta2:
                                if news.get('symbol'):
                                    st.caption(f"💰 **Actif:** `{news.get('symbol')}`")
                                else:
                                    st.caption("💰 **Actif:** Global")
                            with col_meta3:
                                sentiment_text = "HAUSSIER 📈" if news.get('sentiment') == 'bullish' else "BAISSIER 📉" if news.get('sentiment') == 'bearish' else "NEUTRE ➡️"
                                st.caption(f"📊 **Sentiment:** {sentiment_text}")
                        
                        with col_action:
                            url = news.get('url', '')
                            if url:
                                st.markdown(f"[🔗 **Lire**]({url})")
            else:
                st.info("❌ Aucune actualité correspondant aux filtres")
    else:
        st.warning("❌ Aucune news disponible pour le moment. Les APIs peuvent être momentanément indisponibles.")

def page_dashboard():
    st.title("📊 TRADING COMMAND CENTER - Tableau de Bord Premium")
    
    # Header with logout and info
    col_header1, col_header2, col_header3 = st.columns([2, 2, 1])
    with col_header1:
        st.markdown(f"🔑 **User:** `{st.session_state.user_name}`")
    with col_header2:
        st.info("⚡ PLATFORM LIVE | ✅ Données temps réel | 🎯 11 Actifs | 📊 6 Périodes")
    with col_header3:
        if st.button("🚪 Déconnecter", key="btn_logout", use_container_width=True):
            logout(st)
            st.rerun()

    # Show one-time welcome message after successful login - ANIMATED
    if st.session_state.get("show_welcome"):
        name = st.session_state.get("just_logged_in_user", st.session_state.get("user_name", "Trader"))
        name = name if name else "Trader"  # Fallback if None
        # Animated welcome with confetti effect
        st.markdown(f"""
        <style>
        @keyframes slideInDown {{
            from {{ transform: translateY(-100px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
        .welcome-box {{
            animation: slideInDown 0.8s ease-out;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 12px;
            text-align: center;
            color: white;
            font-size: 24px;
            font-weight: bold;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            margin-bottom: 20px;
        }}
        </style>
        <div class="welcome-box">
        ✨ Bienvenue <b>{name}</b>! 🎉 ✨<br>
        <small style="font-size: 14px; margin-top: 10px;">Prêt à trader comme un pro? 🚀</small>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
        st.session_state.show_welcome = False
        st.session_state.just_logged_in_user = None
    
    st.divider()
    
    # Dashboard Metrics Row
    col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
    with col_m1:
        st.metric("🎯 Actifs", "11", "Crypto/Forex/Gold")
    with col_m2:
        st.metric("📊 Indicateurs", "3", "RSI • MACD • Bollinger")
    with col_m3:
        st.metric("⏱️ Périodes", "6", "1H → 3M")
    with col_m4:
        st.metric("📰 News", "Temps Réel", "4 Sources")
    with col_m5:
        st.metric("🤖 Patterns", "19", "Analysis Engine")
    st.divider()
    
    # === TAB LAYOUT FOR DASHBOARD ===
    tab_assets, tab_prices, tab_indicators, tab_analysis = st.tabs(["💰 Actifs", "📊 Prix Live", "📈 Indicateurs", "🎯 Analyse"])
    
    with tab_assets:
        st.markdown("### 💰 Sélection des Actifs - Choisissez vos Pairs")
        st.markdown("Sélectionnez les cryptomonnaies, devises forex, ou matières premières à analyser en temps réel.")
        
        # ALL supported tickers
        tickers = ["BTC", "ETH", "SOL", "ADA", "XRP", "DOT", "EUR", "GBP", "JPY", "AUD", "XAU"]
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("✅ Sélectionner Tous", use_container_width=True):
                st.session_state.selected_tickers = tickers
                st.rerun()
        with col_btn2:
            if st.button("❌ Désélectionner Tous", use_container_width=True):
                st.session_state.selected_tickers = ["BTC", "EUR"]
                st.rerun()
        
        selected_tickers = st.multiselect(
            "🎯 **Choisir les Actifs:**",
            tickers,
            default=st.session_state.get("selected_tickers", ["BTC", "EUR"]),
            key="assets_selector"
        )
        st.session_state.selected_tickers = selected_tickers
        
        # Asset categories
        st.divider()
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            crypto_count = sum(1 for t in selected_tickers if t in ["BTC", "ETH", "SOL", "ADA", "XRP", "DOT"])
            st.metric("🪙 Cryptos", crypto_count, "sélectionnées")
        with col_c2:
            forex_count = sum(1 for t in selected_tickers if t in ["EUR", "GBP", "JPY", "AUD"])
            st.metric("💱 Forex", forex_count, "sélectionnées")
        with col_c3:
            commodities = sum(1 for t in selected_tickers if t in ["XAU"])
            st.metric("🏆 Matières 1ères", commodities, "sélectionnées")
    
    with tab_prices:
        st.markdown("### 📊 Prix en Temps Réel - Market Snapshot")
        
        if st.session_state.get("selected_tickers", []):
            selected_tickers = st.session_state.selected_tickers
            
            # Display last update time
            from datetime import datetime as dt
            now = dt.now().strftime("%H:%M:%S")
            col_info, col_btn = st.columns([5, 1])
            with col_info:
                st.caption(f"🔴 EN DIRECT | Mise à jour: {now} | {len(selected_tickers)} pairs monitorés | Auto-refresh 5s")
            with col_btn:
                if st.button("🔄 Refresh", key="refresh_prices", use_container_width=True):
                    st.session_state.price_refresh_counter = (st.session_state.get("price_refresh_counter", 0) + 1)
                    st.rerun()
            
            st.divider()
            
            price_cols = st.columns(min(3, len(selected_tickers)))
            prices_data = {}
            
            for idx, ticker in enumerate(selected_tickers):
                with price_cols[idx % 3]:
                    # Display price with animation and change info
                    price_display = display_live_price_with_animation(ticker)
                    prices_data[ticker] = price_display
                    
                    # Display as metric with delta (like a sports watch)
                    st.metric(
                        label=f"{price_display['color']} {ticker}",
                        value=price_display['price_str'],
                        delta=price_display['change_str'],
                        delta_color="normal"
                    )
        else:
            st.warning("👈 Sélectionnez des actifs dans l'onglet 'Actifs'")
    
    with tab_indicators:
        st.markdown("### 📈 Sélection des Indicateurs")
        st.markdown("Choisissez les indicateurs techniques à afficher sur les graphes.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            show_rsi = st.checkbox("📊 RSI (14)", value=st.session_state.get("show_rsi", True), key="rsi_check")
            st.session_state.show_rsi = show_rsi
        with col2:
            show_macd = st.checkbox("📉 MACD", value=st.session_state.get("show_macd", False), key="macd_check")
            st.session_state.show_macd = show_macd
        with col3:
            show_bollinger = st.checkbox("📈 Bollinger Bands", value=st.session_state.get("show_bollinger", False), key="bb_check")
            st.session_state.show_bollinger = show_bollinger
        
        st.divider()
        
        # Indicator explanations
        if show_rsi:
            with st.expander("ℹ️ RSI (Relative Strength Index)"):
                st.markdown("""
                **RSI** mesure la force relative d'un actif:
                - **> 70:** Suracheté 🔴 (vente potentielle)
                - **< 30:** Survendu 🟢 (achat potentiel)
                - **30-70:** Zone neutre ⚪
                """)
        
        if show_macd:
            with st.expander("ℹ️ MACD (Moving Average Convergence Divergence)"):
                st.markdown("""
                **MACD** identifie les changements de momentum:
                - **Ligne MACD > Signal:** Momentum haussier 🟢
                - **Ligne MACD < Signal:** Momentum baissier 🔴
                - **Histogramme:** Force du signal
                """)
        
        if show_bollinger:
            with st.expander("ℹ️ Bandes de Bollinger"):
                st.markdown("""
                **Bollinger Bands** détectent volatilité et niveaux extrêmes:
                - **Bande Supérieure:** Résistance 🔴
                - **Bande Inférieure:** Support 🟢
                - **Écartement:** Volatilité accrue 📈
                """)
    
    with tab_analysis:
        st.markdown("### 🎯 Analyse Graphique & Patterns")
        
        selected_period = st.session_state.get("selected_period", "1D")
        
        st.markdown("#### ⏱️ Sélectionnez la Période Temporelle")
        st.markdown("*Choisissez la timeframe pour votre analyse technique*")
        
        period_cols = st.columns(6)
        
        periods = ["1H", "4H", "1D", "1W", "1M", "3M"]
        period_labels = ["⏱️ 1H", "⏱️ 4H", "📅 1D", "📆 1W", "📊 1M", "📈 3M"]
        
        for idx, (period, label) in enumerate(zip(periods, period_labels)):
            with period_cols[idx]:
                if st.button(label, use_container_width=True, key=f"period_{period}"):
                    st.session_state.selected_period = period
                    st.rerun()
        
        selected_period = st.session_state.get("selected_period", "1D")
    
    # === CHARTS DISPLAY ===
    if st.session_state.get("selected_tickers", []):
        selected_tickers = st.session_state.selected_tickers
        
        st.divider()
        st.subheader("📊 Graphiques en Temps Réel")
        
        # For short periods, fetch more data to calculate indicators properly
        days_to_fetch = {
            "1H": 7,      # 7 days for 1H period (better indicators)
            "4H": 7,      # 7 days for 4H period
            "1D": 30,     # 30 days for daily
            "1W": 90,     # 90 days for weekly
            "1M": 180,    # 180 days for monthly
            "3M": 365     # 365 days for quarterly
        }.get(selected_period, 30)
        
        for ticker in selected_tickers:
            # Display with period badge
            period_badge = {"1H": "⏱️ 1 Heure", "4H": "⏱️ 4 Heures", "1D": "📅 1 Jour", "1W": "📆 1 Semaine", "1M": "📊 1 Mois", "3M": "📈 3 Mois"}
            badge = period_badge.get(selected_period, "1 Jour")
            col_title, col_badge = st.columns([3, 1])
            with col_title:
                st.subheader(f"📈 {ticker}")
            with col_badge:
                st.info(badge)
            
            hist_data = get_historical_data(ticker, days=days_to_fetch)
            
            # Sécuriser les données pour le candlestick
            if hist_data.empty:
                st.warning(f"Pas de données disponibles pour {ticker}")
                continue
                
            # Reset index if timestamp is index instead of column
            if hist_data.index.name == 'timestamp' and 'timestamp' not in hist_data.columns:
                hist_data = hist_data.reset_index()
            
            # Ensure timestamp is datetime
            if 'timestamp' not in hist_data.columns:
                hist_data['timestamp'] = pd.date_range(end=datetime.now(), periods=len(hist_data), freq='D')
            else:
                hist_data['timestamp'] = pd.to_datetime(hist_data['timestamp'], errors='coerce')
            
            # IMPORTANT: Limit display data based on period
            # Keep all data for indicator calculations, but display only relevant range
            display_data = hist_data.copy()
            
            # Determine how many candles to display based on period
            display_candles = {
                "1H": 2,      # Show last 2 hours worth of 1H candles
                "4H": 2,      # Show last 8 hours worth of 4H candles (2 x 4h)
                "1D": 30,     # Show last 30 days
                "1W": 12,     # Show last 12 weeks
                "1M": 12,     # Show last 12 months
                "3M": 12      # Show last 12 months
            }.get(selected_period, 30)
            
            # Limit display data to show only relevant timeframe
            if len(display_data) > display_candles:
                display_data = display_data.tail(display_candles)
            
            # Recalculate indicators on FULL data for accuracy
            prices = hist_data['close'].values
            
            rsi = calculate_rsi(prices)
            macd_line, signal_line, histogram = calculate_macd(prices)
            bb_mid, bb_upper, bb_lower = calculate_bollinger_bands(prices)
            
            # Graphe candlestick principal - Subplots: Candles (row1) + Volume (row2)
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                                vertical_spacing=0.02, row_heights=[0.78, 0.22])

            # Determine style based on user selection - use consistent unified premium style for ALL tickers including GOLD
            c_style = st.session_state.get("candle_style", "classic")
            # XM Platform colors - Exact match to professional standards
            # Green for bullish (up), red for bearish (down)
            inc = dict(fillcolor='#1bc47d', line=dict(color='#1bc47d', width=1.5))  # Professional green
            dec = dict(fillcolor='#ff3d3d', line=dict(color='#ff3d3d', width=1.5))  # Professional red
            
            # Force reset Plotly template to prevent style override for GOLD
            template_name = "plotly_dark"
            
            # Apply XM-style professional dark background
            fig.update_layout(
                plot_bgcolor='#0f1729',  # XM style very dark blue-black
                paper_bgcolor='#0f1729',  # Exact XM color
                font=dict(color='#ffffff', family='Arial, sans-serif'),
                title_font_size=16,
                margin=dict(l=50, r=50, t=60, b=50)
            )

            # Candlestick with improved hover and width (with robust validation)
            # Make a safe copy and coerce types - USE DISPLAY_DATA to show only relevant period
            df_candle = display_data.copy()
            required_cols = ['timestamp', 'open', 'high', 'low', 'close']
            missing = [c for c in required_cols if c not in df_candle.columns]
            if missing:
                st.warning(f"Données manquantes pour {ticker}: {missing}")
                continue

            # Ensure timestamp is datetime
            df_candle['timestamp'] = pd.to_datetime(df_candle['timestamp'], errors='coerce')

            # Coerce OHLC to numeric and drop invalid rows
            for c in ['open', 'high', 'low', 'close']:
                df_candle[c] = pd.to_numeric(df_candle[c], errors='coerce')

            df_candle = df_candle.dropna(subset=['timestamp', 'open', 'high', 'low', 'close'])
            if df_candle.empty:
                st.warning(f"Pas de données OHLC valides pour {ticker}.")
                continue

            # Sort by timestamp to avoid ordering issues
            df_candle = df_candle.sort_values('timestamp')

            try:
                # Add candlestick with unified styling that works for all tickers including GOLD
                fig.add_trace(go.Candlestick(
                    x=df_candle['timestamp'],
                    open=df_candle['open'],
                    high=df_candle['high'],
                    low=df_candle['low'],
                    close=df_candle['close'],
                    name='Prix',
                    increasing=dict(
                        fillcolor=inc['fillcolor'],
                        line=dict(color=inc['line']['color'], width=inc['line']['width'])
                    ),
                    decreasing=dict(
                        fillcolor=dec['fillcolor'],
                        line=dict(color=dec['line']['color'], width=dec['line']['width'])
                    ),
                    opacity=1.0,  # Full opacity for clarity
                    showlegend=False,
                    hovertemplate='<b>%{x|%d-%m-%Y}</b><br>Open: %{open:.2f}<br>High: %{high:.2f}<br>Low: %{low:.2f}<br>Close: %{close:.2f}<extra></extra>'
                ), row=1, col=1)
            except Exception as e:
                st.error(f"Erreur affichage bougies pour {ticker}: {e}")
                continue

            # Volume bars - synchronized with candle colors
            if 'volume' in display_data.columns:
                fig.add_trace(go.Bar(
                    x=display_data['timestamp'],
                    y=display_data['volume'],
                    marker=dict(
                        color=[inc['fillcolor'] if c >= o else dec['fillcolor'] for c, o in zip(display_data['close'], display_data['open'])],
                        opacity=0.8,
                        line=dict(width=0)
                    ),
                    name='Volume',
                    hoverinfo='y'
                ), row=2, col=1)

            # If preview requested, limit to short range and add annotation
            if st.session_state.get('preview_candle_style'):
                fig.update_layout(title=f"Preview - Style: {c_style}")
                # After showing preview once, clear flag
                st.session_state.preview_candle_style = False

            # Bollinger and other indicator overlays - Use FULL data for indicators
            if show_bollinger and bb_mid is not None:
                fig.add_trace(go.Scatter(
                    x=hist_data['timestamp'], y=bb_mid,
                    name='Bollinger Mid (20 SMA)', line=dict(color='#00d4ff', width=1.5, dash='dash')
                ), row=1, col=1)
                fig.add_trace(go.Scatter(
                    x=hist_data['timestamp'], y=bb_upper,
                    name='Bollinger Upper', line=dict(color='rgba(255,107,107,0.7)', width=1, dash='dot')
                ), row=1, col=1)
                fig.add_trace(go.Scatter(
                    x=hist_data['timestamp'], y=bb_lower,
                    name='Bollinger Lower', line=dict(color='rgba(81,207,102,0.7)', width=1, dash='dot')
                ), row=1, col=1)

            # Create title with period info
            period_names = {"1H": "1 Heure", "4H": "4 Heures", "1D": "1 Jour", "1W": "1 Semaine", "1M": "1 Mois", "3M": "3 Mois"}
            period_name = period_names.get(selected_period, "1 Jour")
            
            fig.update_layout(
                title=f"<b>{ticker} - {period_name} (Affichage: {len(df_candle)} candles)</b>",
                height=600,  # Professional height for mobile-friendly viewing
                xaxis_rangeslider_visible=False,
                template=template_name,
                hovermode='x unified',
                xaxis=dict(
                    showgrid=True, 
                    gridwidth=1, 
                    gridcolor='rgba(255,255,255,0.05)',
                    showline=True, 
                    linewidth=1, 
                    linecolor='rgba(255,255,255,0.2)'
                ),
                yaxis=dict(
                    showgrid=True, 
                    gridwidth=1, 
                    gridcolor='rgba(255,255,255,0.05)', 
                    side='right', 
                    domain=[0.25, 1.0],
                    showline=True, 
                    linewidth=1, 
                    linecolor='rgba(255,255,255,0.1)',
                    automargin=True,
                    title='Price'
                ),
                yaxis2=dict(
                    showgrid=False, 
                    domain=[0.0, 0.22], 
                    title='Volume', 
                    showline=True, 
                    linewidth=1, 
                    linecolor='rgba(255,255,255,0.1)',
                    side='right'
                ),
                plot_bgcolor='#0f1729',
                paper_bgcolor='#0f1729',
                font=dict(color='#e0e0e0', size=11, family="Arial, sans-serif"),
                margin=dict(b=70, t=80, l=50, r=70),
                title_font_size=16,
                title_x=0.5,
                showlegend=True,
                legend=dict(
                    x=0.01, 
                    y=0.97, 
                    bgcolor='rgba(15, 23, 41, 0.95)', 
                    bordercolor='rgba(255,255,255,0.08)',
                    borderwidth=1,
                    font=dict(size=10)
                ),
                separators=",."
            )

            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            if show_rsi or show_macd:
                col1, col2 = st.columns(2)
                
                if show_rsi:
                    with col1:
                        rsi_value = float(rsi[-1]) if rsi is not None else 0
                        fig_rsi = go.Figure()
                        
                        # RSI line with color based on value
                        rsi_color = '#00ff00' if rsi_value > 50 else '#ff0000'
                        fig_rsi.add_trace(go.Scatter(
                            y=rsi,
                            name='RSI',
                            line=dict(color=rsi_color, width=3),
                            fill='tozeroy',
                            fillcolor='rgba(0, 255, 0, 0.1)' if rsi_value > 50 else 'rgba(255, 0, 0, 0.1)'
                        ))
                        
                        fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", line_width=2, annotation_text="Overbought (70)")
                        fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", line_width=2, annotation_text="Oversold (30)")
                        fig_rsi.add_hline(y=50, line_dash="dot", line_color="gray", line_width=1)
                        
                        fig_rsi.update_layout(
                            title=f"RSI(14) - {ticker}: {rsi_value:.2f}",
                            height=300,
                            xaxis=dict(showgrid=True, gridcolor='#2a2a3a'),
                            yaxis=dict(showgrid=True, gridcolor='#2a2a3a'),
                            template="plotly_dark",
                            plot_bgcolor='#0a0e27',
                            paper_bgcolor='#0a0e27',
                            font=dict(color='#ffffff'),
                            hovermode='x unified'
                        )
                        st.plotly_chart(fig_rsi, use_container_width=True)
                
                if show_macd:
                    with col2:
                        fig_macd = go.Figure()
                        
                        # Histogram en barres avec couleurs red/green
                        colors = ['#ff0000' if float(h) < 0 else '#00ff00' for h in histogram]
                        fig_macd.add_trace(go.Bar(
                            y=histogram,
                            name='MACD Histogram',
                            marker=dict(color=colors, line=dict(width=0)),
                            opacity=0.7
                        ))
                        
                        # MACD line
                        fig_macd.add_trace(go.Scatter(
                            y=macd_line,
                            name='MACD Line',
                            line=dict(color='#00d4ff', width=2)
                        ))
                        
                        # Signal line
                        fig_macd.add_trace(go.Scatter(
                            y=signal_line,
                            name='Signal Line',
                            line=dict(color='#ff8800', width=2)
                        ))
                        
                        fig_macd.add_hline(y=0, line_dash="dash", line_color="gray", line_width=1)
                        
                        fig_macd.update_layout(
                            title=f"MACD - {ticker}",
                            height=300,
                            xaxis=dict(showgrid=True, gridcolor='#2a2a3a'),
                            yaxis=dict(showgrid=True, gridcolor='#2a2a3a'),
                            template="plotly_dark",
                            plot_bgcolor='#0a0e27',
                            paper_bgcolor='#0a0e27',
                            font=dict(color='#ffffff'),
                            hovermode='x unified'
                        )
                        st.plotly_chart(fig_macd, use_container_width=True)
            
            st.divider()
        
        st.markdown("---")
        st.subheader("🚨 Alertes en Temps Réel")
        
        # Check for active alerts
        all_alerts = []
        for ticker in selected_tickers:
            price_info = get_live_price(ticker)
            price = price_info.get('price', 0)
            
            # Get RSI for alert checking
            hist_data = get_historical_data(ticker, days=30)
            prices = hist_data['close'].values
            rsi = calculate_rsi(prices)
            if rsi is not None:
                ticker_alerts = check_alerts(ticker, float(rsi[-1]), price)
                all_alerts.extend(ticker_alerts)
        
        if all_alerts:
            for alert in all_alerts:
                if alert.get("severity") == "warning":
                    st.warning(alert.get("message", f"Alert: {alert['type']}"))
                elif alert.get("severity") == "error":
                    st.error(alert.get("message", f"Alert: {alert['type']}"))
                else:
                    st.info(alert.get("message", f"Alert: {alert['type']}"))
        else:
            st.success("✅ Aucune alerte active - Marché stable")
        
        st.markdown("---")
        st.subheader("4️⃣ Signaux de Trading Intelligents")
        
        for ticker in selected_tickers:
            hist_data = get_historical_data(ticker, days=30)
            prices = hist_data['close'].values
            
            smart_signals = SmartSignals(prices)
            signals = smart_signals.get_detailed_signals()
            
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("RSI", f"{signals['rsi']:.0f}")
            with col2:
                st.metric("MACD", f"{signals['macd']:.0f}")
            with col3:
                st.metric("Bollinger", f"{signals['bollinger']:.0f}")
            with col4:
                st.metric("Trend", f"{signals['trend']:.0f}")
            with col5:
                signal_text = signals['signal']
                if "BUY" in signal_text:
                    st.success(f"**{signal_text}**")
                elif "SELL" in signal_text:
                    st.error(f"**{signal_text}**")
                else:
                    st.info(f"**{signal_text}**")
        
        st.markdown("---")
        st.subheader("5️⃣ Analyse des Risques")
        
        for ticker in selected_tickers:
            hist_data = get_historical_data(ticker, days=30)
            prices = hist_data['close'].values
            
            risk_assessment = RiskAssessment(prices)
            risk_data = risk_assessment.calculate_risk_reward()
            
            st.write(f"**{ticker}**")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Entrée", f"${risk_data['entry']:.4f}")
            with col2:
                st.metric("Support", f"${risk_data['support']:.4f}")
            with col3:
                st.metric("Résistance", f"${risk_data['resistance']:.4f}")
            with col4:
                st.metric("Ratio R/R", f"{risk_data['ratio']:.2f}")
        
        st.markdown("---")
        st.subheader("6️⃣ Historique des Alertes")
        
        alert_history = get_alert_history()
        if alert_history:
            st.dataframe(
                pd.DataFrame(alert_history[-10:]).sort_values('timestamp', ascending=False),
                use_container_width=True
            )
        else:
            st.info("Aucune alerte pour le moment")
        
        st.markdown("---")
        st.subheader("7️⃣ Ressources Éducatives")
        
        concept = st.selectbox("Sélectionnez un concept:", ["RSI", "MACD", "Bollinger", "Trend", "Support", "Resistance", "Volatilite", "Momentum", "Signal", "Ratio_Risque_Rendement"])
        
        if concept:
            st.markdown(format_tooltip_markdown(concept))

def page_patterns():
    """Page Patterns & Stratégies - Intégration complète avec tabs professionnels"""
    from src.educational_content import (
        CANDLESTICK_PATTERNS,
        TRADING_STRATEGIES,
        RISK_MANAGEMENT_RULES,
        PSYCHOLOGY_RULES
    )
    
    st.title("📚 TRADING MASTERY - Patterns & Stratégies Pro")
    st.markdown("*19 Chandeliers Japonais • 4 Stratégies • Risk Management • Psychologie*")
    
    # Info bar
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric("📊 Patterns", "19", "Chandeliers")
    with col_info2:
        st.metric("📈 Stratégies", "4", "Éprouvées")
    with col_info3:
        st.metric("🎯 Mastery", "100%", "Apprentissage")
    
    st.divider()
    
    # === 4 MAIN TABS ===
    tab_candlesticks, tab_strategies, tab_risk, tab_psychology = st.tabs([
        "📊 Candlesticks (19)",
        "📈 Stratégies (4)",
        "⚠️ Risk Management",
        "🧠 Psychologie"
    ])
    
    # === TAB 1: CANDLESTICKS ===
    with tab_candlesticks:
        st.markdown("### 📊 19 Patterns Candlestick - Maîtrise Complète")
        st.markdown("Apprenez à reconnaître les 19 patterns essentiels pour trader avec précision")
        
        st.divider()
        
        # Pattern type filter
        col_filter1, col_filter2 = st.columns(2)
        with col_filter1:
            pattern_type = st.selectbox(
                "🔍 Filtrer par type:",
                ["🟢 Tous les Patterns", "🟢 Haussiers (Bullish)", "🔴 Baissiers (Bearish)"],
                key="pattern_type_filter"
            )
        with col_filter2:
            difficulty = st.selectbox(
                "📊 Niveau de Difficulté:",
                ["Tous", "Débutant", "Intermédiaire", "Avancé"],
                key="pattern_difficulty_filter"
            )
        
        st.divider()
        
        # Pattern selector
        pattern_names = list(CANDLESTICK_PATTERNS.keys())
        selected_pattern = st.selectbox(
            "🎯 **Choisir un Pattern à analyser:**",
            pattern_names,
            key="pattern_selector"
        )
        
        if selected_pattern and selected_pattern in CANDLESTICK_PATTERNS:
            pattern_info = CANDLESTICK_PATTERNS[selected_pattern]
            
            # Pattern display card
            with st.container(border=True):
                col_title, col_type = st.columns([3, 1])
                with col_title:
                    st.markdown(f"## {selected_pattern}")
                with col_type:
                    type_badge = "🟢 BULLISH" if pattern_info.get('type') == 'bullish' else "🔴 BEARISH"
                    st.markdown(f"**{type_badge}**")
                
                st.divider()
                
                # Pattern details in expanders
                col1, col2 = st.columns(2)
                
                with col1:
                    with st.expander("📖 **Description**", expanded=True):
                        st.markdown(pattern_info.get('description', 'N/A'))
                    
                    with st.expander("🎯 **Signification**"):
                        st.markdown(pattern_info.get('signification', 'N/A'))
                
                with col2:
                    with st.expander("✅ **Comment l'identifier**"):
                        st.markdown(pattern_info.get('identification', 'N/A'))
                    
                    with st.expander("💡 **Conseil de Trading**"):
                        st.markdown(pattern_info.get('trading_tip', 'N/A'))
                
                st.divider()
                
                # Reliability metrics
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.metric("📊 Fiabilité", f"{pattern_info.get('reliability', 70)}%")
                with col_m2:
                    frequency = pattern_info.get('frequency', 'Modérée')
                    st.metric("📈 Fréquence", frequency)
                with col_m3:
                    timeframe = pattern_info.get('best_timeframe', '1D')
                    st.metric("⏱️ Meilleur Timeframe", timeframe)
        
        st.divider()
        st.markdown("### 📊 Comparaison des 19 Patterns")
        st.markdown("Tableau complet de tous les patterns avec leurs caractéristiques")
        
        # Create comparison table
        patterns_data = []
        for name, info in CANDLESTICK_PATTERNS.items():
            patterns_data.append({
                "Pattern": name,
                "Type": "🟢 Haussier" if info.get('type') == 'bullish' else "🔴 Baissier",
                "Fiabilité": f"{info.get('reliability', 70)}%",
                "Fréquence": info.get('frequency', 'Modérée'),
                "Timeframe": info.get('best_timeframe', '1D')
            })
        
        patterns_df = pd.DataFrame(patterns_data)
        st.dataframe(patterns_df, use_container_width=True, hide_index=True)
    
    # === TAB 2: STRATEGIES ===
    with tab_strategies:
        st.markdown("### 📈 4 Stratégies Éprouvées")
        st.markdown("Stratégies complètes et testées en live trading")
        
        st.divider()
        
        col_strat1, col_strat2 = st.columns(2)
        with col_strat1:
            st.info("**Stratégies couvrant:** Patterns • Support/Résistance • Signaux Composites • Risk Management")
        with col_strat2:
            st.success("**Toutes les stratégies:** Backtestées ✅ • Éprouvées en Live ✅ • Rentables ✅")
        
        st.divider()
        
        # Strategy selector
        strategy_names = list(TRADING_STRATEGIES.keys())
        selected_strategy = st.selectbox(
            "🎯 **Choisir une Stratégie:**",
            strategy_names,
            key="strategy_selector"
        )
        
        if selected_strategy and selected_strategy in TRADING_STRATEGIES:
            strategy_info = TRADING_STRATEGIES[selected_strategy]
            
            with st.container(border=True):
                st.markdown(f"## {selected_strategy}")
                st.divider()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📊 Win Rate", f"{strategy_info.get('win_rate', 65)}%")
                with col2:
                    st.metric("💰 Profit Factor", f"{strategy_info.get('profit_factor', 2.1):.2f}x")
                with col3:
                    difficulty = strategy_info.get('difficulty', 'Moyen')
                    st.metric("📚 Difficulté", difficulty)
                
                st.divider()
                
                col_a, col_b = st.columns(2)
                with col_a:
                    with st.expander("📖 **Description**", expanded=True):
                        st.markdown(strategy_info.get('nom', 'N/A'))
                        st.markdown(strategy_info.get('description', 'N/A'))
                
                with col_b:
                    with st.expander("🔧 **Mise en Place**"):
                        st.markdown(strategy_info.get('setup', 'N/A'))
                
                st.divider()
                
                col_x, col_y = st.columns(2)
                with col_x:
                    with st.expander("✅ **Signaux d'Entrée**"):
                        st.markdown(strategy_info.get('entry_signals', 'N/A'))
                
                with col_y:
                    with st.expander("❌ **Signaux de Sortie**"):
                        st.markdown(strategy_info.get('exit_signals', 'N/A'))
                
                st.divider()
                
                with st.expander("💡 **Tips et Conseils**"):
                    st.markdown(strategy_info.get('tips', 'N/A'))
    
    # === TAB 3: RISK MANAGEMENT ===
    with tab_risk:
        st.markdown("### ⚠️ Gestion du Risque - La Clé du Succès")
        st.markdown("Les règles essentielles pour protéger votre capital et maximiser les gains")
        
        st.divider()
        
        # Risk calculator
        col_calc1, col_calc2 = st.columns(2)
        
        with col_calc1:
            st.markdown("#### 📊 Calculateur de Risque")
            account_balance = st.number_input("💰 Solde du compte ($):", min_value=100, value=10000, key="risk_account")
            risk_percent = st.slider("📊 Risque par trade (%):", 0.5, 2.0, 1.0, 0.1, key="risk_slider")
            entry_price = st.number_input("📈 Prix d'entrée ($):", min_value=0.01, value=100.0, key="risk_entry")
            stop_loss = st.number_input("📉 Stop Loss ($):", min_value=0.01, value=95.0, key="risk_stop")
        
        with col_calc2:
            st.markdown("#### 📈 Résultats")
            risk_amount = account_balance * (risk_percent / 100)
            pips_risk = abs(entry_price - stop_loss)
            lot_size = risk_amount / pips_risk if pips_risk > 0 else 0
            
            st.metric("💵 Risque ($)", f"${risk_amount:.2f}")
            st.metric("📍 Pips en Risque", f"{pips_risk:.4f}")
            st.metric("📦 Taille Lot", f"{lot_size:.2f}")
            
            # Risk/Reward ratio
            if pips_risk > 0:
                take_profit = st.number_input("🎯 Take Profit ($):", min_value=entry_price + 0.01, value=110.0, key="risk_tp")
                pips_gain = abs(take_profit - entry_price)
                rr_ratio = pips_gain / pips_risk
                
                if rr_ratio >= 2.0:
                    st.success(f"✅ **Ratio R/R: {rr_ratio:.2f}** (EXCELLENT)")
                elif rr_ratio >= 1.5:
                    st.info(f"✅ **Ratio R/R: {rr_ratio:.2f}** (BON)")
                else:
                    st.warning(f"⚠️ **Ratio R/R: {rr_ratio:.2f}** (À AMÉLIORER)")
        
        st.divider()
        
        # Risk rules display
        st.markdown("#### 📖 Règles Fondamentales de Risk Management")
        
        for idx, rule in enumerate(RISK_MANAGEMENT_RULES, 1):
            with st.expander(f"🔹 **Règle {idx}: {rule.get('titre', 'N/A')}**"):
                st.markdown(f"**Description:** {rule.get('description', 'N/A')}")
                st.markdown(f"**Points clés:** {rule.get('points_cles', 'N/A')}")
                st.markdown(f"**Exemple:** {rule.get('exemple', 'N/A')}")
    
    # === TAB 4: PSYCHOLOGY ===
    with tab_psychology:
        st.markdown("### 🧠 Psychologie du Trading - Discipline > Prédiction")
        st.markdown("Maîtriser votre psychologie est plus important que vos indicateurs")
        
        st.divider()
        
        # Psychology metrics
        col_psy1, col_psy2, col_psy3 = st.columns(3)
        with col_psy1:
            st.metric("🧠 Impact Psychologie", "50-70%", "Du succès")
        with col_psy2:
            st.metric("📊 Impact Analyse", "20-30%", "Du succès")
        with col_psy3:
            st.metric("💰 Discipline", "★★★★★", "Essentielle")
        
        st.divider()
        
        # Psychology rules
        st.markdown("#### 📖 Règles de Psychologie du Trading")
        
        for idx, rule in enumerate(PSYCHOLOGY_RULES, 1):
            with st.expander(f"🧠 **Règle {idx}: {rule.get('titre', 'N/A')}**"):
                st.markdown(f"**Problème:** {rule.get('probleme', 'N/A')}")
                st.markdown(f"**Solution:** {rule.get('solution', 'N/A')}")
                st.markdown(f"**Action:** {rule.get('action', 'N/A')}")
        
        st.divider()
        
        # Discipline quiz
        st.markdown("#### 🎯 Quiz: Testez Votre Discipline")
        
        with st.form("psychology_quiz"):
            q1 = st.radio("❌ J'ai perdu mon dernier trade. Je dois:", [
                "Ignorer la perte et trader plus agressif",
                "Analyser la perte calmement avant le prochain trade",
                "Doubler ma mise pour compenser"
            ])
            
            q2 = st.radio("📊 Face à un trade gagnant:", [
                "Fermer très tôt par peur de perdre le gain",
                "Laisser mon TP faire son travail",
                "Ajouter à la position"
            ])
            
            q3 = st.radio("⏱️ Avant chaque trade:", [
                "Checker rapidement les news",
                "Suivre mon plan sans distraction",
                "Écouter les autres traders"
            ])
            
            if st.form_submit_button("📊 Voir mon Score", use_container_width=True):
                score = 0
                if q1 == "Analyser la perte calmement avant le prochain trade": score += 1
                if q2 == "Laisser mon TP faire son travail": score += 1
                if q3 == "Suivre mon plan sans distraction": score += 1
                
                if score == 3:
                    st.success("🏆 **EXCELLENT (3/3)** - Vous avez une excellente discipline!")
                elif score == 2:
                    st.info("✅ **BON (2/3)** - Travaillez sur les points faibles")
                else:
                    st.warning("📈 **À AMÉLIORER (0-1/3)** - Discipline prioritaire!")


def main():
    """Application principale - Routing et navigation"""
    init_session_state()
    apply_custom_theme()
    
    # Initialize sidebar navigation
    st.sidebar.title("📊 DUBAI TRADING TOOLS")
    st.sidebar.caption("v6.1 - Professional Trading Platform")
    st.sidebar.divider()
    
    page = st.sidebar.radio(
        "🗺️ Navigation",
        ["📈 Dashboard", "📰 Actualités IA", "📚 Patterns & Stratégies", "🎓 Tutorial", "⚙️ Profile"],
        label_visibility="collapsed"
    )
    
    st.sidebar.divider()
    st.sidebar.markdown("### 📊 Stats")
    st.sidebar.caption("✅ Platform Live")
    st.sidebar.caption("🔴 Real-time Data")
    st.sidebar.caption("🚀 11 Actifs")
    st.sidebar.caption("📈 6 Périodes")
    
    st.sidebar.divider()
    
    # Route to appropriate page
    if not st.session_state.get("logged_in", False):
        page_login_register()
    elif page == "📈 Dashboard":
        page_dashboard()
    elif page == "📰 Actualités IA":
        page_news_ai()
    elif page == "📚 Patterns & Stratégies":
        page_patterns()
    elif page == "🎓 Tutorial":
        page_tutorial()
    elif page == "⚙️ Profile":
        st.title("⚙️ Paramètres du Compte")
        col_prof1, col_prof2 = st.columns(2)
        with col_prof1:
            st.metric("👤 Utilisateur", st.session_state.get("user_name", "Guest"))
            st.metric("📊 Statut", "Connecté ✅")
        with col_prof2:
            st.metric("🔐 Email", st.session_state.get("user_email", "N/A"))
            st.metric("📅 Membre depuis", "2025")
        
        st.divider()
        
        if st.button("🚪 Déconnecter", use_container_width=True):
            logout(st)
            st.rerun()


if __name__ == "__main__":
    main()


if __name__ == '__main__':
    main()
