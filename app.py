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

st.set_page_config(page_title="Urban Wall", layout="wide", initial_sidebar_state="collapsed")

def get_vibrant_color():
    palette = ["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF", "#FFD700", "#FF4500", "#7B68EE", "#FF1493", "#00FF7F"]
    return random.choice(palette)

# --- 2. CSS TOTALE ---
st.markdown("""
    <style>
    header, footer, [data-testid="stSidebar"], [data-testid="stHeader"] { display: none !important; }
    
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden;
        scrollbar-width: none;
    }
    html::-webkit-scrollbar, body::-webkit-scrollbar { display: none; }

    .stApp {
        background-color: #050505;
        background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("https://www.transparenttextures.com/patterns/dark-brick-wall.png");
        background-attachment: fixed;
    }

    .graffiti-title {
        font-family: 'Rock Salt', cursive; text-align: center; color: white;
        font-size: clamp(30px, 5vw, 45px); padding: 20px; text-shadow: 0 0 15px #FF00FF;
    }

    .stForm { background: rgba(0,0,0,0.85) !important; border: 1px solid #333 !important; border-radius: 15px !important; }

    /* BOMBOLETTE STYLE */
    .can { width: 40px; height: 90px; border-radius: 6px; border: 2px solid #222; position: relative; box-shadow: 5px 5px 15px rgba(0,0,0,0.5); }
    .can-cyan { background: linear-gradient(135deg, #00FFFF, #008888); }
    .can-pink { background: linear-gradient(135deg, #FF00FF, #880088); }
    .can::before { content: ''; position: absolute; top: -10px; left: 50%; transform: translateX(-50%); width: 20px; height: 10px; background: #333; border-radius: 3px; }
    .mist { position: absolute; width: 120px; height: 120px; filter: blur(40px); opacity: 0.4; border-radius: 50%; z-index: 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INPUT E BOMBOLETTE ---
st.markdown('<div class="graffiti-title">CHATITALY URBAN WALL</div>', unsafe_allow_html=True)

col_sx, col_main, col_dx = st.columns([0.2, 0.6, 0.2])

with col_sx:
    st.markdown('<div style="height:50px"></div><div style="position:relative; display: flex; justify-content: flex-end;"><div class="mist" style="background:#00FFFF; top:-20px; right:0;"></div><div class="can can-cyan" style="transform:rotate(-15deg);"></div></div>', unsafe_allow_html=True)

with col_main:
    with st.form("bomb", clear_on_submit=True):
        col_tag, col_msg = st.columns([1, 2])
        nick = col_tag.text_input("TAG", placeholder="Il tuo nome")
        txt = col_msg.text_area("MESSAGGIO", placeholder="Scrivi sul muro...")
        if st.form_submit_button("💨 BOMB THE WALL"):
            if txt.strip():
                l = len(txt)
                f, s = ("'Rock Salt'", 36) if l < 20 else ("'Permanent Marker'", 26) if l < 60 else ("'Gochi Hand'", 22)
                supabase.table("muro").insert({
                    "testo": txt, "autore": nick.upper() or "ANONIMO",
                    "colore": get_vibrant_color(), "font": f, "rotazione": random.randint(-5, 5), "font_size": s
                }).execute()
                st.rerun()

with col_dx:
    st.markdown('<div style="height:50px"></div><div style="position:relative; display: flex; justify-content: flex-start;"><div class="mist" style="background:#FF00FF; top:-20px; left:0;"></div><div class="can can-pink" style="transform:rotate(15deg);"></div></div>', unsafe_allow_html=True)

# --- 4. IL MURO ---
res = supabase.table("muro").select("*").order("id", desc=True).limit(60).execute()
messaggi = res.data

if messaggi:
    style = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Gochi+Hand&display=swap" rel="stylesheet">
    <style>
        ::-webkit-scrollbar { display: none; }
        * { scrollbar-width: none; }
        .wall-grid { 
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 35px;
            padding: 40px;
        }
        .graffito-card { 
            position: relative; display: flex; flex-direction: column; align-items: center;
            padding: 20px; margin: var(--m);
        }
        .splat { 
            position: absolute; width: 160px; height: 160px; 
            filter: blur(55px); opacity: 0.25; z-index: 1; background: var(--c);
        }
        .text-spray { 
            text-align: center; z-index: 2; 
            text-shadow: 1px 1px 3px rgba(0,0,0,0.9), 0 0 12px var(--c);
            line-height: 1.1; word-wrap: break-word;
        }
        .drip { width: 3px; height: 35px; margin-top: 5px; border-radius: 0 0 10px 10px; z-index: 2; opacity: 0.8; background: var(--c); box-shadow: 0 0 8px var(--c); }
        .tag { color: rgba(255,255,255,0.4); font-size: 11px; margin-top: 8px; font-family: sans-serif; font-weight: bold; }
    </style>
    """
    
    html_content = ""
    for m in messaggi:
        c = get_vibrant_color() 
        random.seed(m['id'])
        m_rand = f"{random.randint(5,25)}px"
        rot = random.randint(-6, 6)
        
        html_content += f'''
        <div class="graffito-card" style="--c: {c}; --m: {m_rand};">
            <div class="splat"></div>
            <div class="text-spray" style="color: {c}; font-family: {m['font']}; font-size: {m['font_size']}px; transform: rotate({rot}deg);">
                {m['testo'].replace("<","&lt;")}
            </div>
            <div class="drip" style="--c: {c};"></div>
            <div class="tag">@{m['autore']}</div>
        </div>
        '''
    
    st.components.v1.html(f"{style}<div class='wall-grid'>{html_content}</div>", height=3000, scrolling=True)

# --- 5. MOD ---
with st.expander("MOD"):
    if st.text_input("Psw", type="password") == "chatitaly123":
        for m in messaggi:
            if st.button(f"Elimina {m['id']}", key=f"d_{m['id']}"):
                supabase.table("muro").delete().eq("id", m['id']).execute()
                st.rerun()
