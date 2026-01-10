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

st.set_page_config(page_title="Urban Wall Pro", layout="wide", initial_sidebar_state="collapsed")

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
    /* Nasconde elementi di Streamlit indesiderati */
    [data-testid="stSidebar"], .st-emotion-cache-10o1ihd, footer, header { display: none !important; }
    
    /* Sfondo del muro */
    .stApp {
        background-image: url("https://static.vecteezy.com/system/resources/previews/007/233/624/non_2x/brick-black-wall-texture-background-dark-brickwork-pattern-block-stone-structure-backdrop-dark-brick-wall-realistic-template-abstract-modern-wallpaper-design-illustration-vector.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Nasconde scrollbar */
    ::-webkit-scrollbar { width: 0px; }
    * { scrollbar-width: none; }
    
    /* Stile Titolo */
    .neon-header {
        font-family: 'Rock Salt', cursive;
        text-align: center;
        color: #fff;
        text-shadow: 0 0 10px #FF00FF; /* Un bagliore iniziale */
        font-size: 30px;
        padding: 15px;
        background: rgba(0,0,0,0.6); /* Sfondo semi-trasparente */
        margin-bottom: 20px;
        border-bottom: 2px solid #00FFFF;
    }
    
    /* Stile Form */
    .stForm {
        background: rgba(0,0,0,0.7) !important;
        border: 2px solid #00FFFF !important;
        border-radius: 10px !important;
        padding: 15px !important;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
    }
    .stTextInput input, .stTextArea textarea {
        background-color: rgba(0,0,0,0.7) !important;
        color: #39FF14 !important;
        border: 1px solid #444 !important;
        border-radius: 5px !important;
    }
    .stButton button {
        background: linear-gradient(45deg, #FF00FF, #00FFFF) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        box-shadow: 0 0 10px rgba(255, 0, 255, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNZIONI ---
def carica_messaggi():
    try:
        # Carichiamo gli ultimi 40 messaggi, li invertiamo per vederli dal più vecchio al più nuovo sulla griglia
        res = supabase.table("muro").select("*").order("id", desc=True).limit(40).execute()
        return res.data
    except: return []

# --- 5. INPUT ---
st.markdown('<div class="neon-header">CHATITALY URBAN WALL</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
with c2:
    with st.form("spray_form", clear_on_submit=True):
        col_n, col_m = st.columns([1, 2])
        nick_val = st.session_state.get("saved_nick", "")
        nick = col_n.text_input("TAG", value=nick_val, placeholder="Il tuo tag")
        txt = col_m.text_area("MESSAGGIO", height=65, placeholder="Spruzza la tua idea...")
        submitted = st.form_submit_button("💨 BOMB THE WALL!")

    if submitted and txt.strip():
        st.session_state["saved_nick"] = nick
        l = len(txt)
        # Logica per dimensione e font basata sulla lunghezza del testo
        if l < 10: f_size, rot, font = random.randint(32, 40), random.randint(-10, 10), "'Rock Salt', cursive"
        elif l < 50: f_size, rot, font = random.randint(22, 28), random.randint(-5, 5), "'Permanent Marker', cursive"
        else: f_size, rot, font = random.randint(16, 20), random.randint(-2, 2), "'Patrick Hand', cursive"

        data = {
            "testo": txt, "autore": nick.upper() if nick.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF"]),
            "font": font, "rotazione": rot, "font_size": f_size
        }
        try:
            supabase.table("muro").insert(data).execute()
            st.rerun()
        except: st.rerun()

# --- 6. IL MURO (GRAFICA TIPO IMMAGINE) ---
messaggi = carica_messaggi()
if messaggi:
    style_block = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Patrick+Hand&display=swap" rel="stylesheet">
    <style>
        .graffiti-grid-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); /* 200px min per box, si espande */
            gap: 25px; /* Spazio tra i box */
            padding: 30px;
            max-width: 1200px; /* Limite per non essere troppo largo su schermi grandi */
            margin: auto; /* Centra la griglia */
        }

        @keyframes fadeInDrop {
            0% { opacity: 0; transform: translateY(-20px) scale(0.8); filter: blur(10px); }
            100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0px); }
        }

        .graffito-card {
            background-color: rgba(255, 255, 255, 0.1); /* Sfondo box semi-trasparente */
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            min-height: 150px; /* Altezza minima per i box */
            text-align: center;
            position: relative;
            overflow: hidden; /* Nasconde ciò che esce dal box */
            animation: fadeInDrop 0.8s ease-out forwards;
        }

        .graffito-text {
            white-space: pre-wrap;
            word-wrap: break-word;
            line-height: 1.2;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.6); /* Ombra per leggibilità */
            color: var(--text-color); /* Colore dinamico */
            font-family: var(--font-family);
            font-size: var(--font-size);
            transform: rotate(var(--rotation-deg));
            flex-grow: 1; /* Permette al testo di occupare spazio */
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
        }

        .tag-name {
            font-family: sans-serif;
            font-size: 11px;
            color: rgba(255, 255, 255, 0.5);
            margin-top: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-top: 1px solid rgba(255,255,255,0.1);
            padding-top: 5px;
            width: 80%;
        }

        .drip-effect {
            position: absolute;
            bottom: 0;
            width: 60%; /* Larghezza della 'base' della goccia */
            height: 20px; /* Altezza della parte visibile della goccia */
            background-color: var(--drip-color);
            border-radius: 0 0 50% 50%; /* Forma della goccia */
            left: 20%;
            opacity: 0.8;
            filter: blur(1px);
            box-shadow: 0 0 10px var(--drip-color); /* Bagliore della goccia */
        }

        /* Goccioline aggiuntive */
        .drip-effect::before, .drip-effect::after {
            content: '';
            position: absolute;
            background-color: var(--drip-color);
            border-radius: 50%;
            opacity: 0.7;
            filter: blur(0.5px);
        }
        .drip-effect::before {
            width: 8px; height: 15px; left: 10%; top: 50%;
            transform: rotate(-15deg);
        }
        .drip-effect::after {
            width: 10px; height: 18px; right: 15%; top: 40%;
            transform: rotate(10deg);
        }
    </style>
    """
    
    content_html = ""
    for i, m in enumerate(messaggi):
        # Le posizioni random non servono più, ma teniamo la rotazione
        rot = m["rotazione"]
        
        # Le gocce appaiono sempre, ma con forma e colore coordinato
        drip_color = m["colore"] + 'CC' # Un po' più trasparente
        
        content_html += f'''
        <div class="graffito-card">
            <div class="graffito-text" style="
                --text-color: {m["colore"]}; 
                --font-family: {m["font"]}; 
                --font-size: {m["font_size"]}px; 
                --rotation-deg: {rot}deg;">
                {m["testo"].replace("<","&lt;")}
            </div>
            <div class="drip-effect" style="--drip-color: {drip_color};"></div>
            <span class="tag-name">@{m["autore"]}</span>
        </div>
        '''
    
    st.components.v1.html(f"{style_block}<div class='graffiti-grid-container'>{content_html}</div>", height=2000, scrolling=False)

# --- 7. ADMIN ---
with st.expander("MOD"):
    if st.text_input("Psw", type="password") == "chatitaly123":
        for m in messaggi:
            col_a, col_b = st.columns([4,1])
            col_a.write(f"{m['autore']}: {m['testo'][:20]}")
            if col_b.button("🗑️", key=f"d_{m['id']}"):
                supabase.table("muro").delete().eq("id", m['id']).execute()
                st.rerun()
