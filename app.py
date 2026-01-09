import streamlit as st
import random
from supabase import create_client

# --- 1. CONNESSIONE ---
URL = "https://wumwurwuwoysrvutupde.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind1bXd1cnd1d295c3J2dXR1cGRlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc5NDgwMzIsImV4cCI6MjA4MzUyNDAzMn0.90s0KWQTOHb2fHdlgS4vvMNI-7iiDA-L0aR0qJ_5k7k"

@st.cache_resource
def init_connection():
    return create_client(URL, KEY)

supabase = init_connection()

st.set_page_config(page_title="Il Muro di Chatitaly", layout="wide")

# --- 2. CSS (STILE GRAFICO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Nosifer&family=Rubik+Glitch&display=swap');
    
    .stApp { background-color: #000000 !important; }
    
    .neon-title {
        font-family: 'Permanent Marker', cursive;
        color: #00ffff;
        text-align: center;
        text-shadow: 0 0 10px #0ff, 0 0 20px #f0f;
        font-size: 40px;
        margin-bottom: 20px;
    }

    .wall {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        background: #111;
        padding: 30px;
        border-radius: 20px;
        border: 2px solid #222;
        min-height: 300px;
    }

    .tag {
        display: inline-block;
        margin: 15px;
        line-height: 1;
        text-align: center;
    }

    .nickname {
        font-family: sans-serif;
        font-size: 10px;
        color: #666;
        display: block;
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGICA ---
def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).limit(30).execute()
        return res.data
    except:
        return []

def spruzza():
    t = st.session_state.get("input_testo", "")
    n = st.session_state.get("input_nick", "ANON")
    if t and t.strip():
        data = {
            "testo": t.upper(),
            "autore": n.upper(),
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131"]),
            "font": random.choice(["'Permanent Marker'", "'Nosifer'", "'Rubik Glitch'"]),
            "rotazione": random.randint(-8, 8),
            "font_size": random.randint(20, 30)
        }
        try:
            supabase.table("muro").insert(data).execute()
            st.session_state["input_testo"] = ""
        except:
            pass

# --- 4. INTERFACCIA ---
st.markdown('<h1 class="neon-title">CHATITALY WALL</h1>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.text_input("NICK", key="input_nick", placeholder="Il tuo nome")
    st.text_input("MESSAGGIO", key="input_testo", on_change=spruzza, placeholder="Scrivi e premi Invio")

st.divider()

# --- 5. VISUALIZZAZIONE (VERSIONE ANTI-CODICE) ---
messaggi = carica_messaggi()

if messaggi:
    # Iniziamo la stringa HTML
    html_output = "<div class='wall'>"
    
    for m in messaggi:
        # Pulizia dati per sicurezza
        txt = str(m.get('testo', '')).replace('<', '&lt;')
        aut = str(m.get('autore', 'ANON')).replace('<', '&lt;')
        col = m.get('colore', '#FFF')
        fnt = m.get('font', 'sans-serif')
        siz = m.get('font_size', 20)
        rot = m.get('rotazione', 0)
        
        # Aggiungiamo il pezzo di HTML
        html_output += f"""
        <div class="tag" style="transform: rotate({rot}deg); color: {col}; font-family: {fnt}; font-size: {siz}px;">
            {txt}
            <span class="nickname">BY {aut}</span>
        </div>
        """
    
    html_output += "</div>"
    
    # Stampiamo tutto l'HTML finale in un unico blocco markdown
    st.markdown(html_output, unsafe_allow_html=True)
else:
    st.write("Muro pulito...")

# SideBar Admin
with st.sidebar:
    if st.text_input("Admin", type="password") == "chatitaly123":
        if st.button("RESET MURO"):
            supabase.table("muro").delete().neq("id", 0).execute()
            st.rerun()
