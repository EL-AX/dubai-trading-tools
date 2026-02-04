"""© 2025-2026 ELOADXFAMILY - Tous droits réservés
Tooltips - Contextual in-app help and guidance"""

TOOLTIPS = {
    "RSI": {
        "title": "RSI - Relative Strength Index",
        "description": "Mesure du momentum et de la force relative",
        "content": """RSI scale: 0-100
- **>70**: Suracheté (prix trop haut, risque de baisse)
- **<30**: Survendu (prix trop bas, risque de hausse)
- **50**: Point neutre
- Période: 14 bougies par défaut

**Utilisation**: Attendez RSI < 30 + confirmé par autre indicateur pour signal d'achat fort.""",
        "formula": "RSI = 100 - (100 / (1 + RS))",
        "educatif": "Source: Cours de Trading PDF - Les oscillateurs"
    },
    "MACD": {
        "title": "MACD - Moving Average Convergence Divergence",
        "description": "Détecteur de tendance et momentum",
        "content": """Combine deux moyennes mobiles exponentielles (12 et 26 jours)
- **Croisement haussier**: MACD croise au-dessus de la signal line = ACHAT
- **Croisement baissier**: MACD croise au-dessous = VENTE
- **Histogram**: Représente la différence MACD - Signal

**Signal fort**: MACD + RSI + Bollinger s'accordent.""",
        "formula": "MACD = EMA(12) - EMA(26), Signal = EMA(9) du MACD",
        "educatif": "Source: 'Stratégie De Trading' PDF - Indicateurs composites"
    },
    "Bollinger": {
        "title": "Bandes de Bollinger",
        "description": "Volatilité et zones d'extrême",
        "content": """Trois lignes de Bollinger autour du prix:
- **Bande supérieure**: +2 écarts-type (résistance potentielle)
- **Bande médiane**: Moyenne mobile 20 jours
- **Bande inférieure**: -2 écarts-type (support potentiel)

**Signal d'achat**: Prix touchant bande basse + RSI > 30
**Signal de vente**: Prix touchant bande haute + RSI > 70
**Volatilité**: Largeur des bandes = volatilité du marché.""",
        "formula": "Bande = SMA(20) ± (2 × Écart-type(20))",
        "educatif": "Source: 'Protection de son capital' PDF - Volatilité et gestion"
    },
    "Tendance": {
        "title": "Tendance du Marché",
        "description": "Direction générale du prix",
        "content": """**Tendance haussière**: Chaque high > previous high & chaque low > previous low
- Prix > MA20 > MA50 > MA200 = confirmation forte
- Achetez aux pullbacks sur les supports

**Tendance baissière**: Chaque high < previous high & chaque low < previous low
- Prix < MA20 < MA50 < MA200 = confirmation forte
- Vendez aux rebonds sur les résistances

**Tendance latérale**: Prix oscille entre support/résistance
- Meilleur pour le range trading, pas les tendances""",
        "formula": "Tendance = Analyse des plus hauts/bas successifs",
        "educatif": "Source: 'Cours de trading' - Analyse des tendances"
    },
    "Support": {
        "title": "Niveau de Support",
        "description": "Zone où le prix rebondit à la hausse",
        "content": """Support = Niveau où les acheteurs interviennent
- Identifiez: 2-3 touches au même niveau = support confirmé
- **Cible d'achat**: À proximité du support confirmé
- **Stop loss**: Sous le support (nouveau plus bas = break)

**Stratégie**: Achetez au toucher du support avec ratio 1:3 min""",
        "formula": "Support = Plus bas récent confirmé 2-3 fois",
        "educatif": "Source: 'Stratégie Trading' PDF - Support & Résistance"
    },
    "Resistance": {
        "title": "Niveau de Résistance",
        "description": "Zone où le prix peine à monter",
        "content": """Résistance = Niveau où les vendeurs interviennent
- Identifiez: 2-3 touches au même niveau = résistance confirmée
- **Cible de vente**: À proximité de la résistance confirmée
- **Stop loss**: Au-dessus de la résistance (nouveau plus haut = break)

**Stratégie**: Vendez au toucher de la résistance avec ratio 1:3 min""",
        "formula": "Résistance = Plus haut récent confirmé 2-3 fois",
        "educatif": "Source: 'Stratégie Trading' PDF - Support & Résistance"
    },
    "Volatilite": {
        "title": "Volatilité du Marché",
        "description": "Amplitude et vitesse des mouvements",
        "content": """**Haute volatilité**: Bandes Bollinger larges, mouvements rapides
- Risques: Glissements de prix, breakouts faux
- Avantages: Meilleurs ratios R:B, plus d'opportunités
- **Gestion**: Augmentez taille position légèrement (25-50% max)

**Basse volatilité**: Bandes étroites, mouvements lents
- Risques: Faux signaux, range trading frustrant
- Avantages: Plus prévisible
- **Gestion**: Réduisez taille position à 0.5-1% du compte""",
        "formula": "Volatilité = Écart-type des rendements (périodisé)",
        "educatif": "Source: 'Protection du capital' PDF - Gestion adaptative"
    },
    "Momentum": {
        "title": "Momentum du Prix",
        "description": "Force et vitesse du mouvement",
        "content": """Momentum = Énergie du marché
- **Momentum positif fort**: Prix monte rapidement = ACHAT possible
- **Momentum négatif fort**: Prix baisse rapidement = VENTE possible
- **Momentum faible**: Prix stagne = attendre ou range trading

**Signal**: Divergence MACD/Prix = momentum faiblissant""",
        "formula": "Momentum = Prix(t) - Prix(t-N)",
        "educatif": "Source: 'Cours de Trading' PDF - Indicateurs de momentum"
    },
    "Signal": {
        "title": "Signal de Trading Composite",
        "description": "Recommandation consolidée d'action",
        "content": """Signal combine 4 indicateurs pour fiabilité:
- **STRONG_BUY (80-100)**: 3-4 indicateurs haussiers = entrez
- **BUY (60-80)**: 2-3 indicateurs haussiers = considérez
- **NEUTRAL (40-60)**: Pas de consensus = attendez
- **SELL (20-40)**: 2-3 indicateurs baissiers = sortez
- **STRONG_SELL (0-20)**: 3-4 indicateurs baissiers = liquidez

**Fabilité**: STRONG_BUY/SELL = 80%+ fiabilité
**Meilleur timing**: À la confluence de support/résistance""",
        "formula": "Signal = (RSI_score + MACD_score + Bollinger_score + Trend_score) / 4",
        "educatif": "Source: Dubai Trading Tools - Analyse composite"
    },
    "Ratio_Risque_Rendement": {
        "title": "Ratio Risque/Bénéfice (R:B)",
        "description": "Rapport profit potentiel / risque potentiel",
        "content": """R:B = Bénéfice / Risque

**Recommandations**:
- **Minimum**: 1:2 (risquez 100 pour gagner 200)
- **Bon**: 1:3 (risquez 100 pour gagner 300)
- **Excellent**: 1:5 (risquez 100 pour gagner 500)

**Calcul**: 
- Risque = Prix entrée - Stop loss
- Bénéfice = Objectif - Prix entrée
- R:B = Bénéfice / Risque

**Gestion**: Cherchez TOUJOURS R:B ≥ 1:2 avant d'entrer""",
        "formula": "Ratio R:B = (Cible - Entrée) / (Entrée - Stop Loss)",
        "educatif": "Source: 'Protection de son capital' PDF - Gestion du risque"
    },
    "Divergence": {
        "title": "Divergence (Signal Majeur)",
        "description": "Quand prix et indicateurs ne s'accordent pas",
        "content": """**Divergence baissière** (Sommet):
- Prix fait nouveau HIGH mais RSI baisse = FAIBLESSE
- Signal VENTE fort = retournement proche
- Meilleur: Sur les 3ème-4ème tentatives haussières

**Divergence haussière** (Creux):
- Prix fait nouveau LOW mais RSI monte = FORCE cachée
- Signal ACHAT fort = retournement proche
- Meilleur: Après plusieurs baisses

**Fiabilité**: Divergences = 70-80% d'exactitude""",
        "formula": "Divergence = Tendance prix ≠ Tendance indicateur",
        "educatif": "Source: '19 Chandeliers' + 'Cours Trading' PDFs"
    },
    "Chandelier_Pattern": {
        "title": "Patterns Candlestick (19 Essentiels)",
        "description": "Formations de bougies qui prédisent mouvements",
        "content": """**Tops 3 patterns d'inversion**:
1. **Engulfing**: Grande bougie engloberait petite précédente
   - Haussier = ACHAT (baisse → hausse)
   - Baissier = VENTE (hausse → baisse)
   - Fiabilité: ~75%

2. **Étoile du Matin/Soir**: 3 bougies spécifiques
   - Matin = ACHAT au-dessus du 3ème corps
   - Soir = VENTE au-dessous du 3ème corps
   - Fiabilité: ~80%

3. **Marteau/Pendu**: Petite corps + longue mèche
   - Marteau = ACHAT en baisse
   - Pendu = VENTE en hausse
   - Fiabilité: ~65%

**Meilleure pratique**: Confirmez avec indicateurs + volume élevé""",
        "formula": "Pattern = Formation spécifique de 1-3 bougies",
        "educatif": "Source: '19 CHANDELIERS JAPONAIS A CONNAITRE.pdf'"
    },
    "Vivre_du_Trading": {
        "title": "Vivre du Trading (Principes Fondamentaux)",
        "description": "Comment être profitable sur le long terme",
        "content": """**5 piliers pour trader professionnellement**:

1. **Discipline absolue**: 100% respect des règles, toujours
2. **Gestion du risque**: Max 1-2% par trade, 2% perte/jour = STOP
3. **Journal de trading**: Noter CHAQUE trade pour analyser
4. **Psychologie**: Éliminer peur et avidité
5. **Capitalisation**: Doubler compte tous les 3-6 mois = réaliste

**Erreurs fatales** (à ÉVITER absolument):
- Revenge trading après grosse perte
- Position trop grande (>2%)
- Pas de stop loss
- Trader sans plan
- Suivre les émotions au lieu du système""",
        "formula": "Profit long-terme = Discipline × Gestion risque × Psychologie",
        "educatif": "Source: '7. Vivre du trading.pdf' - Principes professionnels"
    }
}

def get_tooltip(key):
    return TOOLTIPS.get(key, {})

def format_tooltip_markdown(key):
    tooltip = get_tooltip(key)
    if not tooltip:
        return "ℹ️ Information non disponible"
    
    md = f"### {tooltip['title']}\n\n"
    md += f"**Description:** {tooltip['description']}\n\n"
    md += f"{tooltip['content']}\n\n"
    md += f"**Formule:** `{tooltip['formula']}`\n\n"
    md += f"📚 {tooltip.get('educatif', 'Source interne')}"
    return md

def explain_term(term):
    explanations = {
        "overbought": "Suracheté: RSI > 70 = Prix trop haut, risque de correction",
        "oversold": "Survendu: RSI < 30 = Prix trop bas, risque de rebond",
        "bullish": "Haussier: Tendance à la hausse = opportunité d'achat",
        "bearish": "Baissier: Tendance à la baisse = opportunité de vente",
        "divergence": "Divergence: Prix ≠ Indicateur = Signal majeur d'inversion",
        "convergence": "Convergence: Prix = Indicateur = Signal fort confirmé",
        "crossover": "Croisement: Une ligne croise une autre = Signal potentiel",
        "support": "Support: Niveau où prix rebondit à la hausse",
        "resistance": "Résistance: Niveau où prix peine à monter",
        "breakout": "Breakout: Prix casse support/résistance avec volume",
        "pullback": "Pullback: Prix revient à un niveau de support en tendance haussière",
        "trailing_stop": "Stop suiveur: Stop qui monte avec le prix, protection des gains"
    }
    return explanations.get(term.lower(), "Terme non reconnu - consultez l'aide")

