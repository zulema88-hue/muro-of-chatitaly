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

st.set_page_config(page_title="Chatitaly Urban Wall", layout="wide", initial_sidebar_state="collapsed")

# --- 2. LOGICA RESET AUTOMATICO ---
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

# --- 3. CSS GENERALE ---
st.markdown("""
    <style>
    [data-testid="stSidebar"], .st-emotion-cache-10o1ihd, footer, header { display: none !important; }
    .stApp {
        background-image: url("https://static.vecteezy.com/system/resources/previews/007/233/624/non_2x/brick-black-wall-texture-background-dark-brickwork-pattern-block-stone-structure-backdrop-dark-brick-wall-realistic-template-abstract-modern-wallpaper-design-illustration-vector.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    .neon-title {
        font-family: 'Permanent Marker', cursive;
        text-align: center;
        color: white;
        text-shadow: 0 0 20px #FF00FF, 0 0 40px #00FFFF;
        font-size: clamp(30px, 10vw, 55px);
        padding: 20px;
    }
    .stTextInput input, .stTextArea textarea {
        background-color: rgba(0,0,0,0.8) !important;
        color: #00FF00 !important;
        border: 2px solid #555 !important;
        border-radius: 15px !important;
    }
    /* Bottone pulsante */
    .stButton button {
        background: linear-gradient(45deg, #FF00FF, #00FFFF) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 20px !important;
        border: none !important;
        box-shadow: 0 0 15px rgba(255, 0, 255, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNZIONI DATI ---
def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).limit(40).execute()
        return res.data
    except: return []

# --- 5. INTERFACCIA ---
st.markdown('<div class="neon-title">CHATITALY URBAN WALL</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
with c2:
    with st.form("spruzza_form", clear_on_submit=True):
        col_n, col_m = st.columns([1, 2])
        with col_n:
            nick = st.text_input("NICK", value=st.session_state.get("saved_nick", ""), placeholder="Il tuo Tag")
        with col_m:
            txt = st.text_area("MESSAGGIO", height=70, placeholder="Cosa vuoi 'spruzzare'?")
        
        submitted = st.form_submit_button("💨 SPRUZZA SUL MURO!")

    if submitted and txt.strip():
        st.session_state["saved_nick"] = nick
        # Logica dimensioni e font
        if len(txt) > 50: f_size, rot, font = random.randint(16, 19), random.randint(-2, 2), "'Patrick Hand', cursive"
        else: f_size, rot, font = random.randint(26, 36), random.randint(-12, 12), "'Rock Salt', cursive"

        data = {"testo": txt, "autore": nick.upper() if nick.strip() else "ANONIMO", 
                "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF"]), 
                "font": font, "rotazione": rot, "font_size": f_size}
        try:
            supabase.table("muro").insert(data).execute()
            # Piccolo script per il suono (opzionale)
            st.markdown('<audio autoplay><source src="https://www.soundjay.com/misc/sounds/spray-can-01.mp3" type="audio/mpeg"></audio>', unsafe_allow_html=True)
            st.rerun()
        except: st.rerun()

# --- 6. IL MURO CON ANIMAZIONE SPRAY ---
messaggi = carica_messaggi()
if messaggi:
    style_block = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Patrick+Hand&display=swap" rel="stylesheet">
    <style>
        body { margin: 0; background: transparent; }
        .wall-container { 
            display: flex; flex-wrap: wrap; justify-content: center; 
            align-items: center; gap: 15px; padding: 20px; 
        }
        
        /* ANIMAZIONE SPRAY */
        @keyframes sprayEffect {
            0% { filter: blur(15px); opacity: 0; transform: scale(0.5) rotate(0deg); }
            50% { filter: blur(5px); opacity: 0.8; }
            100% { filter: blur(0px); opacity: 1; transform: scale(1) rotate(var(--rot)); }
        }

        .graffiti-box { 
            padding: 10px; text-align: center; 
            filter: drop-shadow(4px 4px 2px rgba(0,0,0,0.9)); 
            white-space: pre-wrap; word-wrap: break-word; 
            max-width: 220px;
            animation: sprayEffect 1s ease-out forwards;
        }

        .author { display: block; font-family: sans-serif; font-size: 9px; color: #888; margin-top: 5px; opacity: 0.7; }
    </style>
    """
    
    content_html = ""
    for i, m in enumerate(messaggi):
        # Aggiungiamo un piccolo ritardo per ogni graffito così appaiono uno dopo l'altro
        delay = i * 0.1 if i < 10 else 0 
        content_html += f'''
        <div class="graffiti-box" style="--rot: {m["rotazione"]}deg; color: {m["colore"]}; font-family: {m["font"]}; font-size: {m["font_size"]}px; animation-delay: {delay}s;">
            {m["testo"].replace("<","&lt;")}
            <span class="author">BY {m["autore"]}</span>
        </div>
        '''
    
    st.components.v1.html(f"{style_block}<div class='wall-container'>{content_html}</div>", height=1500, scrolling=True)

# --- 7. ADMIN ---
with st.expander("🛡️ Moderazione"):
    pwd = st.text_input("Psw", type="password")
    if pwd == "chatitaly123":
        for m in messaggi:
            c_info, c_btn = st.columns([4, 1])
            c_info.write(f"{m['autore']}: {m['testo'][:30]}")
            if c_btn.button("Elimina", key=f"del_{m['id']}"):
                supabase.table("muro").delete().eq("id", m['id']).execute()
                st.rerun()
