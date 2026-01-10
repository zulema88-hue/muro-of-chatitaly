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

# --- 2. CSS CORE (BOMBOLETTE CSS + TITOLO) ---
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
        font-size: clamp(35px, 8vw, 60px);
        padding: 20px 0;
        text-shadow: 2px 2px 0px #000, 0 0 15px #FF00FF;
    }

    /* BOMBOLETTA DISEGNATA IN CSS */
    .can-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 30px;
        margin-top: 20px;
    }

    .spray-can-css {
        width: 45px;
        height: 100px;
        background: linear-gradient(90deg, #333 0%, #666 50%, #333 100%);
        border-radius: 8px 8px 4px 4px;
        position: relative;
        border: 1px solid #111;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }
    
    /* Cappuccio della bomboletta */
    .spray-can-css::before {
        content: '';
        position: absolute;
        top: -12px;
        left: 50%;
        transform: translateX(-50%);
        width: 25px;
        height: 15px;
        background: #222;
        border-radius: 4px 4px 0 0;
    }

    /* Erogatore */
    .spray-can-css::after {
        content: '';
        position: absolute;
        top: -18px;
        left: 50%;
        transform: translateX(-50%);
        width: 8px;
        height: 8px;
        background: #eee;
        border-radius: 2px;
    }

    .stForm {
        background: rgba(0, 0, 0, 0.85) !important;
        border: 1px solid #444 !important;
        border-radius: 15px !important;
        max-width: 650px;
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

# --- 4. INTERFACCIA CON BOMBOLETTE ---
st.markdown('<div class="graffiti-title">CHATITALY URBAN WALL</div>', unsafe_allow_html=True)

# Layout: Bomboletta - Form - Bomboletta
c1, c2, c3 = st.columns([0.2, 0.6, 0.2])

with c1:
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="spray-can-css" style="margin-left: auto; transform: rotate(-10deg);"></div>', unsafe_allow_html=True)

with c2:
    with st.form("spray_form", clear_on_submit=True):
        col_n, col_m = st.columns([1, 2])
        nick = col_n.text_input("TAG", placeholder="Chi sei?")
        txt = col_m.text_area("MESSAGGIO", height=70, placeholder="Bombola il muro...")
        submitted = st.form_submit_button("💨 BOMB THE WALL")

    if submitted and txt.strip():
        l = len(txt)
        if l < 15: f_size, font = 36, "'Rock Salt', cursive"
        elif l < 60: f_size, font = 28, "'Permanent Marker', cursive"
        else: f_size, font = 22, "'Patrick Hand', cursive"

        data = {
            "testo": txt, "autore": nick.upper() if nick.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF"]),
            "font": font, "rotazione": random.randint(-4, 4), "font_size": f_size
        }
        supabase.table("muro").insert(data).execute()
        st.rerun()

with c3:
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="spray-can-css" style="margin-right: auto; transform: rotate(10deg);"></div>', unsafe_allow_html=True)

# --- 5. IL MURO ---
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
            width: 160px;
            height: 160px;
            background: var(--c);
            filter: blur(50px);
            opacity: 0.22;
            z-index: 1;
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
            z-index: 2;
        }
        .author-tag {
            font-family: sans-serif;
            font-size: 10px;
            color: rgba(255,255,255,0.4);
            margin-top: 12px;
            letter-spacing: 2px;
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
