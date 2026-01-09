import streamlit as st
import random
from datetime import datetime
from supabase import create_client, Client

# --- CONNESSIONE SUPABASE ---
URL = "https://wumwurwuwowysrvutupde.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind1bXd1cnd1d295c3J2dXR1cGRlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc5NDgwMzIsImV4cCI6MjA4MzUyNDAzMn0.90s0KWQTOHb2fHdlgS4vvMNI-7iiDA-L0aR0qJ_5k7k"

@st.cache_resource
def init_connection():
    return create_client(URL, KEY)

supabase = init_connection()

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Il Muro di Chatitaly", layout="wide")

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
        filter: drop-shadow(3px 3px 2px #000);
        transition: all 0.3s;
    }

    .graffiti-tag:hover {
        transform: scale(1.3) rotate(0deg) !important;
        z-index: 999;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONI DATABASE ---
def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).execute()
        return res.data
    except:
        return []

def spruzza():
    testo = st.session_state.input_testo
    nick = st.session_state.input_nick
    if testo.strip():
        nuovo_post = {
            "testo": testo.upper(),
            "autore": nick.upper() if nick.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FF5E00", "#FFFFFF"]),
            "font": random.choice(["'Permanent Marker'", "'Nosifer'", "'Rubik Glitch'", "'Special Elite'"]),
            "rotazione": random.randint(-20, 20),
            "font_size": random.randint(22, 55)
        }
        try:
            supabase.table("muro").insert(nuovo_post).execute()
            st.session_state.input_testo = ""
            st.session_state.input_nick = ""
        except Exception as e:
            st.error(f"Errore: Assicurati di aver disattivato RLS su Supabase! {e}")

# --- INTERFACCIA ---
st.markdown("<h1 class='neon-title'>CHATITALY WALL</h1>", unsafe_allow_html=True)

with st.container():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        col_n, col_t = st.columns([1, 2])
        with col_n:
            st.text_input("NICKNAME", key="input_nick", placeholder="Nome")
        with col_t:
            st.text_input("PENSIERO", key="input_testo", on_change=spruzza, placeholder="Scrivi e premi INVIO")

# --- IL MURO ---
messaggi = carica_messaggi()
if messaggi:
    tags_html = "<div class='wall-container'>"
    for m in messaggi:
        tags_html += f"""
            <div class="graffiti-tag" style="
                transform: rotate({m.get('rotazione', 0)}deg);
                color: {m.get('colore', '#fff')};
                font-family: {m.get('font', 'sans-serif')}, cursive;
                font-size: {m.get('font_size', 30)}px;
                text-shadow: 2px 2px 4px #000, 0 0 8px {m.get('colore', '#fff')}88;
            ">
                {m.get('testo', '')}
                <div style="font-size: 10px; color: rgba(255,255,255,0.2); font-family: sans-serif; text-shadow: none;">
                    BY {m.get('autore', 'ANONIMO')}
                </div>
            </div>
        """
    tags_html += "</div>"
    st.markdown(tags_html, unsafe_allow_html=True)
else:
    st.info("Il muro è pulito. Sii il primo a spruzzare!")

# --- ADMIN ---
with st.sidebar:
    pw = st.text_input("Admin", type="password")
    if pw == "chatitaly123":
        if st.button("RESET MURO"):
            supabase.table("muro").delete().neq("id", 0).execute()
            st.rerun()
