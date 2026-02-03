import streamlit as st
print('st.secrets keys:', list(getattr(st, 'secrets', {}).keys()))
print('st.secrets content:', dict(getattr(st, 'secrets', {})))
