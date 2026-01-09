import streamlit as st
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Il Muro di Chatitaly", layout="wide")

# --- LOGICA DI RESET MEZZANOTTE ---
# Inizializziamo la data dell'ultimo reset se non esiste
if 'ultimo_reset' not in st.session_state:
    st.session_state.ultimo_reset = datetime.now().date()

# Se la data attuale è diversa da quella salvata, svuota il muro (è passata la mezzanotte)
if datetime.now().date() > st.session_state.ultimo_reset:
    st.session_state.muro = []
    st.session_state.ultimo_reset = datetime.now().date()

# --- CSS PER MURO DI MATTONI E GRAFFITI ---
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
        text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff;
        font-size: clamp(25px, 6vw, 60px);
        margin-bottom: 0px;
    }

    .wall-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        gap: 15px;
        padding: 40px;
    }

    .graffiti-tag {
        display: inline-block;
        padding: 5px 15px;
        transition: all 0.3s;
        filter: drop-shadow(3px 3px 2px #000);
    }

    .graffiti-tag:hover {
        transform: scale(1.4) rotate(0deg) !important;
        z-index: 999;
        filter: drop-shadow(0 0 15px white);
    }
    </style>
    """, unsafe_allow_html=True)

# --- INIZIALIZZAZIONE ---
if 'muro' not in st.session_state:
    st.session_state.muro = []

font_styles = ["'Permanent Marker'", "'Nosifer'", "'Rubik Glitch'", "'Bangers'", "'Special Elite'"]
colors = ["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FF5E00", "#FFFFFF", "#CCFF00", "#FF007F"]

# --- FUNZIONE SCRITTURA ---
def spruzza():
    testo = st.session_state.input_testo
    nick = st.session_state.input_nick
    if testo.strip():
        nuovo_post = {
            "testo": testo.upper(),
            "autore": nick.upper() if nick.strip() else "ANONIMO",
            "colore": random.choice(colors),
            "font": random.choice(font_styles),
            "rotazione": random.randint(-25, 25),
            "font_size": random.randint(22, 58),
            "ora": datetime.now().strftime("%H:%M")
        }
        st.session_state.muro.append(nuovo_post)
        st.session_state.input_testo = "" # Svuota campo dopo invio

# --- INTERFACCIA ---
st.markdown("<h1 class='neon-title'>CHATITALY WALL</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#444; font-size:12px;'>Reset automatico alle 00:00 | Oggi è il {st.session_state.ultimo_reset}</p>", unsafe_allow_html=True)

with st.container():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        col_n, col_t = st.columns([1, 2])
        with col_n:
            st.text_input("NICKNAME", key="input_nick", placeholder="Chi sei?")
        with col_t:
            st.text_input("PENSIERO", key="input_testo", on_change=spruzza, placeholder="Scrivi e premi INVIO")

# --- IL MURO ---
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
            <div style="font-size: 10px; color: rgba(255,255,255,0.2); font-family: sans-serif; text-shadow: none;">
                {m['autore']} @ {m['ora']}
            </div>
        </div>
    """
tags_html += "</div>"
st.markdown(tags_html, unsafe_allow_html=True)

# --- SIDEBAR ADMIN ---
with st.sidebar:
    st.title("🛡️ Moderazione")
    pw = st.text_input("Password", type="password")
    if pw == "chatitaly123":
        if st.button("RESET MANUALE"):
            st.session_state.muro = []
            st.rerun()
        st.write("---")
        for i, m in enumerate(st.session_state.muro):
            if st.button(f"Elimina: {m['testo'][:15]}", key=f"d_{i}"):
                st.session_state.muro.pop(i)
                st.rerun()
