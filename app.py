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

st.set_page_config(page_title="Urban Wall Floating", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS CORE (BOX TRASPARENTI) ---
st.markdown("""
    <style>
    header, footer, [data-testid="stSidebar"], [data-testid="stHeader"] { display: none !important; }

    .stApp {
        background-color: #0a0a0a;
        background-image: 
            linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)),
            url("https://www.transparenttextures.com/patterns/dark-brick-wall.png");
        background-attachment: fixed;
    }

    .main-title {
        font-family: 'Rock Salt', cursive;
        text-align: center;
        color: white;
        font-size: 35px;
        padding: 30px 0;
        text-shadow: 0 0 15px #FF00FF;
    }

    .stForm {
        background: rgba(0, 0, 0, 0.7) !important;
        border: 1px solid #444 !important;
        border-radius: 15px !important;
    }

    ::-webkit-scrollbar { width: 0px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CARICAMENTO DATI ---
def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).limit(40).execute()
        return res.data
    except: return []

# --- 4. INPUT ---
st.markdown('<div class="main-title">CHATITALY URBAN WALL</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
with c2:
    with st.form("spray_form", clear_on_submit=True):
        col_n, col_m = st.columns([1, 2])
        nick = col_n.text_input("TAG", placeholder="Chi sei?")
        txt = col_m.text_area("MESSAGGIO", height=70, placeholder="Scrivi sul muro...")
        submitted = st.form_submit_button("💨 BOMB THE WALL")

    if submitted and txt.strip():
        l = len(txt)
        if l < 15: f_size, font = 34, "'Rock Salt', cursive"
        elif l < 60: f_size, font = 26, "'Permanent Marker', cursive"
        else: f_size, font = 20, "'Patrick Hand', cursive"

        data = {
            "testo": txt, "autore": nick.upper() if nick.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF"]),
            "font": font, "rotazione": random.randint(-3, 3), "font_size": f_size
        }
        supabase.table("muro").insert(data).execute()
        st.rerun()

# --- 5. IL MURO (SCRITTE FLUTTUANTI) ---
messaggi = carica_messaggi()
if messaggi:
    style_block = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Patrick+Hand&display=swap" rel="stylesheet">
    <style>
        .wall-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 50px;
            padding: 40px;
            justify-items: center;
        }

        .graffito-container {
            background: transparent; /* Box ora invisibile */
            width: 100%;
            min-height: 200px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
            transition: transform 0.3s ease;
        }

        .graffito-container:hover {
            transform: scale(1.1);
        }

        .text-neon {
            text-align: center;
            line-height: 1.3;
            word-wrap: break-word;
            width: 90%;
            z-index: 2;
        }

        /* GOCCIA NEON CHE PARTE DAL TESTO */
        .drip-effect {
            width: 4px;
            height: 40px;
            background: var(--c);
            margin-top: 10px;
            border-radius: 0 0 10px 10px;
            box-shadow: 0 0 10px var(--c), 0 0 20px var(--c);
            position: relative;
        }
        .drip-effect::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: -3px;
            width: 10px;
            height: 10px;
            background: var(--c);
            border-radius: 50%;
        }

        .author-tag {
            font-family: sans-serif;
            font-size: 11px;
            color: rgba(255,255,255,0.3);
            text-transform: uppercase;
            margin-top: 15px;
            letter-spacing: 2px;
        }
    </style>
    """
    
    content_html = ""
    for m in messaggi:
        content_html += f'''
        <div class="graffito-container">
            <div class="text-neon" style="
                color: {m["colore"]}; 
                font-family: {m["font"]}; 
                font-size: {m["font_size"]}px;
                text-shadow: 0 0 10px {m["colore"]}, 0 0 20px {m["colore"]}66, 2px 2px 4px rgba(0,0,0,0.8);
                transform: rotate({m["rotazione"]}deg);">
                {m["testo"].replace("<","&lt;")}
            </div>
            <div class="drip-effect" style="--c: {m["colore"]};"></div>
            <div class="author-tag">@{m["autore"]}</div>
        </div>
        '''
    
    st.components.v1.html(f"{style_block}<div class='wall-grid'>{content_html}</div>", height=2000, scrolling=False)

# --- ADMIN ---
with st.expander("MOD"):
    if st.text_input("Psw", type="password") == "chatitaly123":
        for m in messaggi:
            col_a, col_b = st.columns([4,1])
            col_a.write(f"{m['autore']}: {m['testo'][:20]}")
            if col_b.button("🗑️", key=f"d_{m['id']}"):
                supabase.table("muro").delete().eq("id", m['id']).execute()
                st.rerun()
