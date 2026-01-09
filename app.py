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

# --- 2. CSS GENERALE ---
st.markdown("""
    <style>
    [data-testid="stSidebar"], .st-emotion-cache-10o1ihd, footer, header { display: none !important; }
    
    .stApp {
        background-image: url("https://static.vecteezy.com/system/resources/previews/007/233/624/non_2x/brick-black-wall-texture-background-dark-brickwork-pattern-block-stone-structure-backdrop-dark-brick-wall-realistic-template-abstract-modern-wallpaper-design-illustration-vector.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    
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

    .stTextInput input, .stTextArea textarea {
        background-color: rgba(0,0,0,0.8) !important;
        color: #00FF00 !important;
        border: 1px solid #444 !important;
        font-weight: bold;
    }
    
    .stButton button {
        background-color: #FF00FF !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #00FFFF !important;
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CARICAMENTO DATI ---
def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).limit(50).execute()
        return res.data
    except: return []

# --- 4. INTERFACCIA ---
st.markdown('<div class="neon-title">CHATITALY WALL</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])

with c2:
    # FORM DI INSERIMENTO
    with st.form("spruzza_form", clear_on_submit=True):
        col_nick, col_msg = st.columns([1, 3])
        
        with col_nick:
            default_nick = st.session_state.get("saved_nick", "")
            nick_input = st.text_input("NICK", value=default_nick, placeholder="Chi sei?")
        
        with col_msg:
            txt_input = st.text_area("MESSAGGIO (Canzoni OK)", height=80, placeholder="Scrivi qui... (Invio va a capo)")

        submitted = st.form_submit_button("SPRUZZA SUL MURO 🎨")

    if submitted and txt_input.strip():
        st.session_state["saved_nick"] = nick_input
        
        lunghezza = len(txt_input)
        
        # LOGICA FONT
        if lunghezza > 50:
            f_size = random.randint(16, 19)
            rot = random.randint(-1, 1)
            font_scelto = "'Patrick Hand', cursive"
        elif lunghezza > 20:
            f_size = random.randint(20, 26)
            rot = random.randint(-3, 3)
            font_scelto = "'Permanent Marker', cursive"
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
            st.rerun()
        except:
            st.error("Errore di connessione")

# --- 5. IL MURO (CORRETTO) ---
messaggi = carica_messaggi()

if messaggi:
    # Qui c'era l'errore. Ho diviso la stringa per evitare problemi.
    style_block = """
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
            background: rgba(0,0,0,0.2);
            padding: 15px;
            border-radius: 4px;
            text-align: center;
            filter: drop-shadow(5px 5px 0px rgba(0,0,0,0.5));
            max-width: 350px;
            white-space: pre-wrap;
            word-wrap: break-word;
            line-height: 1.3;
        }
        .author {
            display: block;
            font-family: sans-serif;
            font-size: 10px;
            color: #ccc;
            margin-top: 10px;
            text-transform: uppercase;
            border-top: 1px dashed rgba(255,255,255,0.3);
            padding-top: 5px;
        }
    </style>
    """
    
    content_html = ""
    for m in messaggi:
        clean_text = str(m['testo']).replace("<", "&lt;")
        
        content_html += f"""
        <div class="graffiti-box" style="
            transform: rotate({m['rotazione']}deg); 
            color: {m['colore']}; 
            font-family: {m['font']}; 
            font-size: {m['font_size']}px;">
            {clean_text}
            <span class="author">BY {m['autore']}</span>
        </div>
        """
    
    final_html = f"{style_block}<div class='wall-container'>{content_html}</div>"
    st.components.v1.html(final_html, height=800, scrolling=True)

# Admin
st.markdown("<br><hr style='opacity:0.1'>", unsafe_allow_html=True)
with st.expander("Area Riservata"):
    if st.text_input("Password Admin", type="password") == "chatitaly123":
        if st.button("PULISCI TUTTO"):
            supabase.table("muro").delete().neq("id", 0).execute()
            st.rerun()
