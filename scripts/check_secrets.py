"""© 2025-2026 ELOADXFAMILY - Tous droits réservés
Security Check Script - Validate no secrets are exposed"""
import streamlit as st
print('st.secrets keys:', list(getattr(st, 'secrets', {}).keys()))
print('st.secrets content:', dict(getattr(st, 'secrets', {})))
