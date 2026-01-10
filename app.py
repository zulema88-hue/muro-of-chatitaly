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

st.set_page_config(page_title="Urban Neon Wall", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS CORE (EFFETTO NEON SENZA GOCCE) ---
st.markdown("""
    <style>
    [data-testid="stSidebar"], .st-emotion-cache-10o1ihd, footer, header { display: none !important; }
    
    .stApp {
        background-image: url("https://static.vecteezy.com/system/resources/previews/007/233/624/non_2x/brick-black-wall-texture-background-dark-brick-wall-realistic-template-abstract-modern-wallpaper-design-illustration-vector.jpg");
        background-size: cover;
        background-attachment: fixed;
    }

    ::-webkit-scrollbar { width: 0px; }
    * { scrollbar-width: none; }

    .wall-title {
        font-family: 'Rock Salt', cursive;
        text-align: center;
        color: white;
        font-size: clamp(24px, 5vw, 40px);
        padding: 20px;
        text-shadow: 0 0 10px #FF00FF, 0 0 20px #00FFFF;
    }

    /* Form Input */
    .stForm {
        background: rgba(0,0,0,0.85) !important;
        border: 2px solid #00FFFF !important;
        border-radius: 15px !important;
        z-index: 999;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGICA DATI ---
def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).limit(50).execute()
        return res.data
    except: return []

# --- 4. INTERFACCIA ---
st.markdown('<div class="wall-title">CHATITALY URBAN WALL</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
with c2:
    with st.form("clean_spray", clear_on_submit=True):
        col_n, col_m = st.columns([1, 2])
        nick = col_n.text_input("TAG", placeholder="Tuo Nome")
        txt = col_m.text_area("MESSAGGIO", height=70, placeholder="Cosa vuoi gridare al mondo?")
        submitted = st.form_submit_button("💨 SPRUZZA SUL MURO")

    if submitted and txt.strip():
        l = len(txt)
        # Font e dimensioni dinamiche
        if l < 10: f_size, rot, font = random.randint(40, 55), random.randint(-15, 15), "'Rock Salt', cursive"
        elif l < 60: f_size, rot, font = random.randint(26, 34), random.randint(-8, 8), "'Permanent Marker', cursive"
        else: f_size, rot, font = random.randint(18, 22), random.randint(-4, 4), "'Patrick Hand', cursive"

        data = {
            "testo": txt, "autore": nick.upper() if nick.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF", "#00FF7F"]),
            "font": font, "rotazione": rot, "font_size": f_size
        }
        supabase.table("muro").insert(data).execute()
        st.rerun()

# --- 5. IL MURO SPARPARGLIATO ---
messaggi = carica_messaggi()
if messaggi:
    style_block = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Patrick+Hand&display=swap" rel="stylesheet">
    <style>
        .wall-canvas {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            align-items: center;
            padding: 80px 40px;
            gap: 50px;
            width: 100%;
        }

        .graffito {
            position: relative;
            display: inline-block;
            text-align: center;
            white-space: pre-wrap;
            word-wrap: break-word;
            line-height: 1.2;
            /* EFFETTO NEON INTENSO */
            text-shadow: 0 0 10px var(--c), 0 0 20px var(--c), 2px 2px 2px rgba(0,0,0,0.8);
            transform: rotate(var(--r));
            transition: all 0.3s ease;
            /* Protezione leggibilità */
            min-width: 180px;
            max-width: 400px;
            margin: var(--rand-m);
        }

        .graffito:hover {
            transform: scale(1.15) rotate(0deg) !important;
            z-index: 100;
            cursor: default;
        }

        .author {
            display: block;
            font-family: sans-serif;
            font-size: 10px;
            color: rgba(255,255,255,0.4);
            margin-top: 10px;
            text-transform: uppercase;
            text-shadow: none;
        }
    </style>
    """
    
    content_html = ""
    for m in messaggi:
        random.seed(m['id'])
        # Spostamenti casuali per ogni graffito
        rand_m = f"{random.randint(-30, 30)}px {random.randint(-20, 20)}px"
        
        content_html += f'''
        <div class="graffito" style="
            --c: {m["colore"]}; 
            --r: {m["rotazione"]}deg; 
            --rand-m: {rand_m};
            color: {m["colore"]}; 
            font-family: {m["font"]}; 
            font-size: {m["font_size"]}px;">
            {m["testo"].replace("<","&lt;")}
            <span class="author">BY {m["autore"]}</span>
        </div>
        '''
    
    st.components.v1.html(f"{style_block}<div class='wall-canvas'>{content_html}</div>", height=2500, scrolling=False)

# --- 6. ADMIN ---
with st.expander("MOD"):
    if st.text_input("Psw", type="password") == "chatitaly123":
        for m in messaggi:
            col_a, col_b = st.columns([4,1])
            col_a.write(f"{m['autore']}: {m['testo'][:20]}")
            if col_b.button("🗑️", key=f"d_{m['id']}"):
                supabase.table("muro").delete().eq("id", m['id']).execute()
                st.rerun()
