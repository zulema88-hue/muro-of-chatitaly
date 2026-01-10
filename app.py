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

# Funzione per generare colori HEX casuali e vivaci
def get_random_neon_color():
    # Genera colori con alta saturazione per l'effetto neon
    r = lambda: random.randint(100, 255)
    return '#%02X%02X%02X' % (r(), r(), r())

# --- 2. CSS CORE ---
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
        text-shadow: 2px 2px 0px #000, 0 0 20px #FF00FF;
    }

    .can { width: 40px; height: 90px; border-radius: 6px; position: relative; border: 2px solid #222; }
    .can-left { background: linear-gradient(135deg, #00FFFF, #004444); }
    .can-right { background: linear-gradient(135deg, #FF00FF, #440044); }
    .can::before { content: ''; position: absolute; top: -10px; left: 50%; transform: translateX(-50%); width: 20px; height: 10px; background: #333; border-radius: 3px; }

    .mist { position: absolute; width: 150px; height: 150px; filter: blur(40px); opacity: 0.5; border-radius: 50%; z-index: 0; }
    .mist-left { background: #00FFFF; top: -50px; left: -50px; }
    .mist-right { background: #FF00FF; top: -50px; right: -50px; }

    .stForm { background: rgba(0, 0, 0, 0.85) !important; border: 1px solid #444 !important; border-radius: 15px !important; position: relative; z-index: 2; }
    ::-webkit-scrollbar { width: 0px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INPUT ---
st.markdown('<div class="graffiti-title">CHATITALY URBAN WALL</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns([0.15, 0.7, 0.15])

with c1:
    st.markdown('<div style="height:80px"></div><div style="position:relative"><div class="mist mist-left"></div><div class="can can-left" style="transform:rotate(-15deg); margin-left:auto"></div></div>', unsafe_allow_html=True)

with c2:
    with st.form("spray_form", clear_on_submit=True):
        col_n, col_m = st.columns([1, 2])
        nick = col_n.text_input("TAG", placeholder="Nickname")
        txt = col_m.text_area("MESSAGGIO", height=70, placeholder="Spruzza un colore a caso...")
        submitted = st.form_submit_button("💨 BOMB THE WALL")

    if submitted and txt.strip():
        l = len(txt)
        if l < 15: f_size, font = 38, "'Rock Salt', cursive"
        elif l < 60: f_size, font = 28, "'Permanent Marker', cursive"
        else: f_size, font = 24, "'Gochi Hand', cursive"

        # COLORE COMPLETAMENTE RANDOM PER OGNI MESSAGGIO
        color_choice = get_random_neon_color()
        
        data = {
            "testo": txt, "autore": nick.upper() if nick.strip() else "ANONIMO",
            "colore": color_choice,
            "font": font, "rotazione": random.randint(-10, 10), "font_size": f_size
        }
        supabase.table("muro").insert(data).execute()
        st.rerun()

with c3:
    st.markdown('<div style="height:80px"></div><div style="position:relative"><div class="mist mist-right"></div><div class="can can-right" style="transform:rotate(15deg); margin-right:auto"></div></div>', unsafe_allow_html=True)

# --- 4. IL MURO ---
try:
    res = supabase.table("muro").select("*").order("id", desc=True).limit(50).execute()
    messaggi = res.data
except:
    messaggi = []

if messaggi:
    style_block = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Gochi+Hand&display=swap" rel="stylesheet">
    <style>
        .wall-canvas { display: flex; flex-wrap: wrap; justify-content: space-around; align-items: center; padding: 60px 20px; width: 100%; }
        .graffito-item { position: relative; display: flex; flex-direction: column; align-items: center; margin: var(--m-top) var(--m-side); min-width: 250px; max-width: 450px; }
        
        .paint-splatter { 
            position: absolute; width: 220px; height: 220px; 
            background: var(--splat-c); filter: blur(70px); opacity: 0.3; z-index: 1; 
            top: 50%; left: 50%; transform: translate(-50%, -50%);
        }
        
        .text-neon { 
            text-align: center; line-height: 1.1; word-wrap: break-word; z-index: 2; 
            text-shadow: 2px 2px 4px #000, 0 0 12px var(--c); letter-spacing: -0.5px;
        }
        
        .drip { width: 3px; height: 45px; background: var(--c); margin-top: 5px; border-radius: 0 0 10px 10px; box-shadow: 0 0 10px var(--c); z-index: 2; }
        .author { font-family: sans-serif; font-size: 10px; color: rgba(255,255,255,0.4); text-transform: uppercase; margin-top: 10px; letter-spacing: 2px; }
    </style>
    """
    
    content_html = ""
    for m in messaggi:
        random.seed(m['id'])
        m_top = f"{random.randint(20, 120)}px"
        m_side = f"{random.randint(10, 100)}px"
        
        c = m.get("colore", "#FFFFFF")
        # Generiamo un colore per lo splatter leggermente diverso o complementare basato sul seed
        splat_c = get_random_neon_color() 
        
        content_html += f'''
        <div class="graffito-item" style="--m-top: {m_top}; --m-side: {m_side}; --c: {c}; --splat-c: {splat_c};">
            <div class="paint-splatter"></div>
            <div class="text-neon" style="color: {c}; font-family: {m["font"]}; font-size: {m["font_size"]}px; transform: rotate({m["rotazione"]}deg);">
                {m["testo"].replace("<","&lt;")}
            </div>
            <div class="drip"></div>
            <div class="author">@{m["autore"]}</div>
        </div>
        '''
    st.components.v1.html(f"{style_block}<div class='wall-canvas'>{content_html}</div>", height=4000, scrolling=False)

# --- 5. MOD ---
with st.expander("MOD"):
    if st.text_input("Psw", type="password") == "chatitaly123":
        for m in messaggi:
            ca, cb = st.columns([4,1])
            ca.write(f"{m['autore']}: {m['testo'][:20]}")
            if cb.button("🗑️", key=f"d_{m['id']}"):
                supabase.table("muro").delete().eq("id", m['id']).execute()
                st.rerun()
