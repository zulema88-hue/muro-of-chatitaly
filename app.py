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

st.set_page_config(page_title="Urban Graffiti Wall", layout="wide", initial_sidebar_state="collapsed")

def random_neon():
    # Colori brillanti: almeno una componente sopra 200
    r = random.randint(100, 255)
    g = random.randint(100, 255)
    b = random.randint(100, 255)
    return f"#{r:02x}{g:02x}{b:02x}"

# --- 2. CSS ---
st.markdown("""
    <style>
    header, footer, [data-testid="stSidebar"], [data-testid="stHeader"] { display: none !important; }
    .stApp {
        background-color: #050505;
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("https://www.transparenttextures.com/patterns/dark-brick-wall.png");
        background-attachment: fixed;
    }
    .graffiti-title {
        font-family: 'Rock Salt', cursive; text-align: center; color: white;
        font-size: 50px; padding: 20px; text-shadow: 2px 2px 0px #000, 0 0 20px #FF00FF;
    }
    .stForm { background: rgba(0,0,0,0.9) !important; border: 1px solid #444 !important; border-radius: 15px !important; }
    
    /* BOMBOLETTE */
    .can { width: 40px; height: 90px; border-radius: 6px; border: 2px solid #111; position: relative; }
    .mist { position: absolute; width: 120px; height: 120px; filter: blur(40px); opacity: 0.5; border-radius: 50%; }
    
    ::-webkit-scrollbar { width: 0px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INPUT ---
st.markdown('<div class="graffiti-title">CHATITALY URBAN WALL</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns([0.2, 0.6, 0.2])

with c1:
    st.markdown(f'<div style="position:relative; margin-left:auto;"><div class="mist" style="background:#00FFFF; top:-20px; left:-30px;"></div><div class="can" style="background:linear-gradient(#00FFFF, #005555); transform:rotate(-15deg); margin-left:auto;"></div></div>', unsafe_allow_html=True)

with c2:
    with st.form("bomb", clear_on_submit=True):
        col_tag, col_msg = st.columns([1, 2])
        nick = col_tag.text_input("TAG")
        txt = col_msg.text_area("MESSAGGIO")
        if st.form_submit_button("💨 BOMB THE WALL"):
            if txt.strip():
                l = len(txt)
                f, s = ("'Rock Salt'", 38) if l < 20 else ("'Permanent Marker'", 28) if l < 60 else ("'Gochi Hand'", 22)
                supabase.table("muro").insert({
                    "testo": txt, "autore": nick.upper() or "ANONIMO",
                    "colore": random_neon(), "font": f, "rotazione": random.randint(-8, 8), "font_size": s
                }).execute()
                st.rerun()

with c3:
    st.markdown(f'<div style="position:relative;"><div class="mist" style="background:#FF00FF; top:-20px; right:-30px;"></div><div class="can" style="background:linear-gradient(#FF00FF, #550055); transform:rotate(15deg);"></div></div>', unsafe_allow_html=True)

# --- 4. IL MURO (RANDOM & SPARPARGLIATO) ---
res = supabase.table("muro").select("*").order("id", desc=True).limit(50).execute()
messaggi = res.data

if messaggi:
    style = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Gochi+Hand&display=swap" rel="stylesheet">
    <style>
        .wall-container { 
            display: flex; 
            flex-wrap: wrap; 
            justify-content: space-around; 
            padding: 60px 20px; 
            width: 100%;
        }
        .graffito-box { 
            position: relative; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            margin: var(--m-top) var(--m-side);
            min-width: 300px;
            max-width: 500px;
        }
        .splat { 
            position: absolute; width: 220px; height: 220px; 
            filter: blur(60px); opacity: 0.25; z-index: 1; 
            top: 50%; left: 50%; transform: translate(-50%, -50%);
        }
        .text-main { 
            text-align: center; 
            z-index: 2; 
            /* Outline potente per nitidezza */
            text-shadow: 
                -2px -2px 0 #000,  
                 2px -2px 0 #000,
                -2px  2px 0 #000,
                 2px  2px 0 #000,
                 0 0 15px var(--c);
            font-weight: bold;
            line-height: 1.1;
        }
        .drip-line { width: 4px; height: 45px; margin-top: 5px; border-radius: 0 0 10px 10px; z-index: 2; }
    </style>
    """
    
    html = ""
    for m in messaggi:
        random.seed(m['id']) 
        # Colori e spostamenti randomici
        c_text = random_neon()
        c_splat = random_neon()
        m_top = f"{random.randint(20, 110)}px"
        m_side = f"{random.randint(10, 80)}px"
        
        rot = m.get('rotazione', 0)
        font = m.get('font', "'Permanent Marker'")
        size = m.get('font_size', 26)
        
        html += f'''
        <div class="graffito-box" style="--m-top: {m_top}; --m-side: {m_side}; --c: {c_text};">
            <div class="splat" style="background: {c_splat};"></div>
            <div class="text-main" style="color: {c_text}; font-family: {font}; font-size: {size}px; transform: rotate({rot}deg);">
                {m['testo'].replace("<","&lt;")}
            </div>
            <div class="drip-line" style="background: {c_text}; box-shadow: 0 0 10px {c_text};"></div>
            <div style="color: rgba(255,255,255,0.4); font-size: 10px; margin-top: 12px; font-family: sans-serif; letter-spacing:1px;">@{m['autore']}</div>
        </div>
        '''
    st.components.v1.html(f"{style}<div class='wall-container'>{html}</div>", height=4000, scrolling=False)

# --- 5. ADMIN ---
with st.expander("MOD"):
    if st.text_input("Psw", type="password") == "chatitaly123":
        for m in messaggi:
            if st.button(f"Elimina {m['id']}", key=f"del_{m['id']}"):
                supabase.table("muro").delete().eq("id", m['id']).execute()
                st.rerun()
