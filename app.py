import streamlit as st
import random
from datetime import datetime
from supabase import create_client

# --- 1. CONNESSIONE SUPABASE ---
URL = "https://wumwurwuwoysrvutupde.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind1bXd1cnd1d295c3J2dXR1cGRlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc5NDgwMzIsImV4cCI6MjA4MzUyNDAzMn0.90s0KWQTOHb2fHdlgS4vvMNI-7iiDA-L0aR0qJ_5k7k"

@st.cache_resource
def init_connection():
    return create_client(URL, KEY)

supabase = init_connection()

st.set_page_config(page_title="Urban Graffiti Wall", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS AVANZATO (BOMBOLETTE COLORATE + SPRUZZO) ---
st.markdown("""
    <style>
    header, footer, [data-testid="stSidebar"], [data-testid="stHeader"] { display: none !important; }

    .stApp {
        background-color: #050505;
        background-image: 
            linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)),
            url("https://www.transparenttextures.com/patterns/dark-brick-wall.png");
        background-attachment: fixed;
    }

    .graffiti-title {
        font-family: 'Rock Salt', cursive;
        text-align: center;
        color: #FFFFFF;
        font-size: clamp(35px, 7vw, 60px);
        padding: 20px 0;
        text-shadow: 2px 2px 0px #000, 0 0 15px #00FFFF;
    }

    /* BOMBOLETTE CSS COLORATE */
    .spray-wrapper {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
    }

    .can {
        width: 40px;
        height: 90px;
        border-radius: 6px;
        position: relative;
        border: 2px solid #222;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.8);
    }
    
    .can-cyan { background: linear-gradient(135deg, #00FFFF, #008888); }
    .can-pink { background: linear-gradient(135deg, #FF00FF, #880088); }

    /* Cappuccio ed Erogatore */
    .can::before {
        content: ''; position: absolute; top: -10px; left: 50%;
        transform: translateX(-50%); width: 20px; height: 10px;
        background: #333; border-radius: 3px;
    }

    /* EFFETTO SPRUZZO (Cloud) */
    .mist {
        position: absolute;
        width: 120px;
        height: 120px;
        filter: blur(35px);
        opacity: 0.4;
        border-radius: 50%;
        z-index: 0;
    }
    .mist-left { background: #00FFFF; top: -40px; left: -40px; }
    .mist-right { background: #FF00FF; top: -40px; right: -40px; }

    .stForm {
        background: rgba(0, 0, 0, 0.8) !important;
        border: 1px solid #444 !important;
        border-radius: 15px !important;
        position: relative;
        z-index: 2;
    }

    ::-webkit-scrollbar { width: 0px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INPUT ---
st.markdown('<div class="graffiti-title">CHATITALY URBAN WALL</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([0.15, 0.7, 0.15])

with c1:
    st.markdown('<div style="height:80px"></div><div style="position:relative"><div class="mist mist-left"></div><div class="can can-cyan" style="transform:rotate(-15deg); margin-left:auto"></div></div>', unsafe_allow_html=True)

with c2:
    with st.form("spray_form", clear_on_submit=True):
        col_n, col_m = st.columns([1, 2])
        nick = col_n.text_input("TAG", placeholder="Nickname")
        txt = col_m.text_area("MESSAGGIO", height=70, placeholder="Spruzza qualcosa...")
        submitted = st.form_submit_button("💨 BOMB THE WALL")

    if submitted and txt.strip():
        l = len(txt)
        if l < 15: f_size, font = 34, "'Rock Salt', cursive"
        elif l < 60: f_size, font = 26, "'Permanent Marker', cursive"
        else: f_size, font = 20, "'Patrick Hand', cursive"

        data = {
            "testo": txt, "autore": nick.upper() if nick.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF"]),
            "font": font, "rotazione": random.randint(-4, 4), "font_size": f_size
        }
        supabase.table("muro").insert(data).execute()
        st.rerun()

with c3:
    st.markdown('<div style="height:80px"></div><div style="position:relative"><div class="mist mist-right"></div><div class="can can-pink" style="transform:rotate(15deg); margin-right:auto"></div></div>', unsafe_allow_html=True)

# --- 4. IL MURO ---
res = supabase.table("muro").select("*").order("id", desc=True).limit(40).execute()
messaggi = res.data

if messaggi:
    style_block = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Patrick+Hand&display=swap" rel="stylesheet">
    <style>
        .wall-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 50px; padding: 40px; justify-items: center; }
        .graffito-container { position: relative; width: 100%; min-height: 200px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .paint-splatter { position: absolute; width: 140px; height: 140px; background: var(--c); filter: blur(50px); opacity: 0.2; z-index: 1; }
        .text-neon { text-align: center; line-height: 1.2; word-wrap: break-word; width: 90%; z-index: 2; text-shadow: 1px 1px 2px #000, 0 0 10px var(--c); }
        .drip { width: 3px; height: 35px; background: var(--c); margin-top: 10px; border-radius: 0 0 10px 10px; box-shadow: 0 0 10px var(--c); z-index: 2; }
        .author { font-family: sans-serif; font-size: 10px; color: rgba(255,255,255,0.4); text-transform: uppercase; margin-top: 10px; letter-spacing: 2px; }
    </style>
    """
    
    content_html = ""
    for m in messaggi:
        random.seed(m['id'])
        s_top, s_left = f"{random.randint(10, 50)}%", f"{random.randint(20, 60)}%"
        content_html += f'''
        <div class="graffito-container">
            <div class="paint-splatter" style="--c: {m["colore"]}; top: {s_top}; left: {s_left};"></div>
            <div class="text-neon" style="color: {m["colore"]}; font-family: {m["font"]}; font-size: {m["font_size"]}px; --c: {m["colore"]}; transform: rotate({m["rotazione"]}deg);">
                {m["testo"].replace("<","&lt;")}
            </div>
            <div class="drip" style="--c: {m["colore"]};"></div>
            <div class="author">@{m["autore"]}</div>
        </div>
        '''
    st.components.v1.html(f"{style_block}<div class='wall-grid'>{content_html}</div>", height=2000, scrolling=False)

# --- 5. ADMIN ---
with st.expander("MOD"):
    if st.text_input("Psw", type="password") == "chatitaly123":
        for m in messaggi:
            ca, cb = st.columns([4,1])
            ca.write(f"{m['autore']}: {m['testo'][:20]}")
            if cb.button("🗑️", key=f"d_{m['id']}"):
                supabase.table("muro").delete().eq("id", m['id']).execute()
                st.rerun()
