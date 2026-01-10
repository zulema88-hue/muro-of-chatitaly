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

st.set_page_config(page_title="Urban Wall Fix", layout="wide", initial_sidebar_state="collapsed")

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
    [data-testid="stSidebar"], .st-emotion-cache-10o1ihd, footer, header { display: none !important; }
    .stApp {
        background-image: url("https://static.vecteezy.com/system/resources/previews/007/233/624/non_2x/brick-black-wall-texture-background-dark-brick-wall-realistic-template-abstract-modern-wallpaper-design-illustration-vector.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    ::-webkit-scrollbar { width: 0px; }
    * { scrollbar-width: none; }
    
    .neon-header {
        font-family: 'Rock Salt', cursive;
        text-align: center;
        color: #fff;
        text-shadow: 0 0 15px #FF00FF;
        font-size: 28px;
        padding: 10px;
    }
    
    .stForm {
        background: rgba(0,0,0,0.8) !important;
        border: 2px solid #00FFFF !important;
        border-radius: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNZIONI ---
def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).limit(40).execute()
        return res.data
    except: return []

# --- 5. INPUT ---
st.markdown('<div class="neon-header">CHATITALY URBAN WALL</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
with c2:
    with st.form("spray_form", clear_on_submit=True):
        col_n, col_m = st.columns([1, 2])
        nick = col_n.text_input("TAG", placeholder="Chi sei?")
        txt = col_m.text_area("MESSAGGIO", height=65, placeholder="Spruzza qui...")
        submitted = st.form_submit_button("💨 BOMB THE WALL!")

    if submitted and txt.strip():
        st.session_state["saved_nick"] = nick
        l = len(txt)
        if l < 10: f_size, rot, font = random.randint(32, 42), random.randint(-12, 12), "'Rock Salt', cursive"
        elif l < 50: f_size, rot, font = random.randint(22, 28), random.randint(-7, 7), "'Permanent Marker', cursive"
        else: f_size, rot, font = random.randint(16, 20), random.randint(-3, 3), "'Patrick Hand', cursive"

        data = {
            "testo": txt, "autore": nick.upper() if nick.strip() else "ANONIMO",
            "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF"]),
            "font": font, "rotazione": rot, "font_size": f_size
        }
        try:
            supabase.table("muro").insert(data).execute()
            st.rerun()
        except: st.rerun()

# --- 6. IL MURO (VERSIONE STABILE) ---
messaggi = carica_messaggi()
if messaggi:
    style_block = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Patrick+Hand&display=swap" rel="stylesheet">
    <style>
        .wall-grid {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 40px;
            padding: 50px;
            width: 100%;
        }

        .graffito-wrapper {
            position: relative;
            min-width: 200px;
            max-width: 350px;
            display: flex;
            flex-direction: column;
            align-items: center;
            animation: sprayIn 0.8s ease-out forwards;
        }

        @keyframes sprayIn {
            0% { opacity: 0; filter: blur(10px); transform: scale(0.8); }
            100% { opacity: 1; filter: blur(0px); transform: scale(1); }
        }

        .graffito-box {
            padding: 15px;
            text-align: center;
            white-space: pre-wrap;
            word-wrap: break-word;
            line-height: 1.3;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.9);
            width: 100%; /* Forza il box a non collassare */
        }

        .drip {
            width: 3px;
            background: currentColor;
            opacity: 0.6;
            border-radius: 0 0 3px 3px;
            margin: -5px auto 0 auto; /* Fa partire la goccia dal fondo del testo */
        }

        .tag-label { 
            font-family: sans-serif; 
            font-size: 10px; 
            color: rgba(255,255,255,0.4); 
            margin-top: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
    </style>
    """
    
    content_html = ""
    for i, m in enumerate(messaggi):
        random.seed(m['id'])
        rot = m["rotazione"]
        # Calcolo goccia separato per non influenzare il box del testo
        drip_h = random.randint(20, 60) if (len(m['testo']) < 30 and random.random() > 0.6) else 0
        drip_html = f'<div class="drip" style="height: {drip_h}px; color: {m["colore"]};"></div>' if drip_h > 0 else ""
        
        content_html += f'''
        <div class="graffito-wrapper" style="transform: rotate({rot}deg);">
            <div class="graffito-box" style="color: {m["colore"]}; font-family: {m["font"]}; font-size: {m["font_size"]}px;">
                {m["testo"].replace("<","&lt;")}
            </div>
            {drip_html}
            <div class="tag-label">BY {m["autore"]}</div>
        </div>
        '''
    
    st.components.v1.html(f"{style_block}<div class='wall-grid'>{content_html}</div>", height=2000, scrolling=False)

# --- 7. ADMIN ---
with st.expander("MOD"):
    if st.text_input("Psw", type="password") == "chatitaly123":
        for m in messaggi:
            col_a, col_b = st.columns([4,1])
            col_a.write(f"{m['autore']}: {m['testo'][:20]}")
            if col_b.button("🗑️", key=f"d_{m['id']}"):
                supabase.table("muro").delete().eq("id", m['id']).execute()
                st.rerun()
