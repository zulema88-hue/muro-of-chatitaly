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

# --- 3. CSS GLOBALE ---
st.markdown("""
    <style>
    [data-testid="stSidebar"], .st-emotion-cache-10o1ihd, footer, header { display: none !important; }
    .stApp {
        background-image: url("https://static.vecteezy.com/system/resources/previews/007/233/624/non_2x/brick-black-wall-texture-background-dark-brickwork-pattern-block-stone-structure-backdrop-dark-brick-wall-realistic-template-abstract-modern-wallpaper-design-illustration-vector.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    ::-webkit-scrollbar { width: 0px; background: transparent; }
    * { scrollbar-width: none; }
    
    .neon-title {
        font-family: 'Permanent Marker', cursive;
        text-align: center;
        color: white;
        text-shadow: 0 0 20px #FF00FF, 0 0 40px #00FFFF;
        font-size: clamp(30px, 8vw, 50px);
        padding: 10px;
    }
    .stTextInput input, .stTextArea textarea {
        background-color: rgba(0,0,0,0.8) !important;
        color: #39FF14 !important;
        border: 2px solid #444 !important;
        border-radius: 10px !important;
    }
    .stButton button {
        background: linear-gradient(45deg, #FF00FF, #00FFFF) !important;
        color: white !important; font-weight: bold !important; border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNZIONI DATI ---
def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).limit(50).execute()
        return res.data
    except: return []

# --- 5. INTERFACCIA ---
st.markdown('<div class="neon-title">CHATITALY URBAN WALL</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
with c2:
    with st.form("spruzza_form", clear_on_submit=True):
        col_n, col_m = st.columns([1, 3])
        with col_n:
            nick = st.text_input("NICK", value=st.session_state.get("saved_nick", ""), placeholder="Tag")
        with col_m:
            txt = st.text_area("MESSAGGIO", height=70, placeholder="Cosa scrivi sul muro?")
        submitted = st.form_submit_button("💨 SPRUZZA!")

    if submitted and txt.strip():
        st.session_state["saved_nick"] = nick
        lunghezza = len(txt)
        
        # LOGICA DINAMICA INTELLIGENTE
        if lunghezza < 5: # Emoticon o sigle
            f_size, rot, font, width = random.randint(40, 55), random.randint(-15, 15), "'Rock Salt', cursive", "100px"
        elif lunghezza < 20: # Frasi brevi
            f_size, rot, font, width = random.randint(30, 38), random.randint(-10, 10), "'Permanent Marker', cursive", "180px"
        elif lunghezza < 100: # Frasi medie
            f_size, rot, font, width = random.randint(20, 26), random.randint(-5, 5), "'Permanent Marker', cursive", "250px"
        else: # Canzoni o poesie
            f_size, rot, font, width = random.randint(15, 18), random.randint(-2, 2), "'Patrick Hand', cursive", "320px"

        data = {
            "testo": txt, "autore": nick.upper() if nick.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF", "#00FF7F", "#FFD700"]),
            "font": font, "rotazione": rot, "font_size": f_size
        }
        try:
            supabase.table("muro").insert(data).execute()
            st.rerun()
        except: st.rerun()

# --- 6. IL MURO SPARPARGLIATO ---
messaggi = carica_messaggi()
if messaggi:
    style_block = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Patrick+Hand&display=swap" rel="stylesheet">
    <style>
        ::-webkit-scrollbar { width: 0px; height: 0px; }
        html, body { scrollbar-width: none; background: transparent; margin: 0; padding: 0; overflow-x: hidden; }
        
        .wall-container { 
            display: flex; 
            flex-wrap: wrap; 
            justify-content: space-around; /* Sparpiglia i graffiti sulla riga */
            align-items: center; 
            padding: 40px 20px;
            gap: 10px;
        }

        @keyframes sprayEffect {
            0% { filter: blur(10px); opacity: 0; transform: scale(0.8); }
            100% { filter: blur(0px); opacity: 1; transform: scale(1) rotate(var(--rot)); }
        }

        .graffiti-box { 
            position: relative;
            padding: 15px; 
            text-align: center; 
            filter: drop-shadow(5px 5px 2px rgba(0,0,0,0.9)); 
            white-space: pre-wrap; 
            word-wrap: break-word; 
            animation: sprayEffect 0.8s ease-out forwards;
            /* L'EFFETTO CASUALE: spostamenti randomici */
            margin-top: var(--m-top);
            margin-bottom: var(--m-bottom);
            margin-left: var(--m-left);
            margin-right: var(--m-right);
        }

        .author { display: block; font-family: sans-serif; font-size: 9px; color: #888; margin-top: 8px; opacity: 0.6; text-transform: uppercase; }
    </style>
    """
    
    content_html = ""
    for i, m in enumerate(messaggi):
        # Generiamo spostamenti casuali per ogni singolo messaggio
        m_top = f"{random.randint(-30, 40)}px"
        m_bottom = f"{random.randint(-20, 30)}px"
        m_left = f"{random.randint(-10, 20)}px"
        m_right = f"{random.randint(-10, 20)}px"
        
        # Determiniamo la larghezza massima in base alla lunghezza del testo salvato
        l_testo = len(m['testo'])
        max_w = "120px" if l_testo < 10 else "250px" if l_testo < 50 else "350px"
        
        delay = i * 0.05 if i < 20 else 0 
        
        content_html += f'''
        <div class="graffiti-box" style="
            --rot: {m["rotazione"]}deg; 
            --m-top: {m_top}; --m-bottom: {m_bottom}; --m-left: {m_left}; --m-right: {m_right};
            color: {m["colore"]}; 
            font-family: {m["font"]}; 
            font-size: {m["font_size"]}px; 
            max-width: {max_w};
            animation-delay: {delay}s;">
            {m["testo"].replace("<","&lt;")}
            <span class="author">BY {m["autore"]}</span>
        </div>
        '''
    
    st.components.v1.html(f"{style_block}<div class='wall-container'>{content_html}</div>", height=2500, scrolling=False)

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
