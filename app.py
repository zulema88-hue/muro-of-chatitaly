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

st.set_page_config(page_title="Urban Wall HD", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS CORE (NITIDEZZA, SCHIZZI E BOMBOLETTE) ---
st.markdown("""
    <style>
    header, footer, [data-testid="stSidebar"], [data-testid="stHeader"] { display: none !important; }

    .stApp {
        background-color: #050505;
        background-image: 
            linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)),
            url("https://www.transparenttextures.com/patterns/dark-brick-wall.png");
        background-attachment: fixed;
    }

    /* TITOLO DEFINITO */
    .graffiti-title {
        font-family: 'Rock Salt', cursive;
        text-align: center;
        color: #FFFFFF;
        font-size: clamp(35px, 8vw, 65px);
        padding: 20px 0;
        letter-spacing: -1px;
        text-shadow: 2px 2px 0px #000, 0 0 10px #FF00FF;
        transform: rotate(-1deg);
    }

    /* CONTAINER INPUT CON BOMBOLETTE */
    .input-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        margin-bottom: 40px;
    }

    .spray-can {
        font-size: 50px;
        filter: drop-shadow(0 0 10px rgba(0,255,255,0.5));
    }

    .stForm {
        background: rgba(0, 0, 0, 0.8) !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
        flex-grow: 1;
        max-width: 700px;
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

# --- 4. INPUT CON BOMBOLETTE ---
st.markdown('<div class="graffiti-title">CHATITALY<br>URBAN WALL</div>', unsafe_allow_html=True)

# Layout per le bombolette
col1, col2, col3 = st.columns([0.15, 0.7, 0.15])

with col1:
    st.markdown("<div style='text-align: right;' class='spray-can'>🧴</div>", unsafe_allow_html=True) # Icona bomboletta sinistra

with col2:
    with st.form("spray_form", clear_on_submit=True):
        col_n, col_m = st.columns([1, 2])
        nick = col_n.text_input("TAG", placeholder="Chi sei?")
        txt = col_m.text_area("MESSAGGIO", height=70, placeholder="Lascia il tuo segno...")
        submitted = st.form_submit_button("💨 BOMB THE WALL")

    if submitted and txt.strip():
        l = len(txt)
        if l < 15: f_size, font = 36, "'Rock Salt', cursive"
        elif l < 60: f_size, font = 28, "'Permanent Marker', cursive"
        else: f_size, font = 22, "'Patrick Hand', cursive"

        data = {
            "testo": txt, "autore": nick.upper() if nick.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF", "#00FF7F"]),
            "font": font, "rotazione": random.randint(-4, 4), "font_size": f_size
        }
        supabase.table("muro").insert(data).execute()
        st.rerun()

with col3:
    st.markdown("<div style='text-align: left;' class='spray-can'>🧴</div>", unsafe_allow_html=True) # Icona bomboletta destra

# --- 5. IL MURO CON SCHIZZI ---
messaggi = carica_messaggi()
if messaggi:
    style_block = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Patrick+Hand&display=swap" rel="stylesheet">
    <style>
        .wall-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 60px;
            padding: 50px 20px;
            justify-items: center;
        }

        .graffito-container {
            position: relative;
            width: 100%;
            min-height: 220px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        .paint-splatter {
            position: absolute;
            width: 150px;
            height: 150px;
            background: var(--c);
            filter: blur(45px);
            opacity: 0.25;
            border-radius: 50%;
            z-index: 1;
            top: var(--top);
            left: var(--left);
        }

        .text-neon {
            text-align: center;
            line-height: 1.2;
            word-wrap: break-word;
            width: 90%;
            z-index: 2;
            text-shadow: 1px 1px 2px #000, 0 0 8px var(--c);
        }

        .drip-effect {
            width: 3px;
            height: 35px;
            background: var(--c);
            margin-top: 10px;
            border-radius: 0 0 10px 10px;
            box-shadow: 0 0 10px var(--c);
            position: relative;
            z-index: 2;
        }

        .author-tag {
            font-family: sans-serif;
            font-size: 10px;
            color: rgba(255,255,255,0.4);
            text-transform: uppercase;
            margin-top: 12px;
            letter-spacing: 2px;
            z-index: 2;
        }
    </style>
    """
    
    content_html = ""
    for m in messaggi:
        random.seed(m['id'])
        s_top = f"{random.randint(10, 50)}%"
        s_left = f"{random.randint(20, 60)}%"
        
        content_html += f'''
        <div class="graffito-container">
            <div class="paint-splatter" style="--c: {m["colore"]}; --top: {s_top}; --left: {s_left};"></div>
            <div class="text-neon" style="
                color: {m["colore"]}; 
                font-family: {m["font"]}; 
                font-size: {m["font_size"]}px;
                --c: {m["colore"]};
                transform: rotate({m["rotazione"]}deg);">
                {m["testo"].replace("<","&lt;")}
            </div>
            <div class="drip-effect" style="--c: {m["colore"]};"></div>
            <div class="author-tag">@{m["autore"]}</div>
        </div>
        '''
    
    st.components.v1.html(f"{style_block}<div class='wall-grid'>{content_html}</div>", height=2500, scrolling=False)

# --- 6. ADMIN ---
with st.expander("MOD"):
    if st.text_input("Psw", type="password") == "chatitaly123":
        for m in messaggi:
            col_a, col_b = st.columns([4,1])
            col_a.write(f"{m['autore']}: {m['testo'][:20]}")
            if col_b.button("🗑️", key=f"d_{m['id']}"):
                supabase.table("muro").delete().eq("id", m['id']).execute()
                st.rerun()
