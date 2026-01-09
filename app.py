import streamlit as st
import random
from supabase import create_client

# --- CONNESSIONE ---
URL = "https://wumwurwuwoysrvutupde.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind1bXd1cnd1d295c3J2dXR1cGRlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc5NDgwMzIsImV4cCI6MjA4MzUyNDAzMn0.90s0KWQTOHb2fHdlgS4vvMNI-7iiDA-L0aR0qJ_5k7k"

@st.cache_resource
def init_connection():
    return create_client(URL, KEY)

supabase = init_connection()

st.set_page_config(page_title="Chatitaly Urban Wall", layout="wide")

# --- CSS: MURO REALE (MATTONI VERI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Nosifer&family=Rubik+Glitch&family=Rock+Salt&display=swap');
    
    /* SFONDO CON MATTONI VERI - LINK AGGIORNATO E SICURO */
    .stApp {
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                          url("https://www.transparenttextures.com/patterns/dark-brick-wall.png"),
                          url("https://images.unsplash.com/photo-1590247813693-5541d1c609fd?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
        background-color: #111;
    }

    .neon-title {
        font-family: 'Permanent Marker', cursive;
        color: #fff;
        text-align: center;
        text-shadow: 0 0 10px #ff00ff, 0 0 20px #00ffff;
        font-size: 55px;
        padding: 15px;
    }

    .wall-area {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 35px;
        padding: 50px;
    }

    .graffiti {
        display: inline-block;
        filter: drop-shadow(3px 3px 2px rgba(0,0,0,0.7));
        line-height: 1.1;
        text-align: center;
    }

    .nick-label {
        font-family: sans-serif;
        font-size: 10px;
        display: block;
        opacity: 0.5;
        color: white;
    }

    /* Rende i box di input più leggibili sul muro */
    .stTextInput > div > div > input {
        background-color: rgba(0,0,0,0.8) !important;
        color: white !important;
        border: 1px solid #ff00ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).limit(30).execute()
        return res.data
    except: return []

def spruzza():
    t = st.session_state.get("input_testo", "")
    n = st.session_state.get("input_nick", "")
    if t and t.strip():
        data = {
            "testo": t.upper(),
            "autore": n.upper() if n.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF"]),
            "font": random.choice(["'Permanent Marker'", "'Nosifer'", "'Rubik Glitch'", "'Rock Salt'"]),
            "rotazione": random.randint(-12, 12),
            "font_size": random.randint(25, 45)
        }
        try:
            supabase.table("muro").insert(data).execute()
            st.session_state["input_testo"] = ""
        except: pass

# --- UI ---
st.markdown('<h1 class="neon-title">CHATITALY WALL</h1>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    col1, col2 = st.columns([1, 2])
    with col1: st.text_input("TAG", key="input_nick", placeholder="Nick")
    with col2: st.text_input("SCRIVI SUL MURO", key="input_testo", on_change=spruzza, placeholder="Messaggio...")

# --- RENDERING GRAFFITI ---
messaggi = carica_messaggi()
if messaggi:
    html_tags = "<div class='wall-area'>"
    for m in messaggi:
        txt = str(m.get('testo', ''))
        aut = str(m.get('autore', 'ANON'))
        col = m.get('colore', '#FFF')
        fnt = m.get('font', 'Arial')
        siz = m.get('font_size', 30)
        rot = m.get('rotazione', 0)
        
        html_tags += f"""
        <div class="graffiti" style="transform: rotate({rot}deg); color: {col}; font-family: {fnt}; font-size: {siz}px;">
            {txt}
            <span class="nick-label">BY {aut}</span>
        </div>
        """
    html_tags += "</div>"
    st.markdown(html_tags, unsafe_allow_html=True)

# Admin Sidebar
with st.sidebar:
    if st.text_input("Admin", type="password") == "chatitaly123":
        if st.button("RESET"):
            supabase.table("muro").delete().neq("id", 0).execute()
            st.rerun()
