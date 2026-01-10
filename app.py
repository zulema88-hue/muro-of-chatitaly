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

st.set_page_config(page_title="Urban Wall Glass", layout="wide", initial_sidebar_state="collapsed")

# --- 2. LOGICA RESET ---
def auto_reset_check():
    try:
        oggi = datetime.now().strftime("%Y-%m-%d")
        if st.session_state.get("last_check") != oggi:
            res = supabase.table("muro").select("created_at").order("id", desc=True).limit(1).execute()
            if res.data:
                data_ultimo_msg = res.data[0]['at'].split('T')[0]
                if data_ultimo_msg != oggi:
                    supabase.table("muro").delete().neq("id", 0).execute()
            st.session_state["last_check"] = oggi
    except: pass

auto_reset_check()

# --- 3. CSS CORE (GLASS DESIGN) ---
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

    .main-title {
        font-family: 'Permanent Marker', cursive;
        text-align: center;
        color: white;
        font-size: 40px;
        padding: 20px;
        letter-spacing: 2px;
    }

    /* Form ultra-pulito */
    .stForm {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        backdrop-filter: blur(5px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. CARICAMENTO DATI ---
def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).limit(50).execute()
        return res.data
    except: return []

# --- 5. INTERFACCIA INPUT ---
st.markdown('<div class="main-title">CHATITALY URBAN WALL</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([0.2, 0.6, 0.2])
with c2:
    with st.form("clean_form", clear_on_submit=True):
        col_tag, col_msg = st.columns([1, 2])
        nick = col_tag.text_input("TAG", placeholder="@anonimo")
        txt = col_msg.text_area("MESSAGGIO", height=70, placeholder="Scrivi qualcosa...")
        submitted = st.form_submit_button("INVIA")

    if submitted and txt.strip():
        l = len(txt)
        if l < 20: f_size, font = random.randint(28, 35), "'Rock Salt', cursive"
        elif l < 100: f_size, font = random.randint(18, 22), "'Permanent Marker', cursive"
        else: f_size, font = random.randint(14, 16), "'Patrick Hand', cursive"
        
        data = {
            "testo": txt, "autore": nick.upper() if nick.strip() else "ANONIMO",
            "colore": random.choice(["#FF3131", "#39FF14", "#00FFFF", "#FF00FF", "#FFFF00", "#FFFFFF"]),
            "font": font, "rotazione": 0, "font_size": f_size
        }
        supabase.table("muro").insert(data).execute()
        st.rerun()

# --- 6. IL MURO GLASS STYLE ---
messaggi = carica_messaggi()
if messaggi:
    style_block = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Patrick+Hand&display=swap" rel="stylesheet">
    <style>
        .wall-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 30px;
            padding: 40px;
        }

        .glass-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 15px;
            min-height: 400px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 20px;
            position: relative;
            backdrop-filter: blur(2px);
            transition: all 0.3s ease;
        }

        .message-text {
            text-align: center;
            word-wrap: break-word;
            width: 100%;
            line-height: 1.4;
        }

        .author-tag {
            position: absolute;
            bottom: 40px;
            font-family: sans-serif;
            font-size: 10px;
            color: rgba(255,255,255,0.3);
            letter-spacing: 1px;
        }

        /* La base luminosa dell'immagine */
        .neon-bar {
            position: absolute;
            bottom: 15px;
            width: 80px;
            height: 6px;
            background: var(--c);
            border-radius: 10px;
            box-shadow: 0 0 15px var(--c), 0 0 30px var(--c);
            opacity: 0.8;
        }
    </style>
    """
    
    cards_html = ""
    for m in messaggi:
        cards_html += f'''
        <div class="glass-card">
            <div class="message-text" style="color: {m['colore']}; font-family: {m['font']}; font-size: {m['font_size']}px;">
                {m['testo'].replace("<","&lt;")}
            </div>
            <div class="author-tag">@{m['autore']}</div>
            <div class="neon-bar" style="--c: {m['colore']};"></div>
        </div>
        '''
    
    st.components.v1.html(f"{style_block}<div class='wall-container'>{cards_html}</div>", height=2000, scrolling=False)
