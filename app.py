import streamlit as st
import random
from supabase import create_client

# --- CONNESSIONE ---
URL = "https://wumwurwuwoysrvutupde.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind1bXd1cnd1d295c3J2dXR1cGRlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc5NDgwMzIsImV4cCI6MjA4MzUyNDAzMn0.90s0KWQTOHb2fHdlgS4vvMNI-7iiDA-L0aR0qJ_5k7k"

@st.cache_resource
def init_connection():
    return create_client(URL, KEY)

supabase = init_connection()

st.set_page_config(page_title="Chatitaly Urban Wall", layout="wide", initial_sidebar_state="collapsed")

# --- CSS PER NASCONDERE TUTTO IL NECESSARIO ---
st.markdown("""
    <style>
    [data-testid="stSidebar"], .st-emotion-cache-10o1ihd, footer, header { display: none !important; }
    .stApp {
        background-image: url("https://static.vecteezy.com/system/resources/previews/007/233/624/non_2x/brick-black-wall-texture-background-dark-brickwork-pattern-block-stone-structure-backdrop-dark-brick-wall-realistic-template-abstract-modern-wallpaper-design-illustration-vector.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    .stTextInput input {
        background-color: rgba(0,0,0,0.8) !important;
        color: #39FF14 !important;
        border: 1px solid #333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).limit(40).execute()
        return res.data
    except: return []

def spruzza():
    t = st.session_state.get("input_testo", "")
    n = st.session_state.get("input_nick", "")
    if t and t.strip():
        data = {
            "testo": t.upper(),
            "autore": n.upper() if n.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF"]),
            "font": random.choice(["'Permanent Marker'", "'Nosifer'", "'Rubik Glitch'", "'Rock Salt'"]),
            "rotazione": random.randint(-12, 12),
            "font_size": random.randint(28, 45)
        }
        try:
            supabase.table("muro").insert(data).execute()
            st.session_state["input_testo"] = ""
        except: pass

# --- UI ---
st.markdown("<h1 style='text-align:center; color:white; font-family:sans-serif; text-shadow: 0 0 10px #0ff;'>CHATITALY WALL</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    col1, col2 = st.columns([1, 3])
    with col1: st.text_input("TAG", key="input_nick", placeholder="Nick")
    with col2: st.text_input("MESSAGGIO", key="input_testo", on_change=spruzza, placeholder="Scrivi e premi Invio...")

# --- IL MURO (VERSIONE BLINDATA) ---
messaggi = carica_messaggi()

if messaggi:
    # Costruiamo il blocco HTML con i font inclusi
    html_muro = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Nosifer&family=Rubik+Glitch&family=Rock+Salt&display=swap" rel="stylesheet">
    <style>
        .wall { 
            display: flex; flex-wrap: wrap; justify-content: center; 
            align-items: center; gap: 30px; padding: 20px; 
            font-family: sans-serif;
        }
        .tag { 
            text-align: center; line-height: 1; 
            filter: drop-shadow(3px 3px 2px rgba(0,0,0,0.8));
        }
        .auth { font-size: 11px; opacity: 0.6; display: block; margin-top: 5px; font-family: sans-serif; color: white; }
    </style>
    <div class="wall">
    """
    
    for m in messaggi:
        html_muro += f"""
        <div class="tag" style="transform: rotate({m['rotazione']}deg); color: {m['colore']}; font-family: {m['font']}; font-size: {m['font_size']}px;">
            {m['testo']}
            <span class="auth">BY {m['autore']}</span>
        </div>
        """
    
    html_muro += "</div>"
    
    # Questo comando isola l'HTML e impedisce a Streamlit di romperlo
    st.components.v1.html(html_muro, height=600, scrolling=True)

# Admin
with st.expander("Admin"):
    if st.text_input("Psw", type="password") == "chatitaly123":
        if st.button("RESET"):
            supabase.table("muro").delete().neq("id", 0).execute()
            st.rerun()
