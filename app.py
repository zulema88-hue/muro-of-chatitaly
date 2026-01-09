import streamlit as st
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Il Muro di Chatitaly", layout="wide")

# CSS PER EFFETTO NEON E GRAFFITI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Frijole&display=swap');
    
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(#1a1a1a 1px, transparent 1px);
        background-size: 30px 30px;
    }

    .neon-title {
        font-family: 'Frijole', cursive;
        color: #fff;
        text-align: center;
        text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 20px #ff00ff, 0 0 30px #ff00ff, 0 0 40px #ff00ff;
        font-size: 50px;
        margin-bottom: 10px;
    }

    .graffiti-sticker {
        padding: 20px;
        margin: 15px;
        border-radius: 5px;
        display: inline-block;
        line-height: 1;
        transition: all 0.3s;
    }

    /* Effetto quando passi sopra con il mouse */
    .graffiti-sticker:hover {
        transform: scale(1.1) rotate(0deg) !important;
        z-index: 100;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INIZIALIZZAZIONE ---
if 'muro' not in st.session_state:
    st.session_state.muro = []

colors = ["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FF5E00"]
rotations = [-3, -2, -1, 1, 2, 3] # Gradi di rotazione casuale

# --- LOGICA ---
def spruzza():
    testo = st.session_state.input_testo
    if testo.strip():
        nuovo_post = {
            "testo": testo.upper(),
            "colore": random.choice(colors),
            "rotazione": random.choice(rotations),
            "font_size": random.randint(28, 45),
            "ora": datetime.now().strftime("%H:%M")
        }
        st.session_state.muro.append(nuovo_post)
        st.session_state.input_testo = ""

# --- INTERFACCIA ---
st.markdown("<h1 class='neon-title'>CHATITALY WALL</h1>", unsafe_allow_html=True)

# Campo input al centro
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.text_input("SCRIVI E PREMI INVIO PER SPRUZZARE 🎨", key="input_testo", on_change=spruzza)

st.markdown("<br>", unsafe_allow_html=True)

# --- IL MURO ---
# Creiamo un contenitore flessibile per i graffiti
cols = st.columns(3)

for i, m in enumerate(reversed(st.session_state.muro)):
    with cols[i % 3]:
        st.markdown(f"""
            <div class="graffiti-sticker" style="
                transform: rotate({m['rotazione']}deg);
                color: {m['colore']};
                text-shadow: 2px 2px 0px #000, 0 0 15px {m['colore']};
                font-family: 'Permanent Marker', cursive;
                font-size: {m['font_size']}px;
            ">
                {m['testo']}
                <div style="font-size: 10px; color: #444; font-family: sans-serif; text-shadow: none;">
                    BY ANONYMOUS @ {m['ora']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- ADMIN ---
with st.sidebar:
    st.title("🛠️ Admin")
    pw = st.text_input("Password", type="password")
    if pw == "chatitaly123":
        if st.button("PULISCI MURO"):
            st.session_state.muro = []
            st.rerun()
