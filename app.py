import streamlit as st
import random
from datetime import datetime

# --- CONFIGURAZIONE GRAFICA ---
st.set_page_config(page_title="Il Muro di Chatitaly", layout="wide")

# Carichiamo i font stile graffiti da Google Fonts
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Sedgwick+Ave&family=Bangers&display=swap');
    
    .stApp {
        background-color: #0e1117;
        background-image: radial-gradient(#2d2d2d 1px, transparent 1px);
        background-size: 20px 20px; /* Effetto griglia scura */
    }
    
    .graffiti-card {
        padding: 15px;
        border-radius: 15px;
        margin: 10px;
        border: 1px solid rgba(255,255,255,0.1);
        background: rgba(255,255,255,0.05);
        transition: transform 0.2s;
    }
    
    .graffiti-card:hover {
        transform: scale(1.05) rotate(-1deg);
    }
    </style>
    """, unsafe_allow_html=True)

# --- GESTIONE DATI (Provvisoria in Session State) ---
if 'muro' not in st.session_state:
    st.session_state.muro = []

# Font e colori vivaci per l'effetto spray
fonts = ["'Permanent Marker', cursive", "'Rock Salt', cursive", "'Sedgwick Ave', cursive", "'Bangers', system-ui"]
colors = ["#FF00FF", "#00FFFF", "#FFD700", "#ADFF2F", "#FF4500", "#FF007F", "#00FFAB"]

# --- LOGICA ---
