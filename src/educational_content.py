"""
© 2025-2026 ELOADXFAMILY - Tous droits réservés
Module éducatif - Contenu basé sur les PDFs de 'special learn'
Fournit des insights, patterns candlestick, stratégies, et règles de gestion du risque

Ce module contient:
- 19 Patterns Candlestick avec descriptions complètes
- 4 Stratégies de Trading éprouvées avec étapes détaillées
- 5 Règles de Gestion du Risque inviolables
- 7 Principes de Psychologie du Trader
- Fonctions helper pour génération de news et validation

Tous les contenus sont basés sur les PDFs éducatifs fournis
et respectent les standards professionnels de trading.
"""

# ============================================================================
# 1. CHANDELIERS JAPONAIS - 19 Patterns Essentiels
# ============================================================================
CANDLESTICK_PATTERNS = {
    "Doji": {
        "description": "Ouverture = Fermeture, avec longues mèches",
        "signification": "Indécision du marché, possible retournement",
        "traduction_fr": "Doji",
        "identification": "Chercher une bougie avec un corps minuscule et des mèches hautes/basses similaires",
        "trading_tip": "Point d'entrée/sortie potentiel, à confirmer par volume et pattern précédent",
        "reliability": 65,
        "frequency": "Modérée",
        "best_timeframe": "4H-1D"
    },
    "Harami": {
        "description": "Petite bougie à l'intérieur de la grande précédente",
        "signification": "Inversion de tendance, perte d'élan",
        "traduction_fr": "Harami",
        "identification": "La petite bougie doit être complètement à l'intérieur du range de la bougie précédente",
        "trading_tip": "Utiliser en stratégie de retournement court terme après confirmation du marché",
        "reliability": 60,
        "frequency": "Régulière",
        "best_timeframe": "1H-4H"
    },
    "Engulfing_Haussier": {
        "description": "Grande bougie verte englobeant la bougie noire précédente",
        "signification": "Signal d'achat fort, retournement haussier",
        "traduction_fr": "Avalement Haussier",
        "identification": "Bougie verte plus grande qu'elle doit complètement contenir la bougie noire précédente",
        "trading_tip": "Entrée longue après confirmation volume, stop loss sous le low du pattern",
        "reliability": 85,
        "frequency": "Modérée",
        "best_timeframe": "1D-1W"
    },
    "Engulfing_Baissier": {
        "description": "Grande bougie noire englobeant la bougie verte précédente",
        "signification": "Signal de vente fort, retournement baissier",
        "traduction_fr": "Avalement Baissier",
        "identification": "Bougie noire plus grande doit complètement contenir la bougie verte précédente",
        "trading_tip": "Entrée courte après confirmation volume, stop loss au-dessus du high du pattern",
        "reliability": 85,
        "frequency": "Modérée",
        "best_timeframe": "1D-1W"
    },
    "Étoile_du_Matin": {
        "description": "3 bougies: baisse, doji/petite, hausse",
        "signification": "Retournement haussier très fiable",
        "traduction_fr": "Étoile du Matin",
        "identification": "Première bougie baissière forte, deuxième petite/doji en gap down, troisième haussière fermant dans le premier tiers de la première",
        "trading_tip": "Signal d'achat puissant après tendance baissière, confirmer avec volume",
        "reliability": 90,
        "frequency": "Modérée",
        "best_timeframe": "1D-1W"
    },
    "Étoile_du_Soir": {
        "description": "3 bougies: hausse, doji/petite, baisse",
        "signification": "Retournement baissier très fiable",
        "traduction_fr": "Étoile du Soir",
        "identification": "Première bougie haussière forte, deuxième petite/doji en gap up, troisième baissière fermant dans le premier tiers de la première",
        "trading_tip": "Signal de vente puissant après tendance haussière, confirmer avec volume",
        "reliability": 90,
        "frequency": "Modérée",
        "best_timeframe": "1D-1W"
    },
    "Marteau": {
        "description": "Corps petit, longue mèche basse, peu/pas de mèche haute",
        "signification": "Inversion baissière, support potentiel",
        "traduction_fr": "Marteau",
        "identification": "Bougie avec petit corps en haut, long shadow bas (au moins 2x le corps), peu de wick au-dessus",
        "trading_tip": "Signal d'achat en tendance baissière, placer stop loss sous le low",
        "reliability": 75,
        "frequency": "Régulière",
        "best_timeframe": "4H-1D"
    },
    "Pendu": {
        "description": "Idem marteau mais en tendance haussière",
        "signification": "Inversion haussière potentielle",
        "traduction_fr": "Pendu",
        "identification": "Même apparence que le marteau mais après tendance haussière",
        "trading_tip": "Signal de vente en tendance haussière, placer stop loss au-dessus du high",
        "reliability": 70,
        "frequency": "Régulière",
        "best_timeframe": "4H-1D"
    },
    "Trois_Soldats_Blancs": {
        "description": "3 bougies vertes consécutives avec corps croissants",
        "signification": "Continuation haussière forte",
        "traduction_fr": "Trois Soldats Blancs",
        "identification": "3 bougies vertes d'affilée, chacune plus grande que la précédente, ouvrant dans le corps de la précédente",
        "trading_tip": "Entrée longue en tendance haussière établie, confirmer avec support et volume",
        "reliability": 80,
        "frequency": "Modérée",
        "best_timeframe": "1D-1W"
    },
    "Trois_Corbeau_Noirs": {
        "description": "3 bougies noires consécutives avec corps décroissants",
        "signification": "Continuation baissière forte",
        "traduction_fr": "Trois Corbeaux Noirs",
        "identification": "3 bougies noires d'affilée, chacune plus grande que la précédente, ouvrant dans le corps de la précédente",
        "trading_tip": "Entrée courte en tendance baissière établie, confirmer avec résistance et volume",
        "reliability": 80,
        "frequency": "Modérée",
        "best_timeframe": "1D-1W"
    },
    "Piercing_Line": {
        "description": "Bougie baissière suivie d'une haussière qui perce 50%+ du précédent",
        "signification": "Retournement haussier potentiel",
        "traduction_fr": "Ligne Pierçante",
        "identification": "Première bougie noire forte, deuxième haussière ouvrant sous le low et fermant au-dessus du milieu de la première",
        "trading_tip": "Signal d'achat après baisse marquée, surveiller la confirmation du jour suivant",
        "reliability": 72,
        "frequency": "Modérée",
        "best_timeframe": "1D-1W"
    },
    "Nuage_Sombre": {
        "description": "Bougie haussière suivie d'une baissière qui perce 50%+ du précédent",
        "signification": "Retournement baissier potentiel",
        "traduction_fr": "Nuage Sombre",
        "identification": "Première bougie verte forte, deuxième baissière ouvrant au-dessus du high et fermant au-dessous du milieu de la première",
        "trading_tip": "Signal de vente après hausse marquée, surveiller la confirmation du jour suivant",
        "reliability": 72,
        "frequency": "Modérée",
        "best_timeframe": "1D-1W"
    },
    "In_Neck_Line": {
        "description": "Bougie baissière + petite bougie haussière fermant dans la baissière",
        "signification": "Consolidation de la baisse, potentiel inversion",
        "traduction_fr": "In Neck Line",
        "identification": "Bougie noire suivie d'une petite verte fermant juste au-dessous du close de la noire",
        "trading_tip": "Signal faible, attendre confirmation avant d'agir",
        "reliability": 55,
        "frequency": "Rare",
        "best_timeframe": "1D"
    },
    "On_Neck_Line": {
        "description": "Bougie baissière + petite bougie haussière fermant au même niveau",
        "signification": "Consolidation sans direction claire",
        "traduction_fr": "On Neck Line",
        "identification": "Bougie noire suivie d'une petite verte fermant au même niveau que le close de la noire",
        "trading_tip": "Attendre cassure nette pour signal directionnel clair",
        "reliability": 50,
        "frequency": "Rare",
        "best_timeframe": "1D"
    },
    "Thrusting_Line": {
        "description": "Bougie haussière + baissière fermant dans la haussière",
        "signification": "Élan baissier mais résistance haussière",
        "traduction_fr": "Thrusting Line",
        "identification": "Bougie verte suivie d'une noire fermant dans le body de la verte (haut que le low, bas que le close)",
        "trading_tip": "Potentiel rebond ou consolidation, surveiller le prochain mouvement",
        "reliability": 58,
        "frequency": "Rare",
        "best_timeframe": "4H-1D"
    },
    "High_Wave": {
        "description": "Bougies avec longues mèches hautes et basses, corps petit",
        "signification": "Indécision extrême du marché",
        "traduction_fr": "Vague Haute",
        "identification": "Bougie(s) avec shadows hautes et basses de même longueur, corps minuscule au centre",
        "trading_tip": "Attendre cassure claire, volatilité extrême à gérer avec prudence",
        "reliability": 55,
        "frequency": "Modérée",
        "best_timeframe": "1H-4H"
    },
    "Unique_3LineStrike": {
        "description": "3 bougies de même couleur + 4ème opposée englobeant les 3",
        "signification": "Retournement majeur de tendance",
        "traduction_fr": "Attaque de 3 Lignes",
        "identification": "3 bougies vertes/noires progressives puis 1 longue noire/verte englobeant complètement les 3",
        "trading_tip": "Signal très puissant de retournement, entrée immédiate après la 4ème bougie",
        "reliability": 88,
        "frequency": "Rare",
        "best_timeframe": "1D-1W"
    },
    "Harami_Cross": {
        "description": "Harami avec doji en 2ème position",
        "signification": "Indécision totale, probable inversion",
        "traduction_fr": "Harami en Croix",
        "identification": "Grande bougie suivie d'un doji (ouverture=fermeture) complètement à l'intérieur de la grande",
        "trading_tip": "Signal très fiable d'inversion, attendre confirmation jour suivant",
        "reliability": 82,
        "frequency": "Rare",
        "best_timeframe": "1D-1W"
    },
    "Continuation_Stick": {
        "description": "Bougies consécutives de même couleur sans engulfing, pile continue",
        "signification": "Continuation forte de la tendance actuelle",
        "traduction_fr": "Bâton de Continuation",
        "identification": "3+ bougies vertes/noires consécutives, chacune ayant une valeur confirmant la tendance",
        "trading_tip": "Confirmation de l'élan tendanciel établi, entrer en pyramide progressivement",
        "reliability": 78,
        "frequency": "Très Régulière",
        "best_timeframe": "1H-1D"
    }
}

# ============================================================================
# 2. STRATÉGIES DE TRADING - Basées sur les PDFs
# ============================================================================
TRADING_STRATEGIES = {
    "Support_Résistance": {
        "nom": "Support & Résistance",
        "description": "Identifier les niveaux clés où le prix rebondit",
        "étapes": [
            "1. Identifier 2-3 rebonds au même niveau",
            "2. Tracer une ligne horizontale (support ou résistance)",
            "3. Attendre cassure ou rebond confirmé",
            "4. Entrée au-dessus/dessous du niveau + stop loss"
        ],
        "avantages": ["Universelle", "Facile à identifier", "Haute probabilité"],
        "risques": ["Faux rebonds", "Cassure rapide", "Marché latéral"]
    },
    "Tendance_Breakout": {
        "nom": "Breakout de Tendance",
        "description": "Suivre la tendance après une consolidation",
        "étapes": [
            "1. Identifier triangle/rectangle en consolidation",
            "2. Attendre cassure avec volume élevé",
            "3. Entrée immédiate après cassure",
            "4. Stop loss sous/sur le support/résistance cassé"
        ],
        "avantages": ["Forte volatilité", "Tendance établie", "Ratio risque/bénéfice favorable"],
        "risques": ["Faux breakouts", "Whipsaw", "Glissement de prix"]
    },
    "Moyenne_Mobile": {
        "nom": "Moyenne Mobile (20/50/200)",
        "description": "Utiliser les moyennes comme dynamique de tendance",
        "étapes": [
            "1. Prix > MM20 > MM50 > MM200 = Tendance haussière",
            "2. Prix < MM20 < MM50 < MM200 = Tendance baissière",
            "3. Entrée au toucher de MM20/50",
            "4. Stop loss sous MM200"
        ],
        "avantages": ["Système simple", "Tendance claire", "Adaptatif"],
        "risques": ["Retard sur mouvements rapides", "Faux signaux latéraux"]
    },
    "RSI_Divergence": {
        "nom": "Divergence RSI (Suracheté/Survendu)",
        "description": "Chercher divergences entre prix et RSI",
        "étapes": [
            "1. RSI > 70 = Suracheté, RSI < 30 = Survendu",
            "2. Prix haut mais RSI baisse = Divergence baissière",
            "3. Prix bas mais RSI monte = Divergence haussière",
            "4. Entrée à la confirmation du retournement"
        ],
        "avantages": ["Anticipe les retournements", "Fiable", "Divergences fortes"],
        "risques": ["Peut rester suracheté longtemps", "Confirmation tardive"]
    }
}

# ============================================================================
# 3. GESTION DU RISQUE - Erreurs à Éviter (Protection du Capital)
# ============================================================================
RISK_MANAGEMENT_RULES = {
    "Position_Sizing": {
        "titre": "Dimensionnement de Position",
        "règle": "N'investir JAMAIS plus de 1-2% par position",
        "exemple": "Compte: 10,000$ → Max 100-200$ par trade",
        "erreur": "Trader gros après une bonne série",
        "solution": "Respecter la règle 1-2% quoi qu'il arrive"
    },
    "Stop_Loss_Obligatoire": {
        "titre": "Stop Loss Non-Négociable",
        "règle": "Chaque position a un stop loss AVANT l'entrée",
        "exemple": "Entrée: 100, Stop: 95 = Risque 5%",
        "erreur": "Espérer le rebond sans protection",
        "solution": "Placer stop loss immédiatement après entrée"
    },
    "Ratio_Risque_Gain": {
        "titre": "Ratio Risque/Bénéfice ≥ 1:2",
        "règle": "Gain minimum = 2x le risque",
        "exemple": "Risque: 100$, Gain minimum: 200$",
        "erreur": "Prendre petits gains et grands pertes",
        "solution": "Viser R:B de 1:3 ou 1:5"
    },
    "Max_Pertes_Quotidiennes": {
        "titre": "Limite Perte Quotidienne",
        "règle": "Si perte > 2% du compte, STOP la journée",
        "exemple": "Compte: 10,000$, Max perte jour: 200$",
        "erreur": "Vouloir récupérer les pertes rapidement",
        "solution": "Discipline émotionnelle, on recommence demain"
    },
    "Diversification": {
        "titre": "Ne Pas Mettre Tous les Œufs dans le Même Panier",
        "règle": "Max 10% par actif, varier les paires",
        "exemple": "Portfolio: 10 positions de 10% chacune",
        "erreur": "Trader une seule paire à cause d'une tendance",
        "solution": "Varier les secteurs et timeframes"
    }
}

# ============================================================================
# 4. ACTUALITÉS IMPACTANTES POUR TRADERS
# ============================================================================
IMPACTFUL_NEWS_TEMPLATES = [
    {
        "titre": "Données Économiques Clés",
        "contenu": [
            "📊 Emploi (NFP/Chômage) - Impact: TRÈS ÉLEVÉ",
            "📈 PIB et Inflation - Impact: TRÈS ÉLEVÉ",
            "💰 Décisions Banques Centrales - Impact: CRITIQUE",
            "🏪 Ventes au Détail/PMI - Impact: MOYEN-HAUT"
        ],
        "stratégie": "Attendre 15min post-annonce avant d'entrer. Volatilité extrême.",
        "nom": "Économique"
    },
    {
        "titre": "Opportunités de Trading Crypto",
        "contenu": [
            "🔴 Bitcoin: Analyse des niveaux clés",
            "🟢 Altcoins: Breakouts détectés",
            "📊 Volume: Signature des baleines détectées",
            "⚡ Moments optimaux: 00h UTC, 8h UTC, 15h UTC"
        ],
        "stratégie": "RSI + Moyennes mobiles. Ratio risque/bénéfice 1:3 min",
        "nom": "Crypto"
    },
    {
        "titre": "Retournements Identifiés",
        "contenu": [
            "🔄 Divergences RSI/Prix confirmées",
            "📍 Cassures de résistances historiques",
            "⭐ Patterns candlestick haussiers/baissiers",
            "💡 Niveaux de support testés"
        ],
        "stratégie": "Entrée à la confirmation du pattern + volume",
        "nom": "Patterns"
    },
    {
        "titre": "Gestion du Risque de la Journée",
        "contenu": [
            "⚠️ Volatilité prévue: HAUTE/MOYENNE/BASSE",
            "📍 Niveaux clés à ne pas franchir",
            "🛑 Stop Loss recommandé par actif",
            "✅ Ratio risque/bénéfice optimal du jour"
        ],
        "stratégie": "Adapter la taille des positions à la volatilité",
        "nom": "Risque"
    },
    {
        "titre": "Signaux Composites et Momentum",
        "contenu": [
            "🎯 RSI > 70 = Suracheté (Vendre)",
            "🎯 RSI < 30 = Survendu (Acheter)",
            "📊 MACD croisements confirmés",
            "📈 Bollinger Squeeze avant breakout majeur"
        ],
        "stratégie": "Attendre confirmation de 3 indicateurs minimum avant entrée",
        "nom": "Signaux"
    },
    {
        "titre": "Psychologie et Discipline du Trader",
        "contenu": [
            "🧠 Règle #1: Discipline > Prédiction",
            "🧠 Règle #2: Accepter les petites pertes",
            "🧠 Règle #3: Pas de revenge trading après une perte",
            "🧠 Règle #4: Journal CHAQUE trade"
        ],
        "stratégie": "Créer un plan, le suivre 100%, analyser les erreurs",
        "nom": "Psychologie"
    },
    {
        "titre": "Ses du Marché et Corrélations",
        "contenu": [
            "🔗 BTC/Alt corrélation forte détectée",
            "🌍 Paires forex en trending clairs",
            "💰 Or/Inflation: Relation confirmée",
            "📍 Secteurs/Indices: Tendances établies"
        ],
        "stratégie": "Chercher corrélations pour diversification sécurisée",
        "nom": "Correlations"
    }
]

# ============================================================================
# 5. PRINCIPES DE PSYCHOLOGIE DU TRADER
# ============================================================================
PSYCHOLOGY_RULES = {
    "Discipline": {
        "titre": "Discipline Absolue",
        "probleme": "Les traders inexpérimentés abandonent leur plan au premier doute",
        "solution": "La discipline > La prédiction. Respecter les règles à 100%.",
        "action": "Créer un plan écrit et le suivre sans exception"
    },
    "Gestion_Émotions": {
        "titre": "Gérer les Émotions",
        "probleme": "La peur et l'avidité contrôlent les décisions",
        "solution": "Peur et Avidité sont l'ennemi. Trader sans émotions.",
        "action": "Prendre des pauses après chaque trade gagnant"
    },
    "Accepter_Pertes": {
        "titre": "Accepter les Petites Pertes",
        "probleme": "Les traders refusent de perdre sur un trade et la perte grossit",
        "solution": "Les pertes sont normales. Max 2% par trade, c'est ok.",
        "action": "Accepter la perte et passer au trade suivant"
    },
    "Capitalisation": {
        "titre": "Croissance Stable du Capital",
        "probleme": "Vouloir devenir riche trop vite mène aux pertes",
        "solution": "Objectif: Doubler le compte chaque 3-6 mois via discipline.",
        "action": "Tracker la croissance mensuelle et ajuster la stratégie"
    },
    "Journal_Trading": {
        "titre": "Tenir un Journal de Trading",
        "probleme": "Sans tracking, on répète les mêmes erreurs",
        "solution": "Noter chaque trade: Entrée, sortie, raison. Analyser les erreurs.",
        "action": "Écrire un rapport après chaque session de trading"
    },
    "Pas_de_Revenge_Trading": {
        "titre": "Éviter le Revenge Trading",
        "probleme": "Après une grosse perte, on cherche à la récupérer immédiatement",
        "solution": "Après une grosse perte, prendre une pause. Pas de vengeance.",
        "action": "Si perte > 2% du compte, arrêter et analyser"
    },
    "Confiance_Système": {
        "titre": "Confiance dans le Système",
        "probleme": "Les modifications impulsives détruisent les stratégies rentables",
        "solution": "Faire confiance au système. Pas de modifications impulsives.",
        "action": "Tester le système 100 trades avant d'ajuster"
    }
}

# ============================================================================
# 6. FONCTION GÉNÉRATEUR DE NEWS IMPACTANTES
# ============================================================================
def generate_daily_trading_news(num_templates=None):
    """Génère des actualités trading vraiment utiles basées sur les principes éducatifs
    
    Args:
        num_templates: Nombre de templates à retourner (optionnel, par défaut sélection de 1)
    
    Returns:
        Un template ou liste de templates de news
    """
    import random
    from datetime import datetime
    
    heure_actuelle = datetime.now().hour
    jour_actuel = datetime.now().day
    
    if num_templates is None or num_templates == 1:
        # Sélectionner 1 template basé sur heure et jour
        seed = (jour_actuel * 24 + heure_actuelle) % len(IMPACTFUL_NEWS_TEMPLATES)
        template = IMPACTFUL_NEWS_TEMPLATES[seed]
        
        return {
            "titre": template["titre"],
            "contenus": template["contenu"],
            "stratégie": template["stratégie"],
            "timestamp": datetime.now().isoformat(),
            "source": "Dubai Trading Tools - Analyse Éducative"
        }
    else:
        # Retourner plusieurs templates
        num = min(num_templates, len(IMPACTFUL_NEWS_TEMPLATES))
        indices = random.sample(range(len(IMPACTFUL_NEWS_TEMPLATES)), num)
        return [
            {
                "titre": IMPACTFUL_NEWS_TEMPLATES[i]["titre"],
                "contenus": IMPACTFUL_NEWS_TEMPLATES[i]["contenu"],
                "stratégie": IMPACTFUL_NEWS_TEMPLATES[i]["stratégie"],
                "timestamp": datetime.now().isoformat(),
                "source": "Dubai Trading Tools - Analyse Éducative"
            }
            for i in indices
        ]

def get_pattern_educational_info(pattern_name):
    """Retourne info éducative sur un pattern candlestick"""
    return CANDLESTICK_PATTERNS.get(
        pattern_name,
        {"description": "Pattern non reconnu", "signal": "À analyser", "usage": "Confirmez avec d'autres indicateurs"}
    )

def get_strategy_guide(strategy_name):
    """Retourne guide complet d'une stratégie"""
    return TRADING_STRATEGIES.get(
        strategy_name,
        {"nom": "Stratégie inconnue", "description": "Guide non disponible"}
    )

def check_risk_rule_violation(position_risk_amount, account_balance, daily_loss=None):
    """Vérifie si une position viole les règles de risque
    
    Args:
        position_risk_amount: Montant à risquer dans la position
        account_balance: Solde du compte
        daily_loss: Pertes quotidiennes (optionnel)
    
    Returns:
        Bool: True si violation, False sinon
    """
    if account_balance <= 0:
        return True
    
    risk_pct = (position_risk_amount / account_balance) * 100
    
    # Vérifier dépassement de 2%
    if risk_pct > 2:
        return True
    
    # Vérifier si pertes quotidiennes dépassent 2%
    if daily_loss is not None and daily_loss > account_balance * 0.02:
        return True
    
    return False
