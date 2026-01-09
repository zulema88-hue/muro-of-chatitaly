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

st.set_page_config(page_title="Il Muro di Chatitaly", layout="wide")

# --- STILE GRAFICO (CORRETTO E DIMENSIONI RIDOTTE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Frijole&family=Nosifer&family=Rubik+Glitch&display=swap');
    
    .stApp {
        background-color: #0e0e0e;
        background-image: radial-gradient(#222 1px, transparent 1px);
        background-size: 30px 30px;
    }

    .neon-title {
        font-family: 'Frijole', cursive;
        color: #fff;
        text-align: center;
        text-shadow: 0 0 10px #0ff, 0 0 20px #f0f;
        font-size: 40px;
        padding: 10px;
    }

    .wall-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 15px;
        padding: 20px;
    }

    .graffiti-tag {
        display: inline-block;
        padding: 8px;
        line-height: 1.1;
        filter: drop-shadow(2px 2px 2px #000);
        white-space: nowrap;
    }

    .author-tag {
        font-size: 10px;
        font-family: sans-serif;
        display: block;
        opacity: 0.4;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).limit(50).execute()
        return res.data
    except:
        return []

def spruzza():
    t = st.session_state.get("input_testo", "")
    n = st.session_state.get("input_nick", "")
    if t and t.strip():
        data = {
            "testo": t.upper(),
            "autore": n.upper() if n.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131"]),
            "font": random.choice(["'Permanent Marker'", "'Nosifer'", "'Rubik Glitch'"]),
            "rotazione": random.randint(-15, 15),
            "font_size": random.randint(22, 38) # Scritte più piccole (prima era fino a 55)
        }
        try:
            supabase.table("muro").insert(data).execute()
            st.session_state["input_testo"] = ""
            # RIMOSSO st.rerun() per togliere l'errore giallo
        except Exception as e:
            st.error(f"Errore: {e}")

# --- INTERFACCIA ---
st.markdown("<h1 class='neon-title'>CHATITALY WALL</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    col_n, col_t = st.columns([1, 3])
    with col_n:
        st.text_input("NICK", key="input_nick", placeholder="Nome")
    with col_t:
        st.text_input("SCRIVI E INVIO", key="input_testo", on_change=spruzza, placeholder="Messaggio...")

st.markdown("<hr style='border: 0.5px solid #333'>", unsafe_allow_html=True)

# --- VISUALIZZAZIONE ---
messaggi = carica_messaggi()

if messaggi:
    html = "<div class='wall-container'>"
    for m in messaggi:
        # Recupero parametri o valori di default
        txt = m.get('testo', '')
        aut = m.get('autore', 'ANON')
        col = m.get('colore', '#fff')
        fnt = m.get('font', 'sans-serif')
        rot = m.get('rotazione', 0)
        siz = m.get('font_size', 25)
        
        html += f"""
        <div class="graffiti-tag" style="transform: rotate({rot}deg); color: {col}; font-family: {fnt}, cursive; font-size: {siz}px;">
            {txt}
            <span class="author-tag">BY {aut}</span>
        </div>
        """
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
else:
    st.info("Muro vuoto. Scrivi qualcosa!")
