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

# --- 2. CSS CORE (MURO + NEON) ---
st.markdown("""
    <style>
    [data-testid="stSidebar"], .st-emotion-cache-10o1ihd, footer, header { display: none !important; }
    
    /* SFONDO MURO DI MATTONI */
    .stApp {
        background-image: url("https://static.vecteezy.com/system/resources/previews/007/233/624/non_2x/brick-black-wall-texture-background-dark-brick-wall-realistic-template-abstract-modern-wallpaper-design-illustration-vector.jpg");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }

    ::-webkit-scrollbar { width: 0px; }
    * { scrollbar-width: none; }

    .wall-title {
        font-family: 'Rock Salt', cursive;
        text-align: center;
        color: white;
        font-size: 32px;
        padding: 20px;
        text-shadow: 0 0 10px #FF00FF, 0 0 20px #00FFFF;
    }

    /* Form Input - Trasparente per non coprire troppo il muro */
    .stForm {
        background: rgba(0,0,0,0.8) !important;
        border: 2px solid #39FF14 !important;
        border-radius: 15px !important;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FUNZIONI DATI ---
def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).limit(50).execute()
        return res.data
    except: return []

# --- 4. INTERFACCIA INPUT ---
st.markdown('<div class="wall-title">CHATITALY URBAN WALL</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
with c2:
    with st.form("spray_form", clear_on_submit=True):
        col_n, col_m = st.columns([1, 2])
        nick = col_n.text_input("TAG", placeholder="Chi sei?")
        txt = col_m.text_area("MESSAGGIO", height=70, placeholder="Spruzza la tua frase...")
        submitted = st.form_submit_button("💨 BOMB THE WALL!")

    if submitted and txt.strip():
        l = len(txt)
        if l < 10: f_size, rot, font = random.randint(45, 60), random.randint(-15, 15), "'Rock Salt', cursive"
        elif l < 60: f_size, rot, font = random.randint(28, 36), random.randint(-8, 8), "'Permanent Marker', cursive"
        else: f_size, rot, font = random.randint(18, 23), random.randint(-4, 4), "'Patrick Hand', cursive"

        data = {
            "testo": txt, "autore": nick.upper() if nick.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF", "#FFD700"]),
            "font": font, "rotazione": rot, "font_size": f_size
        }
        try:
            supabase.table("muro").insert(data).execute()
            st.rerun()
        except: st.rerun()

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
            padding: 50px;
            gap: 40px;
            width: 100%;
        }

        .graffito {
            position: relative;
            display: inline-block;
            text-align: center;
            white-space: pre-wrap;
            word-wrap: break-word;
            line-height: 1.1;
            /* NEON GLOW */
            color: var(--c);
            font-family: var(--f);
            font-size: var(--s);
            text-shadow: 0 0 5px var(--c), 0 0 15px var(--c), 2px 2px 2px rgba(0,0,0,0.9);
            transform: rotate(var(--r));
            margin: var(--m);
            min-width: 180px;
            max-width: 450px;
            transition: transform 0.3s;
        }

        .graffito:hover {
            transform: scale(1.1) rotate(0deg) !important;
            z-index: 99;
        }

        .tag {
            display: block;
            font-family: sans-serif;
            font-size: 10px;
            color: rgba(255,255,255,0.3);
            margin-top: 8px;
            text-shadow: none;
            letter-spacing: 1px;
        }
    </style>
    """
    
    content_html = ""
    for m in messaggi:
        random.seed(m['id'])
        rand_m = f"{random.randint(-20, 20)}px {random.randint(-20, 20)}px"
        
        content_html += f'''
        <div class="graffito" style="
            --c: {m["colore"]}; 
            --r: {m["rotazione"]}deg; 
            --s: {m["font_size"]}px;
            --f: {m["font"]};
            --m: {rand_m};">
            {m["testo"].replace("<","&lt;")}
            <span class="tag">@{m["autore"]}</span>
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
