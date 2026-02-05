#!/usr/bin/env python
"""Add professional emojis to patterns and strategies"""
import re

# Read the file
with open('src/educational_content.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Emoji mappings for patterns
pattern_emojis = {
    'Engulfing_Haussier': '📈',
    'Engulfing_Baissier': '📉',
    'Étoile_du_Matin': '🌅',
    'Étoile_du_Soir': '🌙',
    'Marteau': '🔨',
    'Pendu': '🎪',
    'Trois_Soldats_Blancs': '⚔️',
    'Trois_Corbeau_Noirs': '🐦',
    'Piercing_Line': '⚡',
    'Nuage_Sombre': '☁️',
    'In_Neck_Line': '🔗',
    'On_Neck_Line': '➖',
    'Thrusting_Line': '🎯',
    'High_Wave': '🌊',
    'Unique_3LineStrike': '💣',
    'Harami_Cross': '✝️',
    'Continuation_Stick': '📊',
}

# Strategy emojis
strategy_emojis = {
    'Support_Résistance': '📍',
    'Tendance_Breakout': '🚀',
    'Moyenne_Mobile': '📈',
    'RSI_Divergence': '⚖️',
}

# Add emojis to patterns
for pattern_name, emoji in pattern_emojis.items():
    pattern = rf'("{pattern_name}": \{{\n\s+)"description"'
    replacement = rf'\1"emoji": "{emoji}",\n        "description"'
    content = re.sub(pattern, replacement, content)

# Add emojis to strategies
for strat_name, emoji in strategy_emojis.items():
    pattern = rf'("{strat_name}": \{{\n\s+)"nom"'
    replacement = rf'\1"emoji": "{emoji}",\n        "nom"'
    content = re.sub(pattern, replacement, content)

# Write back
with open('src/educational_content.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Emojis added to all patterns and strategies")
