"""
Analyseur de Sentiment Réel pour les Actualités Crypto
Basé sur l'analyse de mots-clés positifs/négatifs dans les titres et descriptions
"""

import re

# Dictionnaire de mots-clés positifs
BULLISH_KEYWORDS = [
    # Hausse
    'surge', 'rally', 'jump', 'soars', 'boom', 'skyrocket', 'explode', 'climb',
    'gain', 'rise', 'rises', 'up', 'bullish', 'bull', 'pump', 'rally',
    # Adoption/positif
    'adoption', 'approve', 'approved', 'launch', 'introduce', 'partnership',
    'partnership', 'collaborate', 'collaboration', 'integrate', 'integration',
    'upgrade', 'improvement', 'improve', 'achieve', 'achieved',
    'milestone', 'record', 'high', 'breakthrough', 'success', 'successful',
    'strong', 'positive', 'growth', 'recover', 'recovery', 'accumulate', 'accumulation',
    # Optimisme
    'optimistic', 'optimism', 'buy', 'opportunity', 'profitable', 'profit',
    'profitable', 'win', 'beat', 'outperform', 'perform', 'performance',
    # Régulation positive
    'approval', 'approved', 'regulation', 'etf', 'institutional', 'institution',
    'corporate', 'adoption', 'bank', 'banks', 'major', 'integration',
    # Nouvelles positives
    'announcement', 'announce', 'announce', 'revealed', 'reveal', 'integration',
    'listed', 'listing', 'add', 'added', 'integr', 'expand', 'expansion',
    # En français
    'hausse', 'explosion', 'explose', 'grimpe', 'monte', 'haussier', 'positif', 'positive',
    'partenariat', 'adoption', 'approbation', 'approuvé', 'record', 'intégration',
    'succès', 'croissance', 'croît', 'opportunité', 'accélération', 'accélère',
    'nouveau', 'sommet', 'gains'
]

# Dictionnaire de mots-clés négatifs
BEARISH_KEYWORDS = [
    # Baisse
    'crash', 'plunge', 'fall', 'falls', 'down', 'drop', 'decline', 'tumble',
    'slip', 'slump', 'collapse', 'lose', 'losing', 'bleed', 'bearish', 'bear',
    'downturn', 'selloff', 'sell', 'selling', 'dump', 'dumping', 'cascade',
    # Problèmes
    'hack', 'hacked', 'breach', 'security', 'exploit', 'exploited', 'stolen',
    'fraud', 'scam', 'bankruptcy', 'bankrupt', 'fail', 'fails', 'failure',
    'error', 'bug', 'vulnerability', 'vulnerable', 'problem', 'problem',
    # Régulation négative
    'ban', 'banned', 'illegal', 'illegality', 'regulation', 'regulate', 'crackdown',
    'sued', 'lawsuit', 'prosecution', 'charge', 'investigation', 'investigate',
    'probe', 'inquiry', 'indicted',
    # Pessimisme
    'pessimism', 'pessimistic', 'negative', 'warning', 'warn', 'warning',
    'risk', 'risky', 'danger', 'dangerous', 'threat', 'threaten', 'concern',
    'worry', 'uncertain', 'uncertainty', 'fear', 'fearing', 'fearful',
    # Mauvaises nouvelles
    'layoff', 'shutdown', 'shut', 'stop', 'stopping', 'exit', 'exiting',
    'bankrupt', 'delisting', 'delist', 'removal', 'remove', 'halt',
    # En français
    'chute', 'chuter', 'chutent', 'effondrement', 'effondre', 'baisse', 'baissier',
    'négatif', 'negative', 'problème', 'piratage', 'piratée', 'fraude', 'escroquerie',
    'faillite', 'faillite', 'ban', 'interdiction', 'régulation', 'investigation',
    'poursuites', 'arrêt', 'fermeture', 'risque', 'danger', 'préoccupation',
    'peur', 'inquiétude', 'inquiet', 'dégât', 'chute drastique', 'crash'
]

def analyze_sentiment(text):
    """
    Analyser le sentiment d'un texte
    Retourne: 'bullish', 'bearish', ou 'neutral'
    """
    if not text:
        return 'neutral'
    
    text_lower = text.lower()
    
    # Compter les occurrences
    bullish_count = 0
    bearish_count = 0
    
    for keyword in BULLISH_KEYWORDS:
        # Simple substring check instead of regex for reliability
        bullish_count += text_lower.count(keyword)
    
    for keyword in BEARISH_KEYWORDS:
        bearish_count += text_lower.count(keyword)
    
    # Déterminer le sentiment
    if bullish_count > bearish_count + 1:
        return 'bullish'
    elif bearish_count > bullish_count + 1:
        return 'bearish'
    else:
        return 'neutral'

def analyze_news_sentiment(news_item):
    """
    Analyser le sentiment d'un article de news complet
    Combine titre + description/résumé
    """
    title = news_item.get('titre', '') or news_item.get('title', '')
    description = news_item.get('resume', '') or news_item.get('description', '') or news_item.get('summary', '')
    
    # Le titre est plus important (poids 2x)
    text = f"{title} {title} {description}"
    
    return analyze_sentiment(text)

def get_impact_score(news_item):
    """
    Retourner un score d'impact (1-10) pour une actualité
    Basé sur le nombre de mots-clés et leur force
    """
    title = news_item.get('titre', '') or news_item.get('title', '')
    description = news_item.get('resume', '') or news_item.get('description', '') or news_item.get('summary', '')
    
    text_lower = (f"{title} {description}").lower()
    
    # Mots-clés avec impact fort
    high_impact_keywords = [
        'crash', 'exploit', 'hack', 'bankruptcy', 'ban', 'regulations',
        'record', 'ath', 'breakthrough', 'milestone', 'partnership',
        'approval', 'etf', 'institutional', 'surge', 'collapse',
        'chute', 'explosion', 'piratage', 'faillite', 'partenariat'
    ]
    
    impact = 3  # Score de base
    
    for keyword in high_impact_keywords:
        pattern = r'\b' + re.escape(keyword) + r'\b'
        count = len(re.findall(pattern, text_lower))
        impact += count * 2
    
    return min(impact, 10)  # Max 10
