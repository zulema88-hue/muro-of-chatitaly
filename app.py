import streamlit as st
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Il Muro di Chatitaly", layout="wide")

# CSS PER MURO DI MATTONI E EFFETTO TAGS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Frijole&family=Nosifer&family=Rubik+Glitch&family=Special+Elite&display=swap');
    
    .stApp {
        background-color: #0a0a0a;
        background-image: 
            linear-gradient(335deg, #050505 23px, transparent 23px),
            linear-gradient(155deg, #080808 23px, transparent 23px),
            linear-gradient(335deg, #050505 23px, transparent 23px),
            linear-gradient(155deg, #080808 23px, transparent 23px);
        background-size: 58px 58px;
    }

    .neon-title {
        font-family: 'Frijole', cursive;
        color: #fff;
        text-align: center;
        text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
        font-size: clamp(25px, 6vw, 60px);
        padding: 10px;
    }

    /* Contenitore flessibile per i graffiti */
    .wall-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        gap: 10px;
        padding: 20px;
    }

    .graffiti-tag {
        display: inline-block;
        padding: 5px 15px;
        line-height: 1;
        transition: all 0.3s;
        filter: drop-shadow(3px 3px 2px #000);
        cursor: default;
    }

    .graffiti-tag:hover {
        transform: scale(1.3) rotate(0deg) !important;
        z-index: 999;
        filter: drop-shadow(0 0 10px white);
    }
    </style>
    """, unsafe_allow_html=True)

# --- INIZIALIZZAZIONE ---
if 'muro' not in st.session_state:
    st.session_state.muro = []

font_styles = ["'Permanent Marker'", "'Nosifer'", "'Rubik Glitch'", "'Bangers'", "'Special Elite'"]
colors = ["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FF5E00", "#FFFFFF", "#CCFF00", "#FF007F", "#008CF0"]

# --- LOGICA ---
def spruzza():
    testo = st.session_state.input_testo
    nick = st.session_state.input_nick
    if testo.strip():
        nuovo_post = {
            "testo": testo.upper(),
            "autore": nick.upper() if nick.strip() else "ANONYMOUS",
            "colore": random.choice(colors),
            "font": random.choice(font_styles),
            "rotazione": random.randint(-20, 20),
            "font_size": random.randint(20, 55), # Dimensioni variabili per farne entrare tanti
            "ora": datetime.now().strftime("%H:%M")
        }
        st.session_state.muro.append(nuovo_post)
        st.session_state.input_testo = ""
        st.session_state.input_nick = ""

# --- INTERFACCIA ---
st.markdown("<h1 class='neon-title'>CHATITALY WALL</h1>", unsafe_allow_html=True)

# Box di input compatto
with st.container():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        col_n, col_t = st.columns([1, 2])
        with col_n:
            st.text_input("NICKNAME", key="input_nick", placeholder="Anonimo")
        with col_t:
            st.text_input("SCRIVI IL TUO PENSIERO", key="input_testo", on_change=spruzza, placeholder="Premi INVIO per pubblicare")

st.markdown("<br>", unsafe_allow_html=True)

# --- IL MURO (LAYOUT DINAMICO) ---
# Usiamo un unico grande blocco HTML per far fluire i graffiti
tags_html = "<div class='wall-container'>"

for m in reversed(st.session_state.muro):
    tags_html += f"""
        <div class="graffiti-tag" style="
            transform: rotate({m['rotazione']}deg);
            color: {m['colore']};
            font-family: {m['font']}, cursive;
            font-size: {m['font_size']}px;
            text-shadow: 2px 2px 4px #000, 0 0 8px {m['colore']}88;
        ">
            {m['testo']}
            <div style="font-size: 9px; color: rgba(255,255,255,0.3); font-family: sans-serif; text-shadow: none;">
                BY {m['autore']} @ {m['ora']}
            </div>
        </div>
    """

tags_html += "</div>"
st.markdown(tags_html, unsafe_allow_html=True)

# --- ADMIN SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Admin")
    pw = st.text_input("Password", type="password")
    if pw == "chatitaly123":
        if st.button("RESET MURO"):
            st.session_state.muro = []
            st.rerun()
