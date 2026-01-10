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

st.set_page_config(page_title="Urban Wall Pro", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS CORE (DESIGN DEFINITO) ---
st.markdown("""
    <style>
    header, footer, [data-testid="stSidebar"], [data-testid="stHeader"] { display: none !important; }

    /* SFONDO MATTONI ALTA DEFINIZIONE */
    .stApp {
        background-color: #0a0a0a;
        background-image: 
            linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
            url("https://www.transparenttextures.com/patterns/dark-brick-wall.png"); /* Texture nitida */
        background-attachment: fixed;
    }

    .main-title {
        font-family: 'Rock Salt', cursive;
        text-align: center;
        color: white;
        font-size: 35px;
        padding: 30px 0;
        text-shadow: 0 0 10px #FF00FF;
    }

    /* FORM STILE MODERNO */
    .stForm {
        background: rgba(20, 20, 20, 0.9) !important;
        border: 1px solid #333 !important;
        border-radius: 15px !important;
        padding: 20px !important;
    }

    ::-webkit-scrollbar { width: 0px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATI ---
def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).limit(40).execute()
        return res.data
    except: return []

# --- 4. INTERFACCIA ---
st.markdown('<div class="main-title">CHATITALY URBAN WALL</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
with c2:
    with st.form("clean_spray", clear_on_submit=True):
        col_n, col_m = st.columns([1, 2])
        nick = col_n.text_input("TAG", placeholder="Il tuo tag...")
        txt = col_m.text_area("MESSAGGIO", height=70, placeholder="Scrivi il tuo graffito...")
        submitted = st.form_submit_button("💨 BOMB THE WALL")

    if submitted and txt.strip():
        l = len(txt)
        # Font e dimensioni come nella reference
        if l < 15: f_size, font = 32, "'Rock Salt', cursive"
        elif l < 60: f_size, font = 24, "'Permanent Marker', cursive"
        else: f_size, font = 18, "'Patrick Hand', cursive"

        data = {
            "testo": txt, "autore": nick.upper() if nick.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF"]),
            "font": font, "rotazione": 0, "font_size": f_size
        }
        supabase.table("muro").insert(data).execute()
        st.rerun()

# --- 5. IL MURO (GRIGLIA ORDINATA + GOCCIA NEON) ---
messaggi = carica_messaggi()
if messaggi:
    style_block = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Patrick+Hand&display=swap" rel="stylesheet">
    <style>
        .wall-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 30px;
            padding: 40px;
            justify-items: center;
        }

        .graffito-card {
            background: rgba(255, 255, 255, 0.08); /* Box semi-trasparente */
            border-radius: 12px;
            padding: 20px;
            width: 100%;
            min-height: 180px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255,255,255,0.1);
        }

        .text-content {
            text-align: center;
            line-height: 1.2;
            word-wrap: break-word;
            width: 100%;
            margin-bottom: 15px;
        }

        /* LA GOCCIA NEON CENTRALE */
        .drip {
            position: absolute;
            bottom: -20px;
            left: 50%;
            transform: translateX(-50%);
            width: 4px;
            height: 30px;
            background: var(--c);
            border-radius: 0 0 10px 10px;
            box-shadow: 0 0 10px var(--c);
        }
        .drip::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: -2px;
            width: 8px;
            height: 8px;
            background: var(--c);
            border-radius: 50%;
            box-shadow: 0 0 15px var(--c);
        }

        .author-tag {
            font-family: sans-serif;
            font-size: 10px;
            color: rgba(255,255,255,0.4);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
    </style>
    """
    
    content_html = ""
    for m in messaggi:
        content_html += f'''
        <div class="graffito-card">
            <div class="text-content" style="
                color: {m["colore"]}; 
                font-family: {m["font"]}; 
                font-size: {m["font_size"]}px;
                text-shadow: 0 0 8px {m["colore"]}44;">
                {m["testo"].replace("<","&lt;")}
            </div>
            <div class="drip" style="--c: {m["colore"]};"></div>
            <div class="author-tag">BY {m["autore"]}</div>
        </div>
        '''
    
    st.components.v1.html(f"{style_block}<div class='wall-grid'>{content_html}</div>", height=2000, scrolling=False)

# --- 6. ADMIN ---
with st.expander("MOD"):
    if st.text_input("Psw", type="password") == "chatitaly123":
        for m in messaggi:
            col_a, col_b = st.columns([4,1])
            col_a.write(f"{m['autore']}: {m['testo'][:20]}")
            if col_b.button("🗑️", key=f"d_{m['id']}"):
                supabase.table("muro").delete().eq("id", m['id']).execute()
                st.rerun()
