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

st.set_page_config(page_title="Chatitaly Urban Wall", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS STILE URBANO ---
st.markdown("""
    <style>
    /* Nasconde elementi inutili */
    [data-testid="stSidebar"], .st-emotion-cache-10o1ihd, footer, header { display: none !important; }
    
    /* Sfondo Muro */
    .stApp {
        background-image: url("https://static.vecteezy.com/system/resources/previews/007/233/624/non_2x/brick-black-wall-texture-background-dark-brickwork-pattern-block-stone-structure-backdrop-dark-brick-wall-realistic-template-abstract-modern-wallpaper-design-illustration-vector.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Titolo */
    .neon-title {
        font-family: sans-serif;
        text-align: center;
        color: white;
        text-shadow: 0 0 10px #FF00FF, 0 0 20px #00FFFF;
        font-size: 40px;
        font-weight: 900;
        padding: 20px;
        background: rgba(0,0,0,0.6);
        margin-bottom: 20px;
        border-bottom: 2px solid #333;
    }

    /* Stile Input */
    .stTextInput input, .stTextArea textarea {
        background-color: rgba(0,0,0,0.8) !important;
        color: #00FF00 !important;
        border: 1px solid #444 !important;
        font-weight: bold;
    }
    
    /* Bottone Spruzza */
    .stButton button {
        background-color: #FF00FF !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        transition: all 0.3s;
    }
    .stButton button:hover {
        background-color: #00FFFF !important;
        color: black !important;
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGICA DI CARICAMENTO ---
def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).limit(50).execute()
        return res.data
    except: return []

# --- 4. INTERFACCIA ---
st.markdown('<div class="neon-title">CHATITALY WALL</div>', unsafe_allow_html=True)

# Creiamo le colonne per centrare il form
c1, c2, c3 = st.columns([1, 2, 1])

with c2:
    # --- FORM DI INSERIMENTO (La soluzione ai tuoi problemi) ---
    with st.form("spruzza_form", clear_on_submit=True): # clear_on_submit pulisce tutto dopo l'invio
        col_nick, col_msg = st.columns([1, 3])
        
        with col_nick:
            # Salviamo il nick in session state per non doverlo riscrivere se il form lo cancella
            default_nick = st.session_state.get("saved_nick", "")
            nick_input = st.text_input("NICK", value=default_nick, placeholder="Chi sei?")
        
        with col_msg:
            txt_input = st.text_area("MESSAGGIO (Canzoni OK)", height=80, placeholder="Scrivi qui... (Usa CTRL+INVIO per inviare veloce)")

        # Il tasto che invia il form
        submitted = st.form_submit_button("SPRUZZA SUL MURO 🎨")

    # --- LOGICA DI INVIO ---
    if submitted and txt_input.strip():
        # Salviamo il nick per la prossima volta
        st.session_state["saved_nick"] = nick_input
        
        # Calcoli intelligenti per il font
        lunghezza = len(txt_input)
        
        # Se è una canzone lunga -> Font piccolo e leggibile
        if lunghezza > 50:
            f_size = random.randint(16, 19)
            rot = random.randint(-1, 1)
            font_scelto = "'Patrick Hand', cursive"
        # Se è medio -> Font medio
        elif lunghezza > 20:
            f_size = random.randint(20, 26)
            rot = random.randint(-3, 3)
            font_scelto = "'Permanent Marker', cursive"
        # Se è corto (Urlo) -> Font Enorme
        else:
            f_size = random.randint(30, 45)
            rot = random.randint(-6, 6)
            font_scelto = "'Rock Salt', cursive"

        data = {
            "testo": txt_input,
            "autore": nick_input.upper() if nick_input.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF", "#FFA500"]),
            "font": font_scelto,
            "rotazione": rot,
            "font_size": f_size
        }
        
        try:
            supabase.table("muro").insert(data).execute()
            st.rerun() # RICARICA LA PAGINA IMMEDIATAMENTE
        except Exception as e:
            st.error(f"Errore: {e}")

# --- 5. IL MURO (VISUALIZZAZIONE) ---
messaggi = carica_messaggi()

if messaggi:
    html_muro = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Patrick+Hand&display=swap" rel="stylesheet">
    <style>
        body { margin: 0; background: transparent; }
        .wall-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            align-items: flex-start;
            gap: 25px;
            padding: 20px;
        }
        .graffiti-box {
            display: inline-block;
            background: rgba(0,0,0,0.2); /* Leggerissimo sfondo scuro per leggere meglio su mattoni */
            padding: 15px;
            border-radius: 4px;
            text-align: center;
            filter: drop-shadow(5px 5px 0px rgba(0,0,0,0.5));
            max-width: 350px; /* Larghezza massima per le canzoni */
            white-space: pre-wrap; /* Mantiene gli a capo */
            word-wrap: break-word;
            line-height: 1.3;
        }
        .author
