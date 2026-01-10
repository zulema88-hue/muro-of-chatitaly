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

# --- 2. CSS BLINDATO (NUOVO MURO DEFINITO) ---
# Immagine scelta da te: più nitida e scura
MURO_URL = "https://img.freepik.com/free-vector/dark-wall-background_1390-191.jpg?semt=ais_hybrid&w=740&q=80"

st.markdown(f"""
    <style>
    header, footer, [data-testid="stSidebar"], [data-testid="stHeader"] {{ display: none !important; }}

    /* FORZA IL MURO SU TUTTA L'APP */
    .stApp, [data-testid="stAppViewContainer"] {{
        background-image: url("{MURO_URL}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        background-repeat: no-repeat !important;
    }}

    /* TRASPARENZA TOTALE PER FAR VEDERE IL MURO */
    .main, [data-testid="stVerticalBlock"], .st-emotion-cache-1y4p8pa, .st-emotion-cache-z5fcl4 {{
        background-color: transparent !important;
    }}

    .wall-title {{
        font-family: 'Rock Salt', cursive;
        text-align: center;
        color: white;
        font-size: clamp(24px, 6vw, 40px);
        padding: 30px 0;
        text-shadow: 0 0 10px #FF00FF, 0 0 25px #00FFFF;
    }}

    /* Form Input */
    .stForm {{
        background: rgba(0,0,0,0.7) !important;
        border: 2px solid #00FFFF !important;
        border-radius: 12px !important;
        backdrop-filter: blur(8px);
    }}
    
    ::-webkit-scrollbar {{ width: 0px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. CARICAMENTO DATI ---
def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).limit(50).execute()
        return res.data
    except: return []

# --- 4. INPUT ---
st.markdown('<div class="wall-title">CHATITALY URBAN WALL</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
with c2:
    with st.form("clean_spray", clear_on_submit=True):
        col_n, col_m = st.columns([1, 2])
        nick = col_n.text_input("TAG", placeholder="Chi sei?")
        txt = col_m.text_area("MESSAGGIO", height=70, placeholder="Cosa scriveresti qui?")
        submitted = st.form_submit_button("💨 BOMB THE WALL!")

    if submitted and txt.strip():
        l = len(txt)
        if l < 15: f_size, rot, font = random.randint(42, 58), random.randint(-12, 12), "'Rock Salt', cursive"
        elif l < 70: f_size, rot, font = random.randint(26, 32), random.randint(-6, 6), "'Permanent Marker', cursive"
        else: f_size, rot, font = random.randint(18, 22), random.randint(-3, 3), "'Patrick Hand', cursive"

        data = {
            "testo": txt, "autore": nick.upper() if nick.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF", "#00FF7F"]),
            "font": font, "rotazione": rot, "font_size": f_size
        }
        supabase.table("muro").insert(data).execute()
        st.rerun()

# --- 5. IL MURO (NEON NITIDO) ---
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
            padding: 40px 20px;
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
            color: var(--c);
            font-family: var(--f);
            font-size: var(--s);
            /* NEON PIÙ DEFINITO */
            text-shadow: 0 0 12px var(--c), 2px 2px 4px rgba(0,0,0,0.9);
            transform: rotate(var(--r));
            margin: var(--m);
            min-width: 160px;
            max-width: 420px;
            transition: transform 0.3s;
        }

        .signature {
            display: block;
            font-family: sans-serif;
            font-size: 10px;
            color: rgba(255,255,255,0.4);
            margin-top: 8px;
            text-transform: uppercase;
            text-shadow: none !important;
        }
    </style>
    """
    
    content_html = ""
    for m in messaggi:
        random.seed(m['id'])
        # Meno caos nei margini per evitare scritte "rotte"
        rand_m = f"{random.randint(-15, 15)}px {random.randint(-10, 10)}px"
        
        content_html += f'''
        <div class="graffito" style="
            --c: {m["colore"]}; 
            --r: {m["rotazione"]}deg; 
            --s: {m["font_size"]}px;
            --f: {m["font"]};
            --m: {rand_m};">
            {m["testo"].replace("<","&lt;")}
            <span class="signature">@{m["autore"]}</span>
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
