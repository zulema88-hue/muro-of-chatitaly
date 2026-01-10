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
    return f"#{random.randint(100, 255):02x}{random.randint(100, 255):02x}{random.randint(100, 255):02x}"

# --- 2. CSS ---
st.markdown("""
    <style>
    header, footer, [data-testid="stSidebar"], [data-testid="stHeader"] { display: none !important; }
    .stApp {
        background-color: #050505;
        background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("https://www.transparenttextures.com/patterns/dark-brick-wall.png");
        background-attachment: fixed;
    }
    .graffiti-title {
        font-family: 'Rock Salt', cursive; text-align: center; color: white;
        font-size: 45px; padding: 15px; text-shadow: 2px 2px 0px #000, 0 0 20px #FF00FF;
    }
    .stForm { background: rgba(0,0,0,0.9) !important; border: 1px solid #444 !important; border-radius: 15px !important; z-index: 999; position: relative; }
    
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
                f, s = ("'Rock Salt'", 40) if l < 20 else ("'Permanent Marker'", 30) if l < 60 else ("'Gochi Hand'", 24)
                supabase.table("muro").insert({
                    "testo": txt, "autore": nick.upper() or "ANONIMO",
                    "colore": random_neon(), "font": f, "rotazione": random.randint(-15, 15), "font_size": s
                }).execute()
                st.rerun()

with c3:
    st.markdown(f'<div style="position:relative;"><div class="mist" style="background:#FF00FF; top:-20px; right:-30px;"></div><div class="can" style="background:linear-gradient(#FF00FF, #550055); transform:rotate(15deg);"></div></div>', unsafe_allow_html=True)

# --- 4. IL MURO DINAMICO ---
# Carichiamo fino a 100 messaggi per fare volume
res = supabase.table("muro").select("*").order("id", desc=True).limit(100).execute()
messaggi = res.data

if messaggi:
    style = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Gochi+Hand&display=swap" rel="stylesheet">
    <style>
        .wall-area { 
            position: relative; 
            width: 100%; 
            height: 2500px; /* Altezza fissa per permettere coordinate Y ampie */
            overflow: hidden;
            margin-top: 50px;
        }
        .graffito-sticker { 
            position: absolute; /* POSIZIONAMENTO RANDOM VERO */
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            z-index: 2;
            transition: transform 0.3s;
        }
        .graffito-sticker:hover { z-index: 100; transform: scale(1.1); } /* Torna in primo piano se passi sopra */
        
        .splat-bg { 
            position: absolute; width: 250px; height: 250px; 
            filter: blur(70px); opacity: 0.3; z-index: -1; 
            top: 50%; left: 50%; transform: translate(-50%, -50%);
        }
        .text-neon { 
            text-align: center; 
            text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000, 0 0 15px var(--c);
            line-height: 1;
            white-space: pre-wrap;
            max-width: 400px;
        }
        .drip-line { width: 5px; height: 50px; margin-top: -5px; border-radius: 0 0 10px 10px; z-index: 1; opacity: 0.8; }
    </style>
    """
    
    html_elements = ""
    for m in messaggi:
        random.seed(m['id']) 
        # Calcoliamo posizione X (0-80%) e Y (0-90%) basata sull'ID
        pos_x = random.randint(5, 75)
        pos_y = random.randint(2, 95)
        
        c_text = random_neon()
        c_splat = random_neon()
        rot = m.get('rotazione', random.randint(-15, 15))
        font = m.get('font', "'Permanent Marker'")
        size = m.get('font_size', 28)
        
        html_elements += f'''
        <div class="graffito-sticker" style="left: {pos_x}%; top: {pos_y}%; --c: {c_text};">
            <div class="splat-bg" style="background: {c_splat};"></div>
            <div class="text-neon" style="color: {c_text}; font-family: {font}; font-size: {size}px; transform: rotate({rot}deg);">
                {m['testo'].replace("<","&lt;")}
            </div>
            <div class="drip-line" style="background: {c_text}; box-shadow: 0 0 12px {c_text};"></div>
            <div style="color: rgba(255,255,255,0.4); font-size: 11px; margin-top: 5px; font-family: sans-serif; font-weight: bold;">@{m['autore']}</div>
        </div>
        '''
    
    st.components.v1.html(f"{style}<div class='wall-area'>{html_elements}</div>", height=2500, scrolling=False)

# --- 5. ADMIN ---
with st.expander("MODERAZIONE"):
    if st.text_input("Psw", type="password") == "chatitaly123":
        for m in messaggi:
            col_a, col_b = st.columns([4,1])
            col_a.write(f"ID {m['id']} - {m['autore']}: {m['testo'][:30]}")
            if col_b.button("🗑️", key=f"del_{m['id']}"):
                supabase.table("muro").delete().eq("id", m['id']).execute()
                st.rerun()
