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

st.set_page_config(page_title="Wild Neon Wall", layout="wide", initial_sidebar_state="collapsed")

# --- 2. LOGICA RESET ---
def auto_reset_check():
    try:
        oggi = datetime.now().strftime("%Y-%m-%d")
        if st.session_state.get("last_check") != oggi:
            res = supabase.table("muro").select("created_at").order("id", desc=True).limit(1).execute()
            if res.data:
                data_ultimo_msg = res.data[0]['created_at'].split('T')[0]
                if data_ultimo_msg != oggi:
                    supabase.table("muro").delete().neq("id", 0).execute()
            st.session_state["last_check"] = oggi
    except: pass

auto_reset_check()

# --- 3. CSS CORE (WILD STYLE) ---
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

    .neon-title {
        font-family: 'Rock Salt', cursive;
        text-align: center;
        color: white;
        font-size: 35px;
        padding: 20px;
        text-shadow: 0 0 10px #FF00FF, 0 0 20px #00FFFF;
    }

    /* Form Clandestino */
    .stForm {
        background: rgba(0,0,0,0.8) !important;
        border: 2px solid #FF00FF !important;
        border-radius: 15px !important;
        position: relative;
        z-index: 9999;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. INPUT ---
st.markdown('<div class="neon-title">CHATITALY WILD NEON</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
with c2:
    with st.form("spray_form", clear_on_submit=True):
        col_n, col_m = st.columns([1, 2])
        nick = col_n.text_input("TAG", placeholder="Chi sei?")
        txt = col_m.text_area("MESSAGGIO", height=70, placeholder="Spruzza sul muro...")
        submitted = st.form_submit_button("💨 BOMB THE WALL!")

    if submitted and txt.strip():
        l = len(txt)
        # Dinamismo basato sulla lunghezza
        if l < 15: f_size, rot, font = random.randint(45, 65), random.randint(-20, 20), "'Rock Salt', cursive"
        elif l < 80: f_size, rot, font = random.randint(28, 38), random.randint(-10, 10), "'Permanent Marker', cursive"
        else: f_size, rot, font = random.randint(18, 24), random.randint(-5, 5), "'Patrick Hand', cursive"

        data = {
            "testo": txt, "autore": nick.upper() if nick.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF", "#00FF7F"]),
            "font": font, "rotazione": rot, "font_size": f_size
        }
        supabase.table("muro").insert(data).execute()
        st.rerun()

# --- 5. IL MURO SPARPARGLIATO ---
messaggi = carica_messaggi() if 'carica_messaggi' in locals() else []
# (Ridefinisco carica_messaggi per sicurezza)
try:
    res = supabase.table("muro").select("*").order("id", desc=True).limit(50).execute()
    messaggi = res.data
except: messaggi = []

if messaggi:
    style_block = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Patrick+Hand&display=swap" rel="stylesheet">
    <style>
        .wall-canvas {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            align-items: center;
            padding: 100px 50px;
            gap: 60px;
            width: 100%;
        }

        .graffito {
            position: relative;
            display: inline-block;
            white-space: pre-wrap;
            word-wrap: break-word;
            text-align: center;
            line-height: 1.1;
            /* Effetto NEON e SPRUZZO */
            filter: drop-shadow(0 0 8px var(--c-glow)) drop-shadow(4px 4px 2px rgba(0,0,0,0.8));
            transform: rotate(var(--r));
            margin: var(--m);
            transition: all 0.3s;
            /* Sicurezza contro linee dritte */
            min-width: 150px;
            max-width: 450px;
        }

        .graffito:hover {
            transform: scale(1.2) rotate(0deg) !important;
            z-index: 1000;
            filter: drop-shadow(0 0 20px var(--c-glow));
        }

        /* Macchie di spruzzo casuali (pseudo-elementi) */
        .graffito::before {
            content: '';
            position: absolute;
            top: -10px; left: -10px;
            width: 20px; height: 20px;
            background: var(--c-glow);
            border-radius: 50%;
            filter: blur(10px);
            opacity: 0.4;
        }

        /* Gocce (Drips) */
        .drip {
            position: absolute;
            top: 95%;
            left: var(--dl);
            width: 3px;
            height: var(--dh);
            background: var(--c-glow);
            border-radius: 0 0 3px 3px;
            opacity: 0.7;
        }

        .tag-signature {
            display: block;
            font-family: sans-serif;
            font-size: 10px;
            color: rgba(255,255,255,0.3);
            margin-top: 10px;
            text-transform: uppercase;
        }
    </style>
    """
    
    content_html = ""
    for i, m in enumerate(messaggi):
        # Generiamo caos controllato
        random.seed(m['id'])
        m_random = f"{random.randint(-40, 40)}px {random.randint(-40, 40)}px"
        drip_html = ""
        # Aggiungiamo gocce solo se il messaggio è corto
        if len(m['testo']) < 40 and random.random() > 0.5:
            for _ in range(random.randint(1, 2)):
                dl = random.randint(10, 90)
                dh = random.randint(20, 70)
                drip_html += f'<div class="drip" style="--dl: {dl}%; --dh: {dh}px;"></div>'

        content_html += f'''
        <div class="graffito" style="
            --c-glow: {m["colore"]}; 
            --r: {m["rotazione"]}deg; 
            --m: {m_random};
            color: {m["colore"]}; 
            font-family: {m["font"]}; 
            font-size: {m["font_size"]}px;">
            {m["testo"].replace("<","&lt;")}
            {drip_html}
            <span class="tag-signature">BY {m["autore"]}</span>
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
