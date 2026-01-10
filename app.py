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

st.set_page_config(page_title="Urban Wild Wall", layout="wide", initial_sidebar_state="collapsed")

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

# --- 3. CSS CORE ---
st.markdown("""
    <style>
    [data-testid="stSidebar"], .st-emotion-cache-10o1ihd, footer, header { display: none !important; }
    .stApp {
        background-image: url("https://static.vecteezy.com/system/resources/previews/007/233/624/non_2x/brick-black-wall-texture-background-dark-brickwork-pattern-block-stone-structure-backdrop-dark-brick-wall-realistic-template-abstract-modern-wallpaper-design-illustration-vector.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    ::-webkit-scrollbar { width: 0px; }
    * { scrollbar-width: none; }
    
    .neon-header {
        font-family: 'Rock Salt', cursive;
        text-align: center;
        color: #fff;
        text-shadow: 0 0 10px #FF00FF, 0 0 20px #FF00FF;
        font-size: 35px;
        padding: 15px;
    }
    
    .stForm {
        background: rgba(0,0,0,0.85) !important;
        border: 2px solid #00FFFF !important;
        border-radius: 15px !important;
        z-index: 1000;
        position: relative;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNZIONI ---
def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=False).limit(60).execute()
        return res.data
    except: return []

# --- 5. INPUT ---
st.markdown('<div class="neon-header">CHATITALY WILD WALL</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
with c2:
    with st.form("spray_form", clear_on_submit=True):
        col_n, col_m = st.columns([1, 2])
        nick = col_n.text_input("TAG", value=st.session_state.get("saved_nick", ""), placeholder="Chi sei?")
        txt = col_m.text_area("MESSAGGIO", height=65, placeholder="Spruzza qui...")
        submitted = st.form_submit_button("💨 BOMB THE WALL!")

    if submitted and txt.strip():
        st.session_state["saved_nick"] = nick
        l = len(txt)
        if l < 10: f_size, rot, font = random.randint(45, 60), random.randint(-25, 25), "'Rock Salt', cursive"
        elif l < 60: f_size, rot, font = random.randint(28, 38), random.randint(-15, 15), "'Permanent Marker', cursive"
        else: f_size, rot, font = random.randint(18, 23), random.randint(-5, 5), "'Patrick Hand', cursive"

        data = {
            "testo": txt, "autore": nick.upper() if nick.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF", "#FF4500"]),
            "font": font, "rotazione": rot, "font_size": f_size
        }
        try:
            supabase.table("muro").insert(data).execute()
            st.rerun()
        except: st.rerun()

# --- 6. IL MURO CAOTICO ---
messaggi = carica_messaggi()
if messaggi:
    style_block = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Patrick+Hand&display=swap" rel="stylesheet">
    <style>
        .wall-canvas {
            position: relative; width: 100%; height: 1000px; 
            overflow: hidden; background: transparent;
        }
        @keyframes sprayIn {
            0% { opacity: 0; filter: blur(15px); transform: scale(1.4); }
            100% { opacity: 1; filter: blur(0px); transform: scale(1) rotate(var(--rot)); }
        }
        .graffito {
            position: absolute; white-space: pre-wrap; word-wrap: break-word;
            text-align: center; line-height: 1.1; animation: sprayIn 0.6s ease-out forwards;
            filter: drop-shadow(3px 3px 0px rgba(0,0,0,0.9));
            transition: transform 0.2s;
        }
        .graffito:hover {
            transform: scale(1.2) rotate(0deg) !important; z-index: 2000 !important;
            filter: drop-shadow(0 0 10px currentColor);
        }
        .tag-name { display: block; font-family: sans-serif; font-size: 9px; color: rgba(255,255,255,0.3); margin-top: 4px; }
    </style>
    """
    
    content_html = ""
    for i, m in enumerate(messaggi):
        # Usiamo l'ID per generare coordinate "stabili" ma casuali
        random.seed(m['id']) 
        left = random.randint(2, 78)
        top = random.randint(2, 82)
        z_index = 10 + i
        max_w = "160px" if len(m['testo']) < 15 else "360px"
        
        content_html += f'''
        <div class="graffito" style="
            left: {left}%; top: {top}%; z-index: {z_index}; 
            color: {m["colore"]}; font-family: {m["font"]}; 
            font-size: {m["font_size"]}px; --rot: {m["rotazione"]}deg;
            max-width: {max_w};">
            {m["testo"].replace("<","&lt;")}
            <span class="tag-name">BY {m["autore"]}</span>
        </div>
        '''
    
    st.components.v1.html(f"{style_block}<div class='wall-canvas'>{content_html}</div>", height=1000)

# --- 7. ADMIN ---
with st.expander("MOD"):
    pwd = st.text_input("Psw", type="password")
    if pwd == "chatitaly123":
        for m in reversed(messaggi):
            col_a, col_b = st.columns([4,1])
            col_a.write(f"{m['autore']}: {m['testo'][:20]}")
            if col_b.button("🗑️", key=f"d_{m['id']}"):
                supabase.table("muro").delete().eq("id", m['id']).execute()
                st.rerun()
