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

# --- CSS: MURO REALE E EFFETTO SPRAY ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Nosifer&family=Rubik+Glitch&family=Rock+Salt&display=swap');
    
    /* SFONDO CON IMMAGINE DI MATTONI REALI */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
        background-size: cover;
        background-attachment: fixed;
    }

    /* TITOLO NEON SOPRA IL MURO */
    .neon-title {
        font-family: 'Permanent Marker', cursive;
        color: #fff;
        text-align: center;
        text-shadow: 0 0 10px #0ff, 0 0 20px #0ff, 0 0 40px #0ff;
        font-size: 60px;
        padding: 20px;
        background: rgba(0,0,0,0.3);
    }

    /* CONTENITORE TRASPARENTE PER I GRAFFITI */
    .wall-area {
        min-height: 600px;
        padding: 50px;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        gap: 40px;
    }

    /* EFFETTO SCRITTA VERNICIATA */
    .graffiti {
        display: inline-block;
        filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.9)); /* Ombra per profondità */
        white-space: pre-wrap;
        max-width: 300px;
        line-height: 1;
    }

    .nick-label {
        font-family: 'Courier New', monospace;
        font-size: 10px;
        display: block;
        opacity: 0.6;
        color: white;
        text-shadow: 1px 1px 1px #000;
    }

    /* STILIZZAZIONE INPUT BOX */
    div[data-baseweb="input"] {
        background-color: rgba(0,0,0,0.7) !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).limit(35).execute()
        return res.data
    except: return []

def spruzza():
    t = st.session_state.get("input_testo", "")
    n = st.session_state.get("input_nick", "ANON")
    if t and t.strip():
        data = {
            "testo": t.upper(),
            "autore": n.upper() if n.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF", "#00FF7F"]),
            "font": random.choice(["'Permanent Marker'", "'Nosifer'", "'Rubik Glitch'", "'Rock Salt'"]),
            "rotazione": random.randint(-15, 15),
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
    st.text_input("NICKNAME", key="input_nick", placeholder="Il tuo tag...")
    st.text_input("SCRIVI SUL MURO", key="input_testo", on_change=spruzza, placeholder="Premi Invio per spruzzare!")

st.markdown("<div class='wall-area'>", unsafe_allow_html=True)

# --- RENDERING GRAFFITI ---
messaggi = carica_messaggi()
if messaggi:
    html_tags = ""
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
    st.markdown(html_tags, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Admin Sidebar
with st.sidebar:
    if st.text_input("Moderazione", type="password") == "chatitaly123":
        if st.button("Pulisci Muro"):
            supabase.table("muro").delete().neq("id", 0).execute()
            st.rerun()
