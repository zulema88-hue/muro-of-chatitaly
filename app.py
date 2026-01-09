import streamlit as st
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Il Muro di Chatitaly", layout="wide")

# CSS PER MURO DI MATTONI E GRAFFITI REALI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Frijole&family=Nosifer&family=Rubik+Glitch&display=swap');
    
    .stApp {
        /* Sfondo Muro di Mattoni */
        background-color: #111;
        background-image: 
            linear-gradient(335deg, #0a0a0a 23px, transparent 23px),
            linear-gradient(155deg, #0f0f0f 23px, transparent 23px),
            linear-gradient(335deg, #0a0a0a 23px, transparent 23px),
            linear-gradient(155deg, #0f0f0f 23px, transparent 23px);
        background-size: 58px 58px;
        background-position: 0px 2px, 4px 35px, 29px 31px, 34px 6px;
    }

    .neon-title {
        font-family: 'Frijole', cursive;
        color: #fff;
        text-align: center;
        text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff;
        font-size: clamp(30px, 8vw, 70px);
        padding: 20px;
    }

    .graffiti-sticker {
        padding: 10px;
        line-height: 0.9;
        transition: all 0.2s;
        filter: drop-shadow(2px 2px 2px #000);
        word-wrap: break-word;
    }

    .graffiti-sticker:hover {
        transform: scale(1.2) rotate(0deg) !important;
        z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INIZIALIZZAZIONE ---
if 'muro' not in st.session_state:
    st.session_state.muro = []

# Lista Font e Colori molto varia
font_styles = ["'Permanent Marker', cursive", "'Nosifer', cursive", "'Rubik Glitch', display", "'Bangers', system-ui"]
colors = ["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FF5E00", "#FFFFFF", "#CCFF00", "#FF007F"]

# --- LOGICA ---
def spruzza():
    testo = st.session_state.input_testo
    if testo.strip():
        nuovo_post = {
            "testo": testo.upper(),
            "colore": random.choice(colors),
            "font": random.choice(font_styles),
            "rotazione": random.randint(-15, 15), # Più rotazione
            "font_size": random.randint(35, 60),  # Più grandi
            "ora": datetime.now().strftime("%H:%M")
        }
        st.session_state.muro.append(nuovo_post)
        st.session_state.input_testo = ""

# --- INTERFACCIA ---
st.markdown("<h1 class='neon-title'>CHATITALY WALL</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.text_input("PRENDI LA BOMBOLETTA E SCRIVI... 🎨", key="input_testo", on_change=spruzza, placeholder="Scrivi qui e premi INVIO")

st.markdown("<br><br>", unsafe_allow_html=True)

# --- IL MURO (DISPOSIZIONE CASUALE) ---
# Usiamo 4 colonne per un effetto più "disordinato" da muro
cols = st.columns(4)

for i, m in enumerate(reversed(st.session_state.muro)):
    with cols[i % 4]:
        st.markdown(f"""
            <div class="graffiti-sticker" style="
                transform: rotate({m['rotazione']}deg);
                color: {m['colore']};
                font-family: {m['font']};
                font-size: {m['font_size']}px;
                text-shadow: 3px 3px 5px #000, 0 0 15px {m['colore']}aa;
            ">
                {m['testo']}
                <div style="font-size: 10px; color: rgba(255,255,255,0.2); font-family: sans-serif; text-shadow: none; margin-top: 5px;">
                    {m['ora']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- ADMIN SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Moderazione")
    pw = st.text_input("Password Admin", type="password")
    if pw == "chatitaly123":
        if st.button("CANCELLA TUTTO IL MURO"):
            st.session_state.muro = []
            st.rerun()
