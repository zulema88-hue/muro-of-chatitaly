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

st.set_page_config(page_title="Chatitaly Urban Wall", layout="wide", initial_sidebar_state="collapsed")

# --- CSS: MURO E RIMOZIONE SIDEBAR ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Nosifer&family=Rubik+Glitch&family=Rock+Salt&display=swap');
    
    # /* NASCONDE SIDEBAR E PULSANTI STREAMLIT */
    [data-testid="stSidebar"], .st-emotion-cache-10o1ihd, .st-emotion-cache-6q9sum {
        display: none !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* SFONDO MURO */
    .stApp {
        background-image: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), 
                          url("https://static.vecteezy.com/system/resources/previews/007/233/624/non_2x/brick-black-wall-texture-background-dark-brickwork-pattern-block-stone-structure-backdrop-dark-brick-wall-realistic-template-abstract-modern-wallpaper-design-illustration-vector.jpg");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }

    .neon-title {
        font-family: 'Permanent Marker', cursive;
        color: #fff;
        text-align: center;
        text-shadow: 0 0 15px #ff00ff, 0 0 30px #00ffff;
        font-size: clamp(40px, 10vw, 70px);
        padding: 20px 0;
    }

    .wall-area {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 40px;
        padding: 40px 10px;
        min-height: 400px;
    }

    .graffiti {
        display: inline-block;
        filter: drop-shadow(4px 4px 2px rgba(0,0,0,0.8));
        line-height: 1.1;
        text-align: center;
    }

    .nick-label {
        font-family: sans-serif;
        font-size: 11px;
        display: block;
        opacity: 0.6;
        color: #eee;
        margin-top: 5px;
    }

    /* INPUT BOX STILE DARK */
    .stTextInput > div > div > input {
        background-color: rgba(0,0,0,0.8) !important;
        color: #39FF14 !important;
        border: 2px solid #333 !important;
        border-radius: 10px !important;
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
            "font": random.choice(["'Permanent Marker'", "'Nosifer'", "'Rubik Glitch'", "'Rock Salt'"]),
            "rotazione": random.randint(-12, 12),
            "font_size": random.randint(28, 48)
        }
        try:
            supabase.table("muro").insert(data).execute()
            st.session_state["input_testo"] = ""
        except: pass

# --- INTERFACCIA ---
st.markdown('<h1 class="neon-title">CHATITALY WALL</h1>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    col1, col2 = st.columns([1, 3])
    with col1: 
        st.text_input("TAG", key="input_nick", placeholder="Nick")
    with col2: 
        st.text_input("SCRIVI SUL MURO", key="input_testo", on_change=spruzza, placeholder="Premi Invio...")

# --- VISUALIZZAZIONE MURO ---
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

# --- ZONA ADMIN (IN FONDO, QUASI INVISIBILE) ---
st.markdown("<br><br><br><br><br><hr style='opacity:0.1'>", unsafe_allow_html=True)
with st.expander("Admin Panel"):
    pw = st.text_input("Password", type="password")
    if pw == "chatitaly123":
        if st.button("RESET MURO"):
            supabase.table("muro").delete().neq("id", 0).execute()
            st.rerun()
