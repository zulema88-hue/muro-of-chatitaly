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

# --- CSS (SUPER SICURO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Nosifer&family=Rubik+Glitch&display=swap');

    .stApp { background-color: #000000 !important; }
    
    .neon-title {
        font-family: 'Permanent Marker', cursive;
        color: #00ffff;
        text-align: center;
        text-shadow: 0 0 10px #0ff;
        font-size: 40px;
    }

    /* Box per i messaggi */
    .msg-box {
        display: inline-block;
        margin: 10px;
        padding: 10px;
        border-radius: 5px;
        line-height: 1.2;
    }

    .author {
        font-size: 10px;
        color: #888;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)

def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).limit(25).execute()
        return res.data
    except:
        return []

def spruzza():
    t = st.session_state.get("input_testo", "")
    n = st.session_state.get("input_nick", "ANON")
    if t and t.strip():
        data = {
            "testo": t.upper(),
            "autore": n.upper(),
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131"]),
            "font": random.choice(["'Permanent Marker'", "'Nosifer'", "'Rubik Glitch'"]),
            "rotazione": random.randint(-5, 5),
            "font_size": random.randint(18, 28)
        }
        try:
            supabase.table("muro").insert(data).execute()
            st.session_state["input_testo"] = ""
        except:
            pass

# --- INTERFACCIA ---
st.markdown('<h1 class="neon-title">CHATITALY WALL</h1>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    n = st.text_input("NICK", key="input_nick", placeholder="Il tuo nome")
    t = st.text_input("MESSAGGIO", key="input_testo", on_change=spruzza, placeholder="Scrivi e premi Invio")

st.divider()

# --- VISUALIZZAZIONE ---
messaggi = carica_messaggi()

if messaggi:
    # Usiamo un unico grande contenitore HTML per evitare che il codice si spezzi
    contenuto_muro = "<div style='text-align: center;'>"
    for m in messaggi:
        testo = m.get('testo', '')
        autore = m.get('autore', 'ANON')
        colore = m.get('colore', '#FFF')
        font = m.get('font', 'sans-serif')
        size = m.get('font_size', 20)
        rot = m.get('rotazione', 0)
        
        # Creiamo il singolo tag in modo pulito
        tag = f"""
        <div class="msg-box" style="transform: rotate({rot}deg); color: {colore}; font-family: {font}; font-size: {size}px;">
            {testo}
            <span class="author">BY {autore}</span>
        </div>
        """
        contenuto_muro += tag
    
    contenuto_muro += "</div>"
    
    # Stampiamo tutto il muro in un colpo solo
    st.markdown(contenuto_muro, unsafe_allow_html=True)

# Admin
if st.sidebar.text_input("Admin", type="password") == "chatitaly123":
    if st.sidebar.button("RESET"):
        supabase.table("muro").delete().neq("id", 0).execute()
        st.rerun()
