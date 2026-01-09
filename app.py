import streamlit as st
import random
from datetime import datetime
from supabase import create_client, Client

# --- 1. CONNESSIONE SUPABASE (URL CORRETTO) ---
URL = "https://wumwurwuwoysrvutupde.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind1bXd1cnd1d295c3J2dXR1cGRlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc5NDgwMzIsImV4cCI6MjA4MzUyNDAzMn0.90s0KWQTOHb2fHdlgS4vvMNI-7iiDA-L0aR0qJ_5k7k"

@st.cache_resource
def init_connection():
    try:
        return create_client(URL, KEY)
    except Exception as e:
        st.error(f"Errore connessione: {e}")
        return None

supabase = init_connection()

# --- 2. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Il Muro di Chatitaly", layout="wide")

# CSS: Sfondo mattoni e stile graffiti
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
        text-shadow: 0 0 10px #00ffff, 0 0 20px #ff00ff;
        font-size: clamp(30px, 8vw, 70px);
        margin-bottom: 20px;
    }

    .wall-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        gap: 20px;
        padding: 40px;
        min-height: 400px;
    }

    .graffiti-tag {
        display: inline-block;
        padding: 10px;
        transition: all 0.3s ease;
        filter: drop-shadow(4px 4px 3px #000);
    }

    .graffiti-tag:hover {
        transform: scale(1.4) rotate(0deg) !important;
        z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGICA DATABASE ---
def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).execute()
        return res.data
    except Exception as e:
        st.error(f"⚠️ Errore caricamento: {e}")
        return []

def spruzza():
    testo = st.session_state.get("input_testo", "")
    nick = st.session_state.get("input_nick", "")
    
    if testo and testo.strip():
        nuovo_post = {
            "testo": testo.upper(),
            "autore": nick.upper() if nick.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FF5E00", "#FFFFFF"]),
            "font": random.choice(["'Permanent Marker'", "'Nosifer'", "'Rubik Glitch'", "'Special Elite'"]),
            "rotazione": random.randint(-20, 20),
            "font_size": random.randint(28, 55)
        }
        try:
            supabase.table("muro").insert(nuovo_post).execute()
            st.session_state["input_testo"] = "" # Svuota il campo
        except Exception as e:
            st.error(f"❌ Errore scrittura: {e}")

# --- 4. INTERFACCIA ---
st.markdown("<h1 class='neon-title'>CHATITALY WALL</h1>", unsafe_allow_html=True)

with st.container():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        col_n, col_t = st.columns([1, 3])
        with col_n:
            st.text_input("NICK", key="input_nick", placeholder="Nome")
        with col_t:
            st.text_input("SCRIVI SUL MURO", key="input_testo", on_change=spruzza, placeholder="Premi INVIO")

st.write("---")

# --- 5. VISUALIZZAZIONE ---
messaggi = carica_messaggi()

if messaggi:
    tags_html = "<div class='wall-container'>"
    for m in messaggi:
        t = m.get('testo', '')
        a = m.get('autore', 'ANONIMO')
        c = m.get('colore', '#fff')
        f = m.get('font', 'sans-serif')
        r = m.get('rotazione', 0)
        s = m.get('font_size', 30)
        
        tags_html += f"""
            <div class="graffiti-tag" style="
                transform: rotate({r}deg);
                color: {c};
                font-family: {f}, cursive;
                font-size: {s}px;
                text-shadow: 2px 2px 4px #000, 0 0 10px {c}88;
            ">
                {t}
                <div style="font-size: 10px; color: rgba(255,255,255,0.1); font-family: sans-serif;">
                    BY {a}
                </div>
            </div>
        """
    tags_html += "</div>"
    st.markdown(tags_html, unsafe_allow_html=True)
else:
    st.info("🎨 Il muro è pulito. Sii il primo a taggare!")

# --- 6. ADMIN ---
with st.sidebar:
    st.title("Moderazione")
    password = st.text_input("Password", type="password")
    if password == "chatitaly123":
        if st.button("RESET MURO"):
            try:
                supabase.table("muro").delete().neq("id", 0).execute()
                st.rerun()
            except:
                st.error("Errore reset")
