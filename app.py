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

# --- 2. LOGICA RESET AUTOMATICO (MEZZANOTTE) ---
# Controlliamo se esiste un record con la data di oggi. Se il muro è vuoto o i messaggi sono di ieri, resetta.
def auto_reset_check():
    try:
        oggi = datetime.now().strftime("%Y-%m-%d")
        # Usiamo lo stato della sessione per evitare di controllare a ogni click
        if st.session_state.get("last_check") != oggi:
            # Recuperiamo l'ultimo messaggio per vedere la data
            res = supabase.table("muro").select("created_at").order("id", desc=True).limit(1).execute()
            if res.data:
                data_ultimo_msg = res.data[0]['created_at'].split('T')[0]
                if data_ultimo_msg != oggi:
                    # Se l'ultimo messaggio non è di oggi, cancella tutto
                    supabase.table("muro").delete().neq("id", 0).execute()
            st.session_state["last_check"] = oggi
    except:
        pass

auto_reset_check()

# --- 3. CSS AGGIORNATO (MIGLIORATO PER MOBILE) ---
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
        text-shadow: 0 0 15px #FF00FF;
        font-size: clamp(25px, 8vw, 40px);
        padding: 10px;
        background: rgba(0,0,0,0.7);
    }
    .stTextInput input, .stTextArea textarea {
        background-color: rgba(0,0,0,0.8) !important;
        color: #00FF00 !important;
        border: 1px solid #444 !important;
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
        col_n, col_m = st.columns([1, 2])
        with col_n:
            nick = st.text_input("NICK", value=st.session_state.get("saved_nick", ""), placeholder="Tag")
        with col_m:
            txt = st.text_area("MESSAGGIO", height=70, placeholder="Scrivi...")
        submitted = st.form_submit_button("SPRUZZA 🎨")

    if submitted and txt.strip():
        st.session_state["saved_nick"] = nick
        lunghezza = len(txt)
        # Calcolo font
        if lunghezza > 50: f_size, rot, font = random.randint(15, 18), random.randint(-2, 2), "'Patrick Hand', cursive"
        else: f_size, rot, font = random.randint(24, 32), random.randint(-10, 10), "'Rock Salt', cursive"

        data = {"testo": txt, "autore": nick.upper() if nick.strip() else "ANONIMO", 
                "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF"]), 
                "font": font, "rotazione": rot, "font_size": f_size}
        try:
            supabase.table("muro").insert(data).execute()
            st.rerun()
        except: st.rerun()

# --- 6. IL MURO (VERSIONE MOBILE-FRIENDLY DISORDINATA) ---
messaggi = carica_messaggi()
if messaggi:
    style_block = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Patrick+Hand&display=swap" rel="stylesheet">
    <style>
        body { margin: 0; background: transparent; overflow-x: hidden; }
        .wall-container { 
            display: flex; 
            flex-wrap: wrap; 
            justify-content: center; 
            align-items: center;
            gap: 10px; /* Ridotto il gap per farli stare vicini */
            padding: 10px; 
        }
        .graffiti-box { 
            padding: 8px; 
            text-align: center; 
            filter: drop-shadow(3px 3px 1px rgba(0,0,0,0.9)); 
            white-space: pre-wrap; 
            word-wrap: break-word; 
            line-height: 1.1; 
            max-width: 180px; /* Più stretto così su mobile ne stanno almeno due vicini */
            margin: 5px;
        }
        .author { display: block; font-family: sans-serif; font-size: 8px; color: #888; margin-top: 3px; text-transform: uppercase; }
    </style>
    """
    content_html = ""
    for m in messaggi:
        content_html += f'<div class="graffiti-box" style="transform: rotate({m["rotazione"]}deg); color: {m["colore"]}; font-family: {m["font"]}; font-size: {m["font_size"]}px;">{m["testo"].replace("<","&lt;")}<span class="author">BY {m["autore"]}</span></div>'
    
    st.components.v1.html(f"{style_block}<div class='wall-container'>{content_html}</div>", height=1500, scrolling=True)

# --- 7. MODERAZIONE ---
with st.expander("🛡️ Admin"):
    pwd = st.text_input("Psw", type="password")
    if pwd == "chatitaly123":
        if st.button("RESET TOTALE ORA"):
            supabase.table("muro").delete().neq("id", 0).execute()
            st.rerun()
        for m in messaggi:
            c_info, c_btn = st.columns([4, 1])
            c_info.write(f"{m['autore']}: {m['testo'][:30]}")
            if c_btn.button("❌", key=f"del_{m['id']}"):
                supabase.table("muro").delete().eq("id", m['id']).execute()
                st.rerun()
