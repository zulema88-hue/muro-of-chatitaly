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

st.set_page_config(page_title="Il Muro di Chatitaly", layout="wide")

# --- CSS: MURO DI MATTONI E EFFETTI GRAFFITI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Nosifer&family=Rubik+Glitch&family=Bungee+Shade&display=swap');
    
    /* Sfondo Muro di Mattoni Scuro */
    .stApp {
        background-color: #1a1a1a;
        background-image: 
            linear-gradient(335deg, #111 23px, transparent 23px),
            linear-gradient(155deg, #151515 23px, transparent 23px),
            linear-gradient(335deg, #111 23px, transparent 23px),
            linear-gradient(155deg, #151515 23px, transparent 23px);
        background-size: 58px 58px;
    }

    .neon-title {
        font-family: 'Bungee Shade', cursive;
        color: #ff00ff;
        text-align: center;
        text-shadow: 3px 3px 0px #00ffff;
        font-size: clamp(30px, 8vw, 60px);
        margin: 20px 0;
    }

    /* Contenitore Muro */
    .brick-wall {
        background: rgba(0,0,0,0.4);
        border: 4px solid #222;
        border-radius: 10px;
        padding: 40px;
        min-height: 500px;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        gap: 30px;
        box-shadow: inset 0 0 50px #000;
    }

    /* Effetto Vernice Spray */
    .tag {
        display: inline-block;
        padding: 5px;
        line-height: 1;
        transition: transform 0.3s;
        filter: drop-shadow(2px 2px 3px rgba(0,0,0,0.8));
    }

    .tag:hover {
        transform: scale(1.2) !important;
        filter: brightness(1.2) drop-shadow(0 0 10px white);
    }

    .author-tag {
        font-family: 'Courier New', monospace;
        font-size: 10px;
        display: block;
        opacity: 0.5;
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).limit(40).execute()
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
            "font": random.choice(["'Permanent Marker'", "'Nosifer'", "'Rubik Glitch'"]),
            "rotazione": random.randint(-15, 15),
            "font_size": random.randint(22, 38)
        }
        try:
            supabase.table("muro").insert(data).execute()
            st.session_state["input_testo"] = ""
        except: pass

# --- INTERFACCIA ---
st.markdown('<h1 class="neon-title">CHATITALY URBAN WALL</h1>', unsafe_allow_html=True)

with st.container():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        col_n, col_t = st.columns([1, 3])
        with col_n:
            st.text_input("NICK", key="input_nick", placeholder="Tag")
        with col_t:
            st.text_input("BOMBOLETTA", key="input_testo", on_change=spruzza, placeholder="Scrivi qui...")

st.markdown("<br>", unsafe_allow_html=True)

# --- IL MURO DI MATTONI ---
messaggi = carica_messaggi()

if messaggi:
    html_muro = "<div class='brick-wall'>"
    for m in messaggi:
        txt = str(m.get('testo', ''))
        aut = str(m.get('autore', 'ANON'))
        col = m.get('colore', '#FFF')
        fnt = m.get('font', 'Arial')
        siz = m.get('font_size', 25)
        rot = m.get('rotazione', 0)
        
        html_muro += f"""
        <div class="tag" style="transform: rotate({rot}deg); color: {col}; font-family: {fnt}; font-size: {siz}px;">
            {txt}
            <span class="author-tag">BY {aut}</span>
        </div>
        """
    html_muro += "</div>"
    st.markdown(html_muro, unsafe_allow_html=True)
else:
    st.info("🎨 Il muro è pronto per i tuoi graffiti. Sii il primo!")

# Sidebar Admin
with st.sidebar:
    if st.text_input("Admin", type="password") == "chatitaly123":
        if st.button("PULISCI MURO"):
            supabase.table("muro").delete().neq("id", 0).execute()
            st.rerun()
