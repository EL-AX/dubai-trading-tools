import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import pytz
from datetime import datetime, timedelta
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="AI Market Hunter - Dubai Edition",
    layout="wide",
    page_icon="📈",
    initial_sidebar_state="expanded"
)

# Titre principal
st.title("🚀 AI Market Hunter - Dubai Edition")
st.markdown("### Développé par un passionné d'IA & Trading | Expertise pratique > Diplômes théoriques")
st.markdown("Cet outil analyse la dynamique des prix pour détecter des opportunités sur les marchés actifs à Dubaï. **Outil éducatif - Pas conseil financier**")

# ========================================
# FONCTION generate_mock_data - TOUJOURS ACTIVE (pas de dépendance yfinance)
# ========================================
def generate_mock_data(ticker="BTC-USD", hours=100):
    """Génère TOUJOURS des données simulées réalistes - fallback garanti"""
    now = datetime.now()
    dates = pd.date_range(end=now, periods=hours, freq='1h')
    
    # Prix de base selon l'actif
    base_price = 50000 if "BTC" in ticker else 2000 if "XAU" in ticker else 100
    
    # Créer une série avec tendance + volatilité réaliste
    np.random.seed(42)  # Pour la reproductibilité
    noise = np.random.randn(hours) * (base_price * 0.005)
    trend = np.linspace(0, base_price * 0.05, hours)
    prices = base_price + trend + np.cumsum(noise)
    
    # Créer le DataFrame
    df = pd.DataFrame({
        'Open': prices * 0.998,
        'High': prices * 1.005,
        'Low': prices * 0.995,
        'Close': prices,
        'Volume': np.random.randint(1000, 50000, hours)
    }, index=dates)
    
    return df

# ========================================
# FONCTION calculate_rsi - NATIVE SANS DÉPENDANCES
# ========================================
def calculate_rsi(prices, period=14):
    """Calcul RSI natif sans dépendances externes"""
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()
    
    rs = avg_gain / avg_loss.replace(0, float('nan'))
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)  # Valeur neutre si calcul impossible

# Sidebar Dubai-specific
def add_dubai_features():
    dubai_time = datetime.now(pytz.timezone('Asia/Dubai'))
    st.sidebar.markdown(f"### 📆 **Date Dubaï** : {dubai_time.strftime('%d/%m/%Y')}")
    st.sidebar.markdown(f"### 🕐 **Heure Dubaï** : {dubai_time.strftime('%H:%M:%S')}")
    st.sidebar.markdown("### 🌟 **Marchés Dubai**")
    st.sidebar.markdown("• Bitcoin (BTC/USD) - Marché 24/7")
    st.sidebar.markdown("• Or (XAU/USD) - Actif refuge populaire")
    st.sidebar.caption("⚠️ Outil éducatif - Conforme réglementation UAE")

add_dubai_features()

# Configuration trader
st.sidebar.header("⚙️ Configuration Trader")
tickers = st.sidebar.multiselect(
    "Actifs à analyser",
    ["BTC-USD", "XAU-USD", "ETH-USD"],
    default=["BTC-USD", "XAU-USD"]
)

# Bouton d'analyse - VERSION CORRIGÉE (graphiques garantis)
if st.button("🔍 Lancer l'Analyse IA", key="analyze_button", use_container_width=True):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, ticker in enumerate(tickers):
        status_text.text(f"Analyse en cours : {ticker} ({i+1}/{len(tickers)})")
        progress_bar.progress((i + 1) / len(tickers))
        
        st.subheader(f"📊 Analyse : {ticker}")
        
        # 🔑 CORRECTION CRUCIALE : UTILISER TOUJOURS LES DONNÉES SIMULÉES
        df = generate_mock_data(ticker, hours=100)
        
        if not df.empty and len(df) > 20:
            # Calculs techniques natifs
            df['RSI'] = calculate_rsi(df['Close'])
            df['EMA_Fast'] = df['Close'].ewm(span=12, adjust=False).mean()
            df['EMA_Slow'] = df['Close'].ewm(span=26, adjust=False).mean()
            
            # Valeurs actuelles (conversion en float explicite)
            last_close = float(df['Close'].iloc[-1])
            last_rsi = float(df['RSI'].iloc[-1])
            last_ema_fast = float(df['EMA_Fast'].iloc[-1])
            last_ema_slow = float(df['EMA_Slow'].iloc[-1])
            
            # Logique de signal REALISTE
            signal = "NEUTRE ⚪"
            signal_color = "gray"
            
            if last_rsi < 30:
                signal = "OPPORTUNITÉ ACHAT 🟢"
                signal_color = "green"
            elif last_rsi > 70:
                signal = "PRUDENCE 🔴"
                signal_color = "red"
            elif last_ema_fast > last_ema_slow:
                signal = "TENDANCE HAUSSE 📈"
                signal_color = "blue"
            
            # ✅ AFFICHAGE PROFESSIONNEL AVEC MÉTRIQUES
            col1, col2, col3 = st.columns(3)
            col1.metric("💰 Prix", f"${last_close:.2f}")
            col2.metric("📊 RSI", f"{last_rsi:.1f}")
            col3.markdown(f"### 🎯 **Signal** : <span style='color:{signal_color}'>{signal}</span>", unsafe_allow_html=True)
            
            # ✅ GRAPHIQUE GARANTI AVEC PLOTLY (version simplifiée mais fonctionnelle)
            fig = go.Figure()
            
            # Prix de clôture
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['Close'],
                mode='lines',
                name='Prix',
                line=dict(color='blue', width=2)
            ))
            
            # EMA rapide
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['EMA_Fast'],
                mode='lines',
                name='EMA 12',
                line=dict(color='red', width=1.5)
            ))
            
            # Configuration du graphique
            fig.update_layout(
                title=f'Évolution du prix : {ticker}',
                yaxis_title='Prix ($)',
                height=400,
                margin=dict(l=20, r=20, t=40, b=20),
                hovermode='x unified',
                template='plotly_white'
            )
            
            # ✅ AFFICHAGE DU GRAPHIQUE (toujours visible)
            st.plotly_chart(fig, use_container_width=True)
            
            # Mini-tableau des derniers prix
            with st.expander("📊 Dernières données (10 dernières heures)"):
                st.dataframe(
                    df[['Open', 'High', 'Low', 'Close', 'RSI']].tail(10).style.format({
                        'Open': '${:.2f}',
                        'High': '${:.2f}',
                        'Low': '${:.2f}',
                        'Close': '${:.2f}',
                        'RSI': '{:.1f}'
                    }),
                    use_container_width=True
                )
            
            st.markdown("---")
        else:
            st.error(f"Données insuffisantes pour {ticker} - Utilisation de données simulées uniquement")
    
    progress_bar.empty()
    status_text.empty()
    st.success("✅ Analyse terminée ! Graphiques générés avec données simulées réalistes.")

# Section "À propos"
st.sidebar.markdown("### 🔥 **Mon Histoire**")
st.sidebar.markdown("""
J'ai quitté l'université pour me consacrer entièrement à ma passion : 
l'IA appliquée aux marchés financiers. Je crois que les résultats 
comptent plus que les diplômes. Cet outil est ma preuve de concept.
""")

st.sidebar.markdown("### 💡 **Pourquoi cet outil ?**")
st.sidebar.markdown("""
• **Gain de temps** : Analyse automatique en 1 clic  
• **Focus Dubai** : Optimisé pour marchés actifs aux Émirats  
• **Zéro risque** : Outil éducatif, pas de signaux directs  
• **Transparence** : Code source disponible sur demande
""")

# Footer
st.markdown("---")
st.markdown("""
**AI Market Hunter - Dubai Edition** | Développé avec ❤️ pour les traders passionnés  
*Disclaimer : Outil éducatif uniquement. Pas conseil financier. Trading comporte des risques.*
""")
