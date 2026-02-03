TOOLTIPS = {
    "RSI": {
        "title": "Relative Strength Index",
        "description": "Mesure la force d'une tendance",
        "content": "RSI entre 0 et 100. Au-dessus de 70 = suracheté. Au-dessous de 30 = survendu.",
        "formula": "RSI = 100 - (100 / (1 + RS))"
    },
    "MACD": {
        "title": "Moving Average Convergence Divergence",
        "description": "Suit la tendance et le momentum",
        "content": "Combine deux moyennes mobiles exponentielles. Croisements = signaux d'achat/vente.",
        "formula": "MACD = EMA(12) - EMA(26)"
    },
    "Bollinger": {
        "title": "Bandes de Bollinger",
        "description": "Mesure la volatilité et les niveaux extrêmes",
        "content": "Trois lignes autour du prix. Prix aux extrêmes = signaux potentiels.",
        "formula": "Bande = SMA +/- (2 * Ecart-type)"
    },
    "Trend": {
        "title": "Tendance",
        "description": "Direction generale du marche",
        "content": "Haussier (vers le haut), baissier (vers le bas), ou lateral (neutre).",
        "formula": "Pente sur periode definie"
    },
    "Support": {
        "title": "Support",
        "description": "Niveau ou le prix a du mal a descendre",
        "content": "Les acheteurs interviennent. Cible pour acheter.",
        "formula": "Support = Plus bas recent"
    },
    "Resistance": {
        "title": "Resistance",
        "description": "Niveau ou le prix a du mal a monter",
        "content": "Les vendeurs interviennent. Cible pour vendre.",
        "formula": "Resistance = Plus haut recent"
    },
    "Volatilite": {
        "title": "Volatilite",
        "description": "Amplitude des mouvements de prix",
        "content": "Haute = mouvements rapides et importants. Basse = mouvements lents.",
        "formula": "Volatilite = Ecart-type des rendements"
    },
    "Momentum": {
        "title": "Momentum",
        "description": "Force et vitesse du mouvement de prix",
        "content": "Momentum positif = prix monte. Momentum negatif = prix baisse.",
        "formula": "Momentum = Prix actuel - Prix passé"
    },
    "Signal": {
        "title": "Signal de Trading",
        "description": "Recommandation d'action (Achat/Vente)",
        "content": "Combine tous les indicateurs. Fort signal = plus de confiance.",
        "formula": "Signal = Moyenne des scores des indicateurs"
    },
    "Ratio_Risque_Rendement": {
        "title": "Ratio Risque/Rendement",
        "description": "Rapport entre perte potentielle et gain potentiel",
        "content": "Bon ratio = rendement > risque. Exemple: 1:2 = bon.",
        "formula": "Ratio = (Resistance - Prix) / (Prix - Support)"
    }
}

def get_tooltip(key):
    return TOOLTIPS.get(key, {})

def format_tooltip_markdown(key):
    tooltip = get_tooltip(key)
    if not tooltip:
        return "Information non disponible"
    
    md = f"### {tooltip['title']}\n\n"
    md += f"**Description:** {tooltip['description']}\n\n"
    md += f"{tooltip['content']}\n\n"
    md += f"**Formule:** `{tooltip['formula']}`"
    return md

def explain_term(term):
    explanations = {
        "overbought": "Prix trop haut = vendre potentiellement",
        "oversold": "Prix trop bas = acheter potentiellement",
        "bullish": "Tendance haussiere = prix monte",
        "bearish": "Tendance baissiere = prix baisse",
        "divergence": "Indicateurs ne s'accordent pas = attention",
        "convergence": "Indicateurs s'accordent = fort signal",
        "crossover": "Une ligne en croise une autre = signal potentiel"
    }
    return explanations.get(term.lower(), "Terme non reconnu")
