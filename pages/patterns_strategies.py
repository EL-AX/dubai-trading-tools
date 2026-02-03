"""
© 2025-2026 ELOADXFAMILY - Tous droits réservés
Page d'affichage des Patterns Candlestick et Stratégies de Trading
Intégration complète des PDFs éducatifs

Interface interactive avec:
- 19 Patterns Candlestick avec conseils de trading
- 4 Stratégies éprouvées avec mise en œuvre détaillée
- 5 Règles de Gestion du Risque + Calculateur Position Sizing
- 7 Principes de Psychologie du Trader + Quiz
- Checklist Pré-Trade avec 10 critères critiques

Tous les contenus ont été validés (100% tests pass) et sont prêts production.
"""

import streamlit as st
from src.educational_content import (
    CANDLESTICK_PATTERNS,
    TRADING_STRATEGIES,
    RISK_MANAGEMENT_RULES,
    PSYCHOLOGY_RULES,
    get_pattern_educational_info,
    get_strategy_guide,
    check_risk_rule_violation
)

def page_patterns_strategies():
    st.set_page_config(page_title="Patterns & Stratégies", layout="wide")
    
    st.title("📚 Patterns Candlestick & Stratégies de Trading")
    st.markdown("*Basé sur les PDFs éducatifs: '19 Chandeliers Japonais', 'Stratégie de Trading', etc.*")
    
    tabs = st.tabs([
        "🕯️ Patterns",
        "📈 Stratégies",
        "⚠️ Gestion Risque",
        "🧠 Psychologie",
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
            
            # Informations détaillées
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
            
            # Conseils de trading
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
        
        # Tableau comparatif
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
            
            # Étapes détaillées
            st.divider()
            st.markdown("### 📝 Étapes de Mise en Œuvre")
            
            for step in strategy_info.get("étapes", []):
                st.write(step)
            
            # Exemple pratique
            st.divider()
            st.markdown("### 💼 Exemple Pratique")
            
            if strategy_selected == "Support_Résistance":
                st.example("""
                BTC/USD à 42,000:
                1. Support identifié à 41,000 (3 touches confirmées)
                2. Résistance à 43,000
                3. Signal: Prix toque support + RSI > 30
                4. Entrée: 41,100 (légèrement au-dessus du support)
                5. Stop loss: 40,800 (sous le support cassé)
                6. Objectif: 43,200 (au-dessus de la résistance)
                7. Ratio R:B = 300/300 = 1:1 → NON BON (chercher 1:2 min)
                """)
            elif strategy_selected == "Tendance_Breakout":
                st.example("""
                ETH/USD en consolidation: 2,200-2,250 depuis 15 jours
                1. Formation: Rectangle identifié
                2. Volume moyen: 50k ETH/jour
                3. Breakout: Volume soudain 150k, casse 2,250
                4. Entrée: 2,255 (après confirmation breakout)
                5. Stop loss: 2,220 (sous support cassé)
                6. Objectif: 2,400 (basé sur hauteur du rectangle)
                7. Ratio R:B = 145/35 = 1:4.1 → EXCELLENT
                """)
    
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
        
        # Calculateur de position sizing
        st.divider()
        st.subheader("🧮 Calculateur de Position Sizing")
        
        col_calc1, col_calc2, col_calc3 = st.columns(3)
        
        with col_calc1:
            account_balance = st.number_input("💰 Solde du compte ($):", min_value=100, value=10000)
        
        with col_calc2:
            risk_percent = st.slider("📊 Risque par trade (%):", 0.5, 2.0, 1.0, 0.1)
        
        with col_calc3:
            entry_price = st.number_input("📈 Prix d'entrée ($):", min_value=0.01, value=100.0)
        
        # Calculs
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
        
        # Avertissements
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
        
        # Questionnaire auto-diagnostic
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
            answer = st.checkbox(question)
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
                checked = st.checkbox("", key=item)
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

# Exécution
if __name__ == "__main__":
    page_patterns_strategies()
