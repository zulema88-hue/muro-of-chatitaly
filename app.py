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

# --- 2. CSS CORE (FIX SFONDO MATTONI) ---
st.markdown("""
    <style>
    /* Rimuove interfacce standard di Streamlit */
    [data-testid="stSidebar"], .st-emotion-cache-10o1ihd, footer, header { display: none !important; }
    
    /* FORZA SFONDO SU TUTTI I LIVELLI */
    .stApp, .main, .st-emotion-cache-z5fcl4 {
        background: url("https://static.vecteezy.com/system/resources/previews/007/233/624/non_2x/brick-black-wall-texture-background-dark-brick-wall-realistic-template-abstract-modern-wallpaper-design-illustration-vector.jpg") no-repeat center center fixed !important;
        background-size: cover !important;
    }

    /* Overlay scuro per migliorare il contrasto neon */
    .main::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.4);
        z-index: -1;
    }

    ::-webkit-scrollbar { width: 0px; }
    
    .wall-title {
        font-family: 'Rock Salt', cursive;
        text-align: center;
        color: white;
        font-size: 35px;
        padding: 30px 0;
        text-shadow: 0 0 15px #FF00FF, 0 0 30px #00FFFF;
    }

    .stForm {
        background: rgba(0,0,0,0.7) !important;
        border: 2px solid #00FFFF !important;
        border-radius: 15px !important;
        backdrop-filter: blur(5px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATI ---
def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).limit(50).execute()
        return res.data
    except: return []

# --- 4. INPUT ---
st.markdown('<div class="wall-title">CHATITALY URBAN WALL</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
with c2:
    with st.form("spray_form", clear_on_submit=True):
        col_n, col_m = st.columns([1, 2])
        nick = col_n.text_input("TAG", placeholder="Chi sei?")
        txt = col_m.text_area("MESSAGGIO", height=70, placeholder="Cosa vuoi scrivere sul muro?")
        submitted = st.form_submit_button("💨 BOMB THE WALL!")

    if submitted and txt.strip():
        l = len(txt)
        if l < 10: f_size, rot, font = random.randint(45, 60), random.randint(-18, 18), "'Rock Salt', cursive"
        elif l < 60: f_size, rot, font = random.randint(28, 36), random.randint(-10, 10), "'Permanent Marker', cursive"
        else: f_size, rot, font = random.randint(18, 24), random.randint(-5, 5), "'Patrick Hand', cursive"

        data = {
            "testo": txt, "autore": nick.upper() if nick.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF", "#FFD700"]),
            "font": font, "rotazione": rot, "font_size": f_size
        }
        try:
            supabase.table("muro").insert(data).execute()
            st.rerun()
        except: pass

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
            padding: 40px;
            gap: 60px;
            width: 100%;
            background: transparent !important;
        }

        .graffito {
            position: relative;
            display: inline-block;
            text-align: center;
            white-space: pre-wrap;
            word-wrap: break-word;
            line-height: 1.2;
            color: var(--c);
            font-family: var(--f);
            font-size: var(--s);
            /* Effetto Neon Spray */
            text-shadow: 0 0 10px var(--c), 0 0 20px var(--c), 3px 3px 2px rgba(0,0,0,0.9);
            transform: rotate(var(--r));
            margin: var(--m);
            min-width: 180px;
            max-width: 450px;
            transition: transform 0.2s;
        }

        .tag-signature {
            display: block;
            font-family: sans-serif;
            font-size: 10px;
            color: rgba(255,255,255,0.4);
            margin-top: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
            text-shadow: none;
        }
    </style>
    """
    
    content_html = ""
    for m in messaggi:
        random.seed(m['id'])
        rand_m = f"{random.randint(-30, 30)}px {random.randint(-20, 20)}px"
        
        content_html += f'''
        <div class="graffito" style="
            --c: {m["colore"]}; 
            --r: {m["rotazione"]}deg; 
            --s: {m["font_size"]}px;
            --f: {m["font"]};
            --m: {rand_m};">
            {m["testo"].replace("<","&lt;")}
            <span class="tag-signature">@{m["autore"]}</span>
        </div>
        '''
    
    st.components.v1.html(f"{style_block}<div class='wall-canvas'>{content_html}</div>", height=2000, scrolling=False)

# --- 6. ADMIN ---
with st.expander("MOD"):
    if st.text_input("Psw", type="password") == "chatitaly123":
        for m in messaggi:
            col_a, col_b = st.columns([4,1])
            col_a.write(f"{m['autore']}: {m['testo'][:20]}")
            if col_b.button("🗑️", key=f"d_{m['id']}"):
                supabase.table("muro").delete().eq("id", m['id']).execute()
                st.rerun()
