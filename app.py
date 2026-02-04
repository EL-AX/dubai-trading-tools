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
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import requests

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
    
    # Format price with animation effect
    if price > 0:
        price_str = f"${price:,.2f}"
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
        - Vérifiez régulièrement vos paramètres de compte
        """)
    
    with st.expander("📊 2. Tableau de Bord - Votre Centre de Contrôle"):
        st.markdown("""
        **🎯 Sélection des Actifs**
        - Choisissez jusqu'à 8 actifs à analyser simultanément
        - **Crypto**: BTC (Bitcoin), ETH (Ethereum), SOL (Solana)
        - **Forex**: EUR, GBP, JPY, AUD (parités de change)
        - **Matières**: XAU (Or / Gold)
        
        **💹 Prix en Temps Réel**
        - Prix instantané avec changement 24h
        - Volume 24h et capitalisation boursière
        - Mise à jour automatique toutes les 5 minutes
        - Indicateurs visuels: 🟢 (hausse), 🔴 (baisse)
        
        **📈 Graphiques Interactifs**
        - Bougies (Candlestick) sur 30 jours
        - Bandes de Bollinger pour la volatilité
        - Volume d'échange synchronisé
        - Styles personnalisables: Classic, Boxy, Thin, Model
        
        **🚨 Signaux & Alertes**
        - Signaux composites automatiques (STRONG_BUY à STRONG_SELL)
        - Alertes pour RSI, volatilité, changements 24h
        - Activez/désactivez les alertes dans les paramètres
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
        - Attendez STRONG_BUY (>80) pour acheter
        - Attendez STRONG_SELL (<20) pour vendre
        - Combinez avec les bandes de Bollinger pour confirmation
        
        **Stratégie Avancée (Professionnels)**
        - Utilisez RSI + MACD + Bollinger ensemble
        - Cherchez les divergences (prix monte, RSI baisse = signal faible)
        - Identifiez les zones de support/résistance
        - Gérez votre risque avec stop-loss et take-profit
        
        **Gestion du Risque**
        - Risquez jamais >2% du portefeuille par trade
        - Définissez un ratio risque/récompense minimum 1:2
        - Utilisez les alertes pour détecter les mouvements
        - Diversifiez sur plusieurs actifs
        
        **Utilisation des Alertes**
        1. Activez les alertes dans Paramètres
        2. L'app monitore RSI, volatilité, changements 24h
        3. Revenez régulièrement pour vérifier les signaux
        4. Combiné avec une stratégie pour plus de robustesse
        """)
    
    with st.expander("⚙️ 5. Paramètres & Configuration"):
        st.markdown("""
        **Devise Préférée**
        - Choisissez entre USD, EUR, GBP
        - Tous les prix seront affichés dans cette devise
        
        **Style des Bougies**
        - **Classic**: Apparence traditionnelle
        - **Boxy**: Bougies plus carrées
        - **Thin**: Bougies fines (pour beaucoup de données)
        - **Model**: Style premium professionnel
        
        **Alertes**
        - Activez/désactivez les notifications
        - Consultez l'historique des alertes déclenchées
        - Archivez les anciennes alertes
        
        **Sauvegarde**
        - Les paramètres sont automatiquement sauvegardés
        - Ils persistent entre les sessions
        """)
    
    with st.expander("❓ 6. FAQ & Dépannage"):
        st.markdown("""
        **Q: Pourquoi les prix ne se mettent pas à jour?**
        A: L'app s'actualise toutes les 5 minutes. Attendez ou recharger la page.
        
        **Q: Les bougies ne s'affichent pas?**
        A: Cela peut signifier qu'il n'y a pas assez de données. Attendez 24h pour plus de points.
        
        **Q: Comment interpréter les signaux?**
        A: Consultez la section "Indicateurs Techniques" ci-dessus pour chaque métrique.
        
        **Q: Puis-je trader en direct?**
        A: Cette app est un **outil d'analyse**, pas une plateforme de trading. Utilisez une plateforme (Binance, Kraken, etc.)
        
        **Q: Mes données sont-elles sécurisées?**
        A: Oui. Mot de passe hashé, emails vérifiés, données encryptées.
        """)
    
    st.divider()
    st.info("💡 **Conseil Pro**: Testez vos stratégies avec les graphiques en papier avant d'investir de l'argent réel. Les performances passées n'indiquent pas les performances futures.")
    
    with st.expander("🎯 4. Signaux de Trading"):
        st.markdown("""
        L'app génère automatiquement des signaux basés sur 4 indicateurs:
        
        - 🔴 **STRONG_BUY**: Score 80-100 (forte opportunité d'achat)
        - 🟢 **BUY**: Score 60-80 (opportunité d'achat)
        - 🟡 **NEUTRAL**: Score 40-60 (pas de signal clair)
        - 🟠 **SELL**: Score 20-40 (vendre potentiellement)
        - 🔴 **STRONG_SELL**: Score 0-20 (forte vente recommandée)
        """)
    
    with st.expander("⚠️ 5. Analyse des Risques"):
        st.markdown("""
        **Support & Résistance**
        - Support: Niveau où le prix a du mal à descendre
        - Résistance: Niveau où le prix a du mal à monter
        
        **Risk/Reward Ratio**
        - Ratio = Profit potentiel / Risque potentiel
        - Bon ratio ≥ 2:1
        - Aide à planifier les entrées/sorties
        """)
    
    with st.expander("⚙️ 6. Paramètres"):
        st.markdown("""
        **Thème**: Changez entre mode clair et sombre
        **Devise**: Sélectionnez votre devise préférée
        **Alertes**: Activez/désactivez les notifications
        """)
    
    st.divider()
    st.info("💡 Astuce: L'app s'actualise toutes les 5 minutes pour des prix en temps réel.")

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
    """Section actualités IA en temps réel - Vraies sources (Reddit, RSS, CoinGecko)"""
    st.title("📰 Actualités Temps Réel - Sources Réelles")
    if st.button("🔄 Actualiser", use_container_width=True):
        # Force clear cache and refresh
        from src.cache import CacheManager
        cache = CacheManager()
        cache.delete("real_news_all")
        st.rerun()
    
    # Get REAL news from real sources
    from src.real_news import get_all_real_news
    news_items = get_all_real_news()
    
    st.info("✅ Cache 10min | Sources réelles: Reddit, RSS (CoinDesk, CoinTelegraph), CoinGecko Trending")
    if news_items:
        sentiments = [n.get('sentiment', 'neutral') for n in news_items]
        bullish_count = sentiments.count('bullish')
        bearish_count = sentiments.count('bearish')
        neutral_count = sentiments.count('neutral')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📈 Bullish", f"{bullish_count}")
        with col2:
            st.metric("📉 Bearish", f"{bearish_count}")
        with col3:
            st.metric("➡️ Neutre", f"{neutral_count}")
        with col4:
            st.metric("📊 Total", f"{len(news_items)}")
        st.divider()
        for idx, news in enumerate(news_items, 1):
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"**{idx}. {news.get('titre', 'N/A')}**")
                with col2:
                    symbol = news.get('symbol', '')
                    if symbol:
                        st.code(symbol, language="")
                with col3:
                    if news.get('sentiment') == 'bullish':
                        st.success("📈 HAUSSIER")
                    elif news.get('sentiment') == 'bearish':
                        st.error("📉 BAISSIER")
                    else:
                        st.info("➡️ NEUTRE")
                resume = news.get('resume', 'N/A')
                st.markdown(f"{resume}")
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"📌 **Source:** {news.get('source', 'Unknown')}")
                with col2:
                    url = news.get('url', '')
                    if url:
                        st.markdown(f"[🔗 Lire]({url})")
                st.divider()
    else:
        st.warning("❌ Aucune news disponible pour le moment. Les APIs peuvent être momentanément indisponibles.")

def page_dashboard():
    st.title("📊 Tableau de Bord")
    if st.button("Se déconnecter", key="btn_logout", use_container_width=True):
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
    
    st.write(f"**Utilisateur:** {st.session_state.user_name}")
    
    st.markdown("---")
    st.subheader("1️⃣ Sélection des Actifs")
    
    # ALL supported tickers
    tickers = ["BTC", "ETH", "SOL", "ADA", "XRP", "DOT", "EUR", "GBP", "JPY", "AUD", "XAU"]
    selected_tickers = st.multiselect("Sélectionnez les actifs à analyser:", tickers, default=["BTC", "EUR"])
    
    if selected_tickers:
        st.markdown("---")
        st.subheader("2️⃣ Prix en Temps Réel 📊 (Mise à jour automatique)")
        
        # Display last update time
        from datetime import datetime as dt
        now = dt.now().strftime("%H:%M:%S")
        st.caption(f"🔄 Dernière mise à jour: {now} | Les prix s'actualisent automatiquement (comme une montre de sport)")
        
        # Add auto-refresh for live prices (like a sports watch)
        if "price_refresh_counter" not in st.session_state:
            st.session_state.price_refresh_counter = 0
        
        # Placeholder for refresh button
        col_refresh = st.columns([5, 1])[1]
        with col_refresh:
            if st.button("🔄", key="refresh_prices", use_container_width=True):
                st.session_state.price_refresh_counter += 1
                st.rerun()
        
        price_cols = st.columns(len(selected_tickers))
        prices_data = {}
        
        for idx, ticker in enumerate(selected_tickers):
            with price_cols[idx]:
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
        
        st.markdown("---")
        st.subheader("3️⃣ Graphiques et Indicateurs")
        
        st.info("📊 Sélectionnez les indicateurs à afficher sur tous les graphes:")
        col1, col2, col3 = st.columns(3)
        with col1:
            show_rsi = st.checkbox("RSI (14)", value=True)
        with col2:
            show_macd = st.checkbox("MACD", value=True)
        with col3:
            show_bollinger = st.checkbox("Bollinger Bands", value=True)
        
        st.markdown("---")
        
        # Afficher un graphe pour CHAQUE crypto sélectionnée
        for ticker in selected_tickers:
            st.subheader(f"📈 {ticker} - Analyse Technique Complète")
            
            hist_data = get_historical_data(ticker, days=10)
            
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
            
            prices = hist_data['close'].values
            
            rsi = calculate_rsi(prices)
            macd_line, signal_line, histogram = calculate_macd(prices)
            bb_mid, bb_upper, bb_lower = calculate_bollinger_bands(prices)
            
            # Graphe candlestick principal - Subplots: Candles (row1) + Volume (row2)
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                                vertical_spacing=0.02, row_heights=[0.78, 0.22])

            # Determine style based on user selection - use consistent unified premium style for ALL tickers including GOLD
            c_style = st.session_state.get("candle_style", "classic")
            # Unified premium model style that works consistently for all tickers including GOLD
            # Green for bullish (up), red for bearish (down)
            inc = dict(fillcolor='#17957b', line=dict(color='#17957b', width=4))
            dec = dict(fillcolor='#e83a4a', line=dict(color='#e83a4a', width=4))
            
            # Force reset Plotly template to prevent style override for GOLD
            template_name = "plotly_dark"
            
            # Apply dark premium background for all styles
            fig.update_layout(
                plot_bgcolor='#0f1419', 
                paper_bgcolor='#0f1419', 
                font=dict(color='#ffffff', family='Arial, sans-serif'),
                title_font_size=16,
                margin=dict(l=50, r=50, t=60, b=50)
            )

            # Candlestick with improved hover and width (with robust validation)
            # Make a safe copy and coerce types
            df_candle = hist_data.copy()
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
                    x=df_candle['timestamp'].tolist(),
                    open=df_candle['open'].tolist(),
                    high=df_candle['high'].tolist(),
                    low=df_candle['low'].tolist(),
                    close=df_candle['close'].tolist(),
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
            if 'volume' in hist_data.columns:
                fig.add_trace(go.Bar(
                    x=hist_data['timestamp'],
                    y=hist_data['volume'],
                    marker=dict(
                        color=[inc['fillcolor'] if c >= o else dec['fillcolor'] for c, o in zip(hist_data['close'], hist_data['open'])],
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

            # Bollinger and other indicator overlays
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

            fig.update_layout(
                title=f"<b>{ticker} - Analyse Candlestick (30J)</b>",
                height=900,  # Increased height for better visibility
                xaxis_rangeslider_visible=False,
                template=template_name,  # Use the template variable to ensure consistency
                hovermode='x unified',
                xaxis=dict(
                    showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.08)',
                    showline=True, linewidth=1, linecolor='rgba(255,255,255,0.2)',
                    type='date'
                ),
                yaxis=dict(
                    showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.08)', 
                    side='right', domain=[0.22, 1.0],
                    showline=True, linewidth=1, linecolor='rgba(255,255,255,0.2)',
                    automargin=True
                ),
                yaxis2=dict(
                    showgrid=False, domain=[0.0, 0.18], 
                    title='Volume', 
                    showline=True, linewidth=1, linecolor='rgba(255,255,255,0.2)'
                ),
                plot_bgcolor='#0f1419',
                paper_bgcolor='#0f1419',
                font=dict(color='#e0e0e0', size=12, family="Arial, Helvetica, sans-serif"),
                margin=dict(b=80, t=100, l=60, r=80),
                title_font_size=18,
                showlegend=True,
                legend=dict(
                    x=0.01, y=0.97, 
                    bgcolor='rgba(15, 20, 25, 0.95)', 
                    bordercolor='#17957b', 
                    borderwidth=2, 
                    font=dict(size=10, color='#e0e0e0')
                )
            )

            st.plotly_chart(fig, use_container_width=True)
            
            # Afficher les indicateurs en sous-graphes
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
    """Page Patterns & Stratégies - Intégration complète des PDFs d'apprentissage"""
    from src.educational_content import (
        CANDLESTICK_PATTERNS,
        TRADING_STRATEGIES,
        RISK_MANAGEMENT_RULES,
        PSYCHOLOGY_RULES
    )
    
    st.markdown("# 📚 Patterns Candlestick & Stratégies de Trading")
    st.markdown("*Basé sur les PDFs éducatifs: '19 Chandeliers Japonais', 'Stratégie de Trading', etc.*")
    
    st.divider()
    
    tabs = st.tabs([
        "🕯️ Patterns (19)",
        "📈 Stratégies (4)",
        "⚠️ Gestion Risque (5)",
        "🧠 Psychologie (7)",
        "✅ Checklist"
    ])
    
    # ============================================================================
    # TAB 1: PATTERNS CANDLESTICK
    # ============================================================================
    with tabs[0]:
        st.header("19 Chandeliers Japonais Essentiels")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            pattern_selected = st.selectbox(
                "🎯 Choisissez un pattern:",
                list(CANDLESTICK_PATTERNS.keys()),
                key="pattern_select"
            )
        
        if pattern_selected:
            pattern_info = CANDLESTICK_PATTERNS[pattern_selected]
            
            with col2:
                st.subheader(f"✨ {pattern_info.get('traduction_fr', pattern_selected)}")
            
            col_info1, col_info2, col_info3 = st.columns(3)
            
            with col_info1:
                st.markdown("**📍 Description**")
                st.write(pattern_info.get("description", ""))
            
            with col_info2:
                st.markdown("**🎯 Signal**")
                st.write(pattern_info.get("signal", ""))
            
            with col_info3:
                st.markdown("**💡 Utilisation**")
                st.write(pattern_info.get("usage", ""))
            
            st.divider()
            st.markdown("### 💰 Conseil de Trading")
            st.info(f"""
            **Comment trader ce pattern:**
            1. Identifiez-le sur le graphique (candlestick de 1h ou 4h pour plus de fiabilité)
            2. Attendez une **confirmation du volume** (volume > moyenne 20j)
            3. Entrez **au-delà du pattern** (+ 0.5% pour sécurité)
            4. **Stop loss**: Sous le low du pattern (pour haussier) ou au-dessus du high (pour baissier)
            5. **Objectif**: Ratio risque/bénéfice minimum 1:2
            """)
        
        st.divider()
        st.subheader("📊 Comparaison des 19 Patterns")
        
        comparison_data = []
        for name, info in CANDLESTICK_PATTERNS.items():
            comparison_data.append({
                "Pattern": info.get("traduction_fr", name),
                "Signal": info.get("signal", ""),
                "Fiabilité": "Haute" if "Étoile" in name else "Moyenne" if "Engulfing" in name else "Bonne"
            })
        
        st.dataframe(comparison_data, use_container_width=True)
    
    # ============================================================================
    # TAB 2: STRATÉGIES DE TRADING
    # ============================================================================
    with tabs[1]:
        st.header("Stratégies de Trading Éprouvées")
        
        strategy_selected = st.selectbox(
            "Choisissez une stratégie:",
            list(TRADING_STRATEGIES.keys()),
            key="strategy_select"
        )
        
        if strategy_selected:
            strategy_info = TRADING_STRATEGIES[strategy_selected]
            
            st.subheader(f"📈 {strategy_info.get('nom', '')}")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("**Description**")
                st.write(strategy_info.get("description", ""))
                
                st.markdown("**✅ Avantages**")
                for advantage in strategy_info.get("avantages", []):
                    st.write(f"• {advantage}")
            
            with col2:
                st.markdown("**⚠️ Risques**")
                for risk in strategy_info.get("risques", []):
                    st.write(f"• {risk}")
            
            st.divider()
            st.markdown("### 📝 Étapes de Mise en Œuvre")
            
            for step in strategy_info.get("étapes", []):
                st.write(step)
    
    # ============================================================================
    # TAB 3: GESTION DU RISQUE
    # ============================================================================
    with tabs[2]:
        st.header("⚠️ Gestion du Risque - 5 Règles Inviolables")
        
        for rule_key, rule_info in RISK_MANAGEMENT_RULES.items():
            with st.expander(f"📋 {rule_info['titre']}", expanded=False):
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("**La Règle**")
                    st.info(rule_info['règle'])
                    
                    st.markdown("**Exemple**")
                    st.write(rule_info['exemple'])
                
                with col2:
                    st.markdown("**❌ Erreur Courante**")
                    st.error(rule_info['erreur'])
                    
                    st.markdown("**✅ Solution**")
                    st.success(rule_info['solution'])
        
        st.divider()
        st.subheader("🧮 Calculateur de Position Sizing")
        
        col_calc1, col_calc2, col_calc3 = st.columns(3)
        
        with col_calc1:
            account_balance = st.number_input("💰 Solde du compte ($):", min_value=100, value=10000)
        
        with col_calc2:
            risk_percent = st.slider("📊 Risque par trade (%):", 0.5, 2.0, 1.0, 0.1)
        
        with col_calc3:
            entry_price = st.number_input("📈 Prix d'entrée ($):", min_value=0.01, value=100.0)
        
        risk_amount = account_balance * (risk_percent / 100)
        stop_loss_price = st.number_input("🛑 Prix du stop loss ($):", min_value=0.01, value=95.0)
        
        risk_per_unit = abs(entry_price - stop_loss_price)
        if risk_per_unit > 0:
            position_size = risk_amount / risk_per_unit
            position_size_usd = position_size * entry_price
        else:
            position_size = 0
            position_size_usd = 0
        
        st.divider()
        
        res_col1, res_col2, res_col3 = st.columns(3)
        
        with res_col1:
            st.metric("💵 Montant à Risquer", f"${risk_amount:.2f}")
        
        with res_col2:
            st.metric("📦 Taille Position", f"{position_size:.2f} unités")
        
        with res_col3:
            st.metric("💳 Total Investi", f"${position_size_usd:.2f}")
        
        if position_size_usd > account_balance:
            st.error("❌ ATTENTION: Position dépasse votre solde!")
        elif position_size_usd > account_balance * 0.5:
            st.warning("⚠️ PRUDENCE: Position représente >50% du compte")
        else:
            st.success("✅ Position conforme aux règles de gestion du risque")
    
    # ============================================================================
    # TAB 4: PSYCHOLOGIE DU TRADER
    # ============================================================================
    with tabs[3]:
        st.header("🧠 Psychologie du Trader - Principes Fondamentaux")
        
        st.markdown("### Les 7 Règles de Psychologie pour Profiter Long-Terme")
        
        for rule, description in PSYCHOLOGY_RULES.items():
            rule_clean = rule.replace("_", " ")
            st.success(f"**{rule_clean}**: {description}")
        
        st.divider()
        
        st.subheader("❓ Quiz: Êtes-vous Prêt Psychologiquement?")
        
        quiz_questions = [
            "Acceptez-vous les petites pertes sans 'revenge trading'?",
            "Suivez-vous votre plan 100% même si ça semble stupide?",
            "Pouvez-vous rester calme lors des -2% de baisse?",
            "Maintenez-vous votre taille position même après une victoire?",
            "Documentez-vous CHAQUE trade dans un journal?",
            "Avez-vous des règles d'arrêt quotidien (perte max)?",
            "Pouvez-vous supporter un losing streak de 5 trades?",
        ]
        
        score = 0
        for i, question in enumerate(quiz_questions):
            answer = st.checkbox(question, key=f"quiz_{i}")
            if answer:
                score += 1
        
        st.divider()
        
        if st.button("📊 Voir votre Score"):
            percentage = (score / len(quiz_questions)) * 100
            
            st.markdown(f"### Votre Score: {score}/{len(quiz_questions)} ({percentage:.0f}%)")
            
            if percentage >= 80:
                st.success("🎉 **EXCELLENT**: Vous êtes mentalement préparé pour trader professionnel")
            elif percentage >= 60:
                st.info("📈 **BON**: Travaillez sur les points faibles pour être plus discipliné")
            else:
                st.warning("⚠️ **À AMÉLIORER**: Prenez du recul et travaillez votre mentalité avant de trader")
    
    # ============================================================================
    # TAB 5: CHECKLIST PRÉ-TRADE
    # ============================================================================
    with tabs[4]:
        st.header("✅ Checklist Avant Chaque Trade")
        
        st.markdown("### Suivez cette checklist AVANT d'entrer en position:")
        
        checklist_items = {
            "📍 Support/Résistance": "Zone identifiée et confirmée (2-3 touches)",
            "📈 Pattern Identifié": "Chandelier ou pattern reconnaissable",
            "🎯 Signaux Confirmés": "STRONG_BUY ou au minimum BUY (RSI + MACD + Bollinger)",
            "📊 Volume": "Volume > moyenne 20 jours (confirmation)",
            "🛑 Stop Loss": "Défini AVANT l'entrée (sous support ou au-dessus high)",
            "💰 Position Size": "Risque = 1-2% du compte maximum",
            "📈 Ratio R:B": "Au minimum 1:2, mieux 1:3",
            "📚 Tendance": "Confirmée (prix > MA20 > MA50 > MA200 pour haussier)",
            "🔔 Alertes": "Configurées pour gérer la sortie",
            "📝 Journal": "Raison du trade notée avant entrée"
        }
        
        checked_items = 0
        for item, description in checklist_items.items():
            col_check, col_text = st.columns([0.5, 2])
            with col_check:
                checked = st.checkbox("", key=f"check_{item}")
            with col_text:
                st.write(f"**{item}** - {description}")
            if checked:
                checked_items += 1
        
        st.divider()
        
        completion_percent = (checked_items / len(checklist_items)) * 100
        st.progress(completion_percent / 100)
        st.markdown(f"### Complété: {checked_items}/{len(checklist_items)} items ({completion_percent:.0f}%)")
        
        if checked_items == len(checklist_items):
            st.success("✅ **PRÊT À TRADER**: Tous les critères sont remplis!")
        elif checked_items >= len(checklist_items) * 0.8:
            st.info("⚠️ Presque prêt: Complétez les derniers points")
        else:
            st.warning("🚫 Ne pas trader encore: Complétez la checklist d'abord")

def page_settings():
    st.markdown("## ⚙️ Paramètres")
    
    st.divider()
    
    settings = get_user_settings(st.session_state.user_email)
    
    st.subheader("Préférences Utilisateur")
    
    alerts_enabled = st.checkbox("Activer les alertes", value=settings.get("alerts_enabled", True))
    currency = st.selectbox("Devise préférée:", ["USD", "EUR", "GBP"], index=0 if settings.get("currency") == "USD" else (1 if settings.get("currency") == "EUR" else 2))
    candle_style = st.selectbox("Style des bougies:", ["classic", "boxy", "thin", "Modèle"], index=0 if settings.get("candle_style", "classic") == "classic" else (1 if settings.get("candle_style") == "boxy" else (2 if settings.get("candle_style") == "thin" else 3)))
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        if st.button("💾 Enregistrer les paramètres", use_container_width=True):
            settings["alerts_enabled"] = alerts_enabled
            settings["currency"] = currency
            settings["candle_style"] = candle_style
            save_user_settings(st.session_state.user_email, settings)
            # Apply to current session immediately
            st.session_state.alerts_enabled = alerts_enabled
            st.session_state.currency = currency
            st.session_state.candle_style = candle_style
            st.success("✅ Paramètres enregistrés!")
            st.rerun()
    
    with col2:
        if st.button("👁️ Aperçu", use_container_width=True):
            st.session_state.preview_candle_style = True
            st.session_state.candle_style = candle_style
            st.info(f"Aperçu: {candle_style}")
    
    with col3:
        if st.button("❌ Annuler", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()

def main():
    # Initialize WebSocket feeds for real-time prices
    try:
        from src.websocket_feeds import initialize_realtime_feeds
        if "websockets_initialized" not in st.session_state:
            initialize_realtime_feeds()
            st.session_state.websockets_initialized = True
    except:
        pass
    
    # Initialize session state early so theme and preferences can be applied immediately
    init_session_state(st)
    if "user_language" not in st.session_state:
        st.session_state.user_language = "fr"
    apply_custom_theme()
    init_session_state(st)

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_email" not in st.session_state:
        st.session_state.user_email = None
    if "user_name" not in st.session_state:
        st.session_state.user_name = None
    # Default candle style
    if "candle_style" not in st.session_state:
        st.session_state.candle_style = "classic"
    
    show_header()
    
    if not st.session_state.authenticated:
        page_login_register()
    else:
        if "current_page" not in st.session_state:
            st.session_state.current_page = "dashboard"
        
        with st.sidebar:
            st.title("📍 Navigation")
            menu_options = [
                "📊 Tableau de Bord",
                "📚 Tutoriel",
                "🕯️ Patterns",
                "📰 Actualités IA",
                "⚙️ Paramètres"
            ]
            current_index = 0
            if st.session_state.current_page == "tutorial":
                current_index = 1
            elif st.session_state.current_page == "patterns":
                current_index = 2
            elif st.session_state.current_page == "news":
                current_index = 3
            elif st.session_state.current_page == "settings":
                current_index = 4
            
            page = st.radio("Menu:", menu_options, index=current_index, key="page_selector")
            
            # Map selection to page
            page_map = {
                menu_options[0]: "dashboard",
                menu_options[1]: "tutorial",
                menu_options[2]: "patterns",
                menu_options[3]: "news",
                menu_options[4]: "settings"
            }
            
            if page in page_map:
                st.session_state.current_page = page_map[page]
        
        if st.session_state.current_page == "dashboard":
            page_dashboard()
        elif st.session_state.current_page == "tutorial":
            page_tutorial()
        elif st.session_state.current_page == "patterns":
            page_patterns()
        elif st.session_state.current_page == "news":
            page_news_ai()
        elif st.session_state.current_page == "settings":
            page_settings()
        
        # Footer with copyright
        st.divider()
        st.markdown("""
        <div style='text-align: center; color: #888; font-size: 0.85rem; margin-top: 40px; padding: 20px;'>
        <p>© 2025-2026 <strong>ELOADXFAMILY</strong> - Tous droits réservés</p>
        <p><em>Dubai Trading Tools - Professional Trading Dashboard</em></p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

