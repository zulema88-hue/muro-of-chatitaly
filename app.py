import streamlit as st
import random
from supabase import create_client

# --- CONNESSIONE ---
URL = "https://wumwurwuwoysrvutupde.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind1bXd1cnd1d295c3J2dXR1cGRlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc5NDgwMzIsImV4cCI6MjA4MzUyNDAzMn0.90s0KWQTOHb2fHdlgS4vvMNI-7iiDA-L0aR0qJ_5k7k"

@st.cache_resource
def init_connection():
    return create_client(URL, KEY)

supabase = init_connection()

st.set_page_config(page_title="Chatitaly Urban Wall", layout="wide", initial_sidebar_state="collapsed")

# --- CSS BASE ---
st.markdown("""
    <style>
    [data-testid="stSidebar"], .st-emotion-cache-10o1ihd, footer, header { display: none !important; }
    
    .stApp {
        background-image: url("https://static.vecteezy.com/system/resources/previews/007/233/624/non_2x/brick-black-wall-texture-background-dark-brickwork-pattern-block-stone-structure-backdrop-dark-brick-wall-realistic-template-abstract-modern-wallpaper-design-illustration-vector.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Titolo */
    .neon-title {
        font-family: sans-serif;
        text-align: center;
        color: white;
        text-shadow: 0 0 10px #FF00FF;
        font-size: 40px;
        font-weight: bold;
        padding: 20px;
        background: rgba(0,0,0,0.5);
    }

    /* Input Box più grandi per scrivere canzoni */
    .stTextArea textarea {
        background-color: rgba(0,0,0,0.8) !important;
        color: #00FFFF !important;
        border: 1px solid #555 !important;
        font-size: 16px;
    }
    .stTextInput input {
        background-color: rgba(0,0,0,0.8) !important;
        color: #39FF14 !important;
        border: 1px solid #555 !important;
    }
    </style>
    """, unsafe_allow_html=True)

def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).limit(50).execute()
        return res.data
    except: return []

def spruzza():
    t = st.session_state.get("input_testo", "")
    n = st.session_state.get("input_nick", "")
    
    if t and t.strip():
        lunghezza = len(t)
        
        # --- LOGICA INTELLIGENTE ---
        # Se il testo è lungo (> 50 caratteri), font piccolo e poca rotazione
        if lunghezza > 50:
            f_size = random.randint(16, 20) # Piccolo per le canzoni
            rot = random.randint(-2, 2)     # Quasi dritto per leggere meglio
            font_scelto = "'Patrick Hand', cursive" # Font leggibile
        # Se il testo è medio (20-50 caratteri)
        elif lunghezza > 20:
            f_size = random.randint(22, 28)
            rot = random.randint(-5, 5)
            font_scelto = "'Permanent Marker', cursive"
        # Se il testo è corto (un saluto veloce)
        else:
            f_size = random.randint(35, 50) # Grande!
            rot = random.randint(-10, 10)
            font_scelto = "'Rock Salt', cursive"

        data = {
            "testo": t, # Tolto .upper() per lasciare minuscole le canzoni se vuoi
            "autore": n.upper() if n.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF", "#FFA500"]),
            "font": font_scelto,
            "rotazione": rot,
            "font_size": f_size
        }
        try:
            supabase.table("muro").insert(data).execute()
            st.session_state["input_testo"] = "" # Pulisce il campo
        except: pass

# --- UI ---
st.markdown('<div class="neon-title">CHATITALY WALL</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.text_input("NICKNAME", key="input_nick", placeholder="Chi sei?")
    # Cambiato in TEXT AREA per permettere testi più lunghi e comodi
    st.text_area("SCRIVI QUI (Vai a capo per le canzoni)", key="input_testo", height=100, placeholder="Scrivi il tuo messaggio o incolla una canzone...")
    st.button("SPRUZZA SUL MURO", on_click=spruzza, use_container_width=True)

# --- VISUALIZZAZIONE MURO ---
messaggi = carica_messaggi()

if messaggi:
    # HTML Blindato
    html_muro = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Patrick+Hand&display=swap" rel="stylesheet">
    <style>
        body { margin: 0; padding: 0; background: transparent; }
        .wall-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            align-items: flex-start; /* Allinea in alto */
            gap: 20px;
            padding: 20px;
        }
        .graffiti-box {
            display: inline-block;
            padding: 15px;
            text-align: center;
            /* Ombra nera per staccare dal muro */
            filter: drop-shadow(4px 4px 2px rgba(0,0,0,0.9));
            /* Forza il testo ad andare a capo */
            max-width: 300px;
            word-wrap: break-word;
            white-space: pre-wrap; 
            line-height: 1.2;
        }
        .author {
            display: block;
            font-family: sans-serif;
            font-size: 10px;
            color: rgba(255,255,255,0.7);
            margin-top: 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
    </style>
    <div class="wall-container">
    """
    
    for m in messaggi:
        # Recupero dati
        txt = m.get('testo', '')
        # Sostituiamo gli a capo (\n) con <br> per l
