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

# --- CSS DEFINITIVO (PULITO E COPRENTE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Nosifer&family=Rubik+Glitch&display=swap');

    .stApp {
        background-color: #000000 !important;
        background-image: radial-gradient(#333 1px, transparent 1px) !important;
        background-size: 20px 20px !important;
    }

    .neon-title {
        font-family: 'Permanent Marker', cursive;
        color: #00ffff;
        text-align: center;
        text-shadow: 0 0 10px #0ff, 0 0 20px #f0f;
        font-size: 45px;
        margin: 20px 0;
    }

    .wall-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 15px;
        padding: 30px;
    }

    .graffiti-tag {
        display: inline-block;
        padding: 10px;
        text-shadow: 2px 2px 0px #000;
        text-align: center;
    }

    .author-info {
        font-family: sans-serif;
        font-size: 11px;
        color: rgba(255,255,255,0.4);
        display: block;
        margin-top: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).limit(30).execute()
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
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131"]),
            "font": random.choice(["'Permanent Marker'", "'Nosifer'", "'Rubik Glitch'"]),
            "rotazione": random.randint(-10, 10),
            "font_size": random.randint(22, 32) # DIMENSIONE RIDOTTA
        }
        try:
            supabase.table("muro").insert(data).execute()
            st.session_state["input_testo"] = ""
        except:
            pass

# --- INTERFACCIA ---
st.markdown('<h1 class="neon-title">CHATITALY WALL</h1>', unsafe_allow_html=True)

with st.container():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        col_n, col_t = st.columns([1, 3])
        with col_n:
            st.text_input("NICK", key="input_nick", placeholder="Nick")
        with col_t:
            st.text_input("SCRIVI E INVIO", key="input_testo", on_change=spruzza, placeholder="Messaggio...")

st.markdown("<br><hr style='border: 0.5px solid #222'><br>", unsafe_allow_html=True)

# --- VISUALIZZAZIONE CORRETTA ---
messaggi = carica_messaggi()

if messaggi:
    # Costruiamo l'HTML in una variabile e poi lo stampiamo UNA VOLTA SOLA
    html_wall = "<div class='wall-container'>"
    for m in messaggi:
        # Recupero sicuro dei valori
        txt = m.get('testo', '')
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
    st.write("Muro vuoto...")

# Sezione Admin segreta nella sidebar
if st.sidebar.text_input("Admin", type="password") == "chatitaly123":
    if st.sidebar.button("PULISCI TUTTO"):
        supabase.table("muro").delete().neq("id", 0).execute()
        st.rerun()
