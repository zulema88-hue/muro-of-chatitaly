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

st.set_page_config(page_title="Urban Wall - Full Color", layout="wide", initial_sidebar_state="collapsed")

# Funzione per generare un colore neon veramente random
def random_neon():
    return f"#{random.randint(50, 255):02x}{random.randint(50, 255):02x}{random.randint(50, 255):02x}"

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
        font-size: 50px; padding: 20px; text-shadow: 0 0 20px #FF00FF;
    }
    .stForm { background: rgba(0,0,0,0.8) !important; border: 1px solid #444 !important; border-radius: 15px !important; }
    /* BOMBOLETTE */
    .can { width: 40px; height: 90px; border-radius: 6px; border: 2px solid #222; position: relative; }
    .mist { position: absolute; width: 100px; height: 100px; filter: blur(40px); opacity: 0.6; border-radius: 50%; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INPUT ---
st.markdown('<div class="graffiti-title">CHATITALY URBAN WALL</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns([0.2, 0.6, 0.2])

with c1: # Bomboletta sinistra
    st.markdown(f'<div style="position:relative; margin-left:auto;"><div class="mist" style="background:#00FFFF; top:-20px;"></div><div class="can" style="background:linear-gradient(#00FFFF, #005555); transform:rotate(-15deg);"></div></div>', unsafe_allow_html=True)

with c2:
    with st.form("bomb", clear_on_submit=True):
        col_tag, col_msg = st.columns([1, 2])
        nick = col_tag.text_input("TAG")
        txt = col_msg.text_area("MESSAGGIO")
        if st.form_submit_button("💨 BOMB THE WALL"):
            if txt.strip():
                # Salviamo un colore nel DB, ma il visualizzatore ne genererà comunque uno random se serve
                new_color = random_neon()
                l = len(txt)
                f, s = ("'Rock Salt'", 38) if l < 20 else ("'Permanent Marker'", 28) if l < 60 else ("'Gochi Hand'", 22)
                supabase.table("muro").insert({
                    "testo": txt, "autore": nick.upper() or "ANONIMO",
                    "colore": new_color, "font": f, "rotazione": random.randint(-10, 10), "font_size": s
                }).execute()
                st.rerun()

with c3: # Bomboletta destra
    st.markdown(f'<div style="position:relative;"><div class="mist" style="background:#FF00FF; top:-20px;"></div><div class="can" style="background:linear-gradient(#FF00FF, #550055); transform:rotate(15deg);"></div></div>', unsafe_allow_html=True)

# --- 4. IL MURO (FORZA RANDOM) ---
res = supabase.table("muro").select("*").order("id", desc=True).limit(50).execute()
messaggi = res.data

if messaggi:
    style = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Gochi+Hand&display=swap" rel="stylesheet">
    <style>
        .wall { display: flex; flex-wrap: wrap; justify-content: space-around; padding: 50px; }
        .item { position: relative; margin: 40px; display: flex; flex-direction: column; align-items: center; }
        .splat { position: absolute; width: 200px; height: 200px; filter: blur(60px); opacity: 0.3; z-index: 1; }
        .text { text-align: center; z-index: 2; text-shadow: 2px 2px 4px #000; font-weight: bold; }
        .drip { width: 4px; height: 40px; margin-top: 5px; border-radius: 0 0 10px 10px; z-index: 2; }
    </style>
    """
    
    html = ""
    for m in messaggi:
        # QUI LA MAGIA: Anche se il DB ha un colore vecchio, qui lo rimescoliamo usando l'ID come base
        random.seed(m['id']) 
        c_text = random_neon() # Colore testo unico
        c_splat = random_neon() # Colore spruzzo diverso dal testo
        
        rot = m.get('rotazione', 0)
        font = m.get('font', "'Permanent Marker'")
        size = m.get('font_size', 25)
        
        html += f'''
        <div class="item">
            <div class="splat" style="background: {c_splat};"></div>
            <div class="text" style="color: {c_text}; font-family: {font}; font-size: {size}px; transform: rotate({rot}deg); text-shadow: 0 0 10px {c_text};">
                {m['testo']}
            </div>
            <div class="drip" style="background: {c_text}; box-shadow: 0 0 10px {c_text};"></div>
            <div style="color: rgba(255,255,255,0.3); font-size: 10px; margin-top: 10px;">@{m['autore']}</div>
        </div>
        '''
    st.components.v1.html(f"{style}<div class='wall'>{html}</div>", height=3000)

# --- 5. MOD ---
with st.expander("MOD"):
    if st.text_input("Psw", type="password") == "chatitaly123":
        for m in messaggi:
            if st.button(f"Cancella {m['id']}"):
                supabase.table("muro").delete().eq("id", m['id']).execute()
                st.rerun()
