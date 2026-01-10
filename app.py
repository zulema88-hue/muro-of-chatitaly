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

st.set_page_config(page_title="Urban Wall Pro", layout="wide", initial_sidebar_state="collapsed")

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

# --- 3. CSS CORE + EFFETTI SPECIALI ---
st.markdown("""
    <style>
    [data-testid="stSidebar"], .st-emotion-cache-10o1ihd, footer, header { display: none !important; }
    .stApp {
        background-image: url("https://static.vecteezy.com/system/resources/previews/007/233/624/non_2x/brick-black-wall-texture-background-dark-brickwork-pattern-block-stone-structure-backdrop-dark-brick-wall-realistic-template-abstract-modern-wallpaper-design-illustration-vector.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Titolo Neon Flicker */
    @keyframes flicker {
        0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% { text-shadow: 0 0 10px #FF00FF, 0 0 20px #FF00FF; }
        20%, 22%, 24%, 55% { text-shadow: none; opacity: 0.8; }
    }

    .neon-header {
        font-family: 'Rock Salt', cursive;
        text-align: center;
        color: #fff;
        animation: flicker 3s infinite;
        font-size: 35px;
        padding: 10px;
    }
    
    .stForm {
        background: rgba(0,0,0,0.85) !important;
        border: 2px solid #00FFFF !important;
        border-radius: 15px !important;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNZIONI ---
def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).limit(45).execute()
        return res.data
    except: return []

# --- 5. INPUT ---
st.markdown('<div class="neon-header">CHATITALY URBAN WALL</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
with c2:
    with st.form("spray_form", clear_on_submit=True):
        col_n, col_m = st.columns([1, 2])
        nick = col_n.text_input("TAG", placeholder="Chi sei?")
        txt = col_m.text_area("MESSAGGIO", height=65, placeholder="Spruzza qui...")
        submitted = st.form_submit_button("💨 BOMB THE WALL!")

    if submitted and txt.strip():
        st.session_state["saved_nick"] = nick
        l = len(txt)
        if l < 10: f_size, rot, font = random.randint(38, 50), random.randint(-15, 15), "'Rock Salt', cursive"
        elif l < 50: f_size, rot, font = random.randint(24, 32), random.randint(-8, 8), "'Permanent Marker', cursive"
        else: f_size, rot, font = random.randint(16, 22), random.randint(-3, 3), "'Patrick Hand', cursive"

        data = {
            "testo": txt, "autore": nick.upper() if nick.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF"]),
            "font": font, "rotazione": rot, "font_size": f_size
        }
        try:
            supabase.table("muro").insert(data).execute()
            st.rerun()
        except: st.rerun()

# --- 6. IL MURO CON EFFETTI ---
messaggi = carica_messaggi()
if messaggi:
    style_block = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Patrick+Hand&display=swap" rel="stylesheet">
    <style>
        .wall-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
            grid-auto-rows: minmax(200px, auto);
            gap: 25px;
            padding: 40px;
        }

        /* Effetto Goccia (Drip) */
        .drip {
            position: absolute;
            width: 4px;
            height: 40px;
            background: currentColor;
            border-radius: 0 0 4px 4px;
            top: 80%;
            opacity: 0.7;
            filter: blur(1px);
        }

        @keyframes sprayIn {
            0% { opacity: 0; filter: blur(15px); transform: scale(0.7) translateY(-20px); }
            100% { opacity: 1; filter: blur(0px); transform: scale(1) rotate(var(--r)); }
        }

        .graffito-box {
            position: relative;
            padding: 15px;
            text-align: center;
            white-space: pre-wrap;
            filter: drop-shadow(4px 4px 2px rgba(0,0,0,0.9));
            animation: sprayIn 0.8s ease-out forwards;
            margin-top: var(--mt);
            margin-left: var(--ml);
            transition: all 0.3s;
        }

        .graffito-box:hover {
            transform: scale(1.15) rotate(0deg) !important;
            z-index: 500;
            cursor: crosshair;
        }

        .tag { display: block; font-family: sans-serif; font-size: 10px; color: #666; margin-top: 8px; font-weight: bold; }
    </style>
    """
    
    content_html = ""
    for i, m in enumerate(messaggi):
        random.seed(m['id'])
        mt = random.randint(-40, 40)
        ml = random.randint(-40, 40)
        
        # Aggiungiamo gocce casuali solo per messaggi corti o medi
        drip_html = ""
        if len(m['testo']) < 40 and random.random() > 0.6:
            drip_left = random.randint(20, 80)
            drip_h = random.randint(20, 60)
            drip_html = f'<div class="drip" style="left:{drip_left}%; height:{drip_h}px;"></div>'
        
        content_html += f'''
        <div style="display: flex; justify-content: center; align-items: center;">
            <div class="graffito-box" style="
                --r: {m["rotazione"]}deg; 
                --mt: {mt}px; --ml: {ml}px;
                color: {m["colore"]}; font-family: {m["font"]}; 
                font-size: {m["font_size"]}px;">
                {m["testo"].replace("<","&lt;")}
                {drip_html}
                <span class="tag">TAG: {m["autore"]}</span>
            </div>
        </div>
        '''
    
    st.components.v1.html(f"{style_block}<div class='wall-grid'>{content_html}</div>", height=1800, scrolling=False)

# --- 7. ADMIN ---
with st.expander("MOD"):
    pwd = st.text_input("Psw", type="password")
    if pwd == "chatitaly123":
        for m in messaggi:
            col_a, col_b = st.columns([4,1])
            col_a.write(f"{m['autore']}: {m['testo'][:20]}")
            if col_b.button("🗑️", key=f"d_{m['id']}"):
                supabase.table("muro").delete().eq("id", m['id']).execute()
                st.rerun()
