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

# Configurazione pagina (deve essere la prima istruzione Streamlit)
st.set_page_config(page_title="Il Muro di Chatitaly", layout="wide")

# --- CSS FORZATO ---
st.markdown("""
    <style>
    /* Caricamento Font */
    @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Nosifer&family=Rubik+Glitch&family=Special+Elite&display=swap');

    /* Sfondo globale nero */
    .stApp {
        background-color: #000000 !important;
        background-image: radial-gradient(#333 1px, transparent 1px) !important;
        background-size: 20px 20px !important;
    }

    /* Titolo Neon */
    .neon-title {
        font-family: 'Permanent Marker', cursive;
        color: #00ffff;
        text-align: center;
        text-shadow: 0 0 10px #00ffff, 0 0 20px #ff00ff;
        font-size: 50px;
        margin-bottom: 30px;
    }

    /* Contenitore Graffiti */
    .wall-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 20px;
        padding: 30px;
        background: rgba(20, 20, 20, 0.8);
        border: 2px solid #222;
        border-radius: 15px;
    }

    /* Stile singolo Messaggio */
    .graffiti-tag {
        display: inline-block;
        padding: 10px;
        line-height: 1.2;
        text-shadow: 2px 2px 0px #000;
        transition: transform 0.2s;
    }

    .graffiti-tag:hover {
        transform: scale(1.1) rotate(0deg) !important;
    }

    .author-info {
        font-family: sans-serif;
        font-size: 10px;
        color: #888;
        display: block;
        margin-top: 5px;
        text-transform: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGICA ---
def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).limit(40).execute()
        return res.data
    except:
        return []

def spruzza():
    t = st.session_state.get("input_testo", "")
    n = st.session_state.get("input_nick", "ANON")
    if t and t.strip():
        data = {
            "testo": t.upper(),
            "autore": n.upper() if n.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FF5E00"]),
            "font": random.choice(["'Permanent Marker'", "'Nosifer'", "'Rubik Glitch'", "'Special Elite'"]),
            "rotazione": random.randint(-12, 12),
            "font_size": random.randint(20, 35) # Dimensioni ridotte come richiesto
        }
        try:
            supabase.table("muro").insert(data).execute()
            st.session_state["input_testo"] = ""
        except Exception as e:
            st.error(f"Errore: {e}")

# --- INTERFACCIA ---
st.markdown('<h1 class="neon-title">CHATITALY WALL</h1>', unsafe_allow_html=True)

with st.container():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        col_n, col_t = st.columns([1, 3])
        with col_n:
            st.text_input("NICK", key="input_nick", placeholder="Chi sei?")
        with col_t:
            st.text_input("SCRIVI E INVIO", key="input_testo", on_change=spruzza, placeholder="Il tuo messaggio...")

st.markdown("<br><hr style='border: 1px solid #333'><br>", unsafe_allow_html=True)

# --- VISUALIZZAZIONE ---
messaggi = carica_messaggi()

if messaggi:
    html_wall = "<div class='wall-container'>"
    for m in messaggi:
        txt = m.get('testo', 'EMPTY')
        aut = m.get('autore', 'ANON')
        col = m.get('colore', '#FFF')
        fnt = m.get('font', 'Arial')
        rot = m.get('rotazione', 0)
        siz = m.get('font_size', 25)
        
        html_wall += f"""
        <div class="graffiti-tag" style="transform: rotate({rot}deg); color: {col}; font-family: {fnt}; font-size: {siz}px;">
            {txt}
            <span class="author-info">BY {aut}</span>
        </div>
        """
    html_wall += "</div>"
    st.markdown(html_wall, unsafe_allow_html=True)
else:
    st.markdown("<p style='text-align:center; color:#555;'>Muro pulito. Lascia un segno!</p>", unsafe_allow_html=True)

# Admin Panel in fondo o sidebar
if st.sidebar.text_input("Admin", type="password") == "chatitaly123":
    if st.sidebar.button("RESET"):
        supabase.table("muro").delete().neq("id", 0).execute()
        st.rerun()
