import streamlit as st
import random
from datetime import datetime
from supabase import create_client

# --- 1. CONNESSIONE ---
URL = "https://wumwurwuwoysrvutupde.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind1bXd1cnd1d295c3J2dXR1cGRlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc5NDgwMzIsImV4cCI6MjA4MzUyNDAzMn0.90s0KWQTOHb2fHdlgS4vvMNI-7iiDA-L0aR0qJ_5k7k"

@st.cache_resource
def init_connection():
    return create_client(URL, KEY)

supabase = init_connection()

st.set_page_config(page_title="Urban Chaos Wall", layout="wide", initial_sidebar_state="collapsed")

# --- 2. LOGICA RESET ---
def auto_reset_check():
    try:
        oggi = datetime.now().strftime("%Y-%m-%d")
        if st.session_state.get("last_check") != oggi:
            res = supabase.table("muro").select("created_at").order("id", desc=True).limit(1).execute()
            if res.data:
                data_ultimo_msg = res.data[0]['created_at'].split('T')[0]
                if data_ultimo_msg != oggi:
                    supabase.table("muro").delete().neq("id", 0).execute()
            st.session_state["last_check"] = oggi
    except: pass

auto_reset_check()

# --- 3. CSS CORE ---
st.markdown("""
    <style>
    [data-testid="stSidebar"], .st-emotion-cache-10o1ihd, footer, header { display: none !important; }
    .stApp {
        background-image: url("https://static.vecteezy.com/system/resources/previews/007/233/624/non_2x/brick-black-wall-texture-background-dark-brickwork-pattern-block-stone-structure-backdrop-dark-brick-wall-realistic-template-abstract-modern-wallpaper-design-illustration-vector.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    ::-webkit-scrollbar { width: 0px; }
    * { scrollbar-width: none; }
    
    .neon-header {
        font-family: 'Rock Salt', cursive;
        text-align: center;
        color: #fff;
        text-shadow: 0 0 10px #FF00FF, 0 0 20px #FF00FF, 0 0 40px #FF00FF;
        font-size: 40px;
        padding: 20px;
        background: rgba(0,0,0,0.4);
    }
    
    /* Form Stile "Clandestino" */
    .stForm {
        background: rgba(0,0,0,0.8) !important;
        border: 2px solid #FF00FF !important;
        border-radius: 20px !important;
        padding: 15px !important;
        position: relative;
        z-index: 999; /* Sempre sopra i graffiti */
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNZIONI ---
def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=False).limit(60).execute()
        return res.data
    except: return []

# --- 5. INPUT ---
st.markdown('<div class="neon-header">CHATITALY WILD WALL</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([0.15, 0.7, 0.15])
with c2:
    with st.form("spray_form", clear_on_submit=True):
        col_n, col_m = st.columns([1, 2])
        nick = col_n.text_input("TAG", value=st.session_state.get("saved_nick", ""), placeholder="Nick")
        txt = col_m.text_area("MESSAGGIO", height=65, placeholder="Spruzza qui...")
        submitted = st.form_submit_button("💨 BOMB THE WALL!")

    if submitted and txt.strip():
        st.session_state["saved_nick"] = nick
        l = len(txt)
        # Font e Dimensioni Hardcore
        if l < 10: f_size, rot, font = random.randint(45, 65), random.randint(-20, 20), "'Rock Salt', cursive"
        elif l < 60: f_size, rot, font = random.randint(28, 40), random.randint(-15, 15), "'Permanent Marker', cursive"
        else: f_size, rot, font = random.randint(18, 24), random.randint(-5, 5), "'Patrick Hand', cursive"

        data = {
            "testo": txt, "autore": nick.upper() if nick.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF", "#00FF7F", "#FFD700", "#FF4500"]),
            "font": font, "rotazione": rot, "font_size": f_size
        }
        try:
            supabase.table("muro").insert(data).execute()
            st.rerun()
        except: st.rerun()

# --- 6. IL MURO CAOTICO ---
messaggi = carica_messaggi()
if messaggi:
    style_block = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Patrick+Hand&display=swap" rel="stylesheet">
    <style>
        .wall-canvas {
            position: relative;
            width: 100%;
            height: 1200px; /* Altezza fissa per permettere il posizionamento assoluto */
            overflow: hidden;
            background: transparent;
        }

        @keyframes sprayIn {
            0% { opacity: 0; filter: blur(20px) brightness(2); transform: scale(1.5); }
            100% { opacity: 1; filter: blur(0px) brightness(1); transform: scale(1); }
        }

        .graffito {
            position: absolute;
            white-space: pre-wrap;
            word-wrap: break-word;
            text-align: center;
            line-height: 1.1;
            animation: sprayIn 0.6s ease-out forwards;
            filter: drop-shadow(4px 4px 0px rgba(0,0,0,0.8));
            cursor: pointer;
            transition: transform 0.2s, z-index 0.2s;
        }
        
        .graffito:hover {
            transform: scale(1.2) rotate(0deg) !important;
            z-index: 1000 !important;
            filter: drop-shadow(0 0 15px currentColor);
        }

        .tag-name {
            display: block;
            font-family: sans-serif;
            font-size: 10px;
            color: rgba(255,255,255,0.4);
            margin-top: 5px;
            text-shadow: none;
        }
    </style>
    """
    
    content_html = ""
    for i, m in
