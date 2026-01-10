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

st.set_page_config(page_title="Urban Wall", layout="wide", initial_sidebar_state="collapsed")

def random_neon():
    # Colori neon vibranti ma solidi
    palette = ["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF", "#FFD700", "#FF4500", "#7B68EE"]
    return random.choice(palette)

# --- 2. CSS ---
st.markdown("""
    <style>
    header, footer, [data-testid="stSidebar"], [data-testid="stHeader"] { display: none !important; }
    .stApp {
        background-color: #050505;
        background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("https://www.transparenttextures.com/patterns/dark-brick-wall.png");
        background-attachment: fixed;
    }
    .graffiti-title {
        font-family: 'Rock Salt', cursive; text-align: center; color: white;
        font-size: 45px; padding: 20px; text-shadow: 0 0 15px #FF00FF;
    }
    .stForm { background: rgba(0,0,0,0.85) !important; border: 1px solid #333 !important; border-radius: 15px !important; }
    
    /* BOMBOLETTE */
    .can { width: 40px; height: 90px; border-radius: 6px; border: 2px solid #111; position: relative; }
    .mist { position: absolute; width: 100px; height: 100px; filter: blur(40px); opacity: 0.4; border-radius: 50%; }
    
    ::-webkit-scrollbar { width: 0px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INPUT ---
st.markdown('<div class="graffiti-title">CHATITALY URBAN WALL</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns([0.2, 0.6, 0.2])

with c1:
    st.markdown(f'<div style="position:relative; margin-left:auto;"><div class="mist" style="background:#00FFFF; top:-10px;"></div><div class="can" style="background:linear-gradient(#00FFFF, #005555); transform:rotate(-12deg); margin-left:auto;"></div></div>', unsafe_allow_html=True)

with c2:
    with st.form("bomb", clear_on_submit=True):
        col_tag, col_msg = st.columns([1, 2])
        nick = col_tag.text_input("TAG")
        txt = col_msg.text_area("MESSAGGIO")
        if st.form_submit_button("💨 BOMB THE WALL"):
            if txt.strip():
                l = len(txt)
                f, s = ("'Rock Salt'", 36) if l < 20 else ("'Permanent Marker'", 26) if l < 60 else ("'Gochi Hand'", 22)
                supabase.table("muro").insert({
                    "testo": txt, "autore": nick.upper() or "ANONIMO",
                    "colore": random_neon(), "font": f, "rotazione": random.randint(-5, 5), "font_size": s
                }).execute()
                st.rerun()

with c3:
    st.markdown(f'<div style="position:relative;"><div class="mist" style="background:#FF00FF; top:-10px;"></div><div class="can" style="background:linear-gradient(#FF00FF, #550055); transform:rotate(12deg);"></div></div>', unsafe_allow_html=True)

# --- 4. IL MURO (GRIGLIA SPARPARGLIATA MA LEGGIBILE) ---
res = supabase.table("muro").select("*").order("id", desc=True).limit(60).execute()
messaggi = res.data

if messaggi:
    style = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Gochi+Hand&display=swap" rel="stylesheet">
    <style>
        .wall-grid { 
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 40px;
            padding: 40px;
            align-items: center;
        }
        .graffito-card { 
            position: relative; 
            display: flex; 
            flex-direction: column; 
            align-items: center;
            padding: 20px;
            margin: var(--rand-m);
        }
        .splat-effect { 
            position: absolute; width: 180px; height: 180px; 
            filter: blur(50px); opacity: 0.2; z-index: 1; 
            background: var(--c);
        }
        .text-spray { 
            text-align: center; 
            z-index: 2; 
            /* Ombra naturale, niente bordini neri strani */
            text-shadow: 1px 1px 3px rgba(0,0,0,0.8), 0 0 10px var(--c);
            line-height: 1.2;
            word-wrap: break-word;
        }
        .drip-classic { width: 3px; height: 35px; margin-top: 5px; border-radius: 0 0 10px 10px; z-index: 2; opacity: 0.7; }
        .tag-name { color: rgba(255,255,255,0.3); font-size: 10px; margin-top: 10px; font-family: sans-serif; }
    </style>
    """
    
    html_content = ""
    for m in messaggi:
        random.seed(m['id']) 
        c = m.get('colore', random_neon())
        # Spostamento leggero per rompere la simmetria senza sovrapporre tutto
        rand_m = f"{random.randint(0,30)}px {random.randint(0,30)}px"
        
        html_content += f'''
        <div class="graffito-card" style="--c: {c}; --rand-m: {rand_m};">
            <div class="splat-effect"></div>
            <div class="text-spray" style="color: {c}; font-family: {m['font']}; font-size: {m['font_size']}px; transform: rotate({m['rotazione']}deg);">
                {m['testo'].replace("<","&lt;")}
            </div>
            <div class="drip-classic" style="background: {c}; box-shadow: 0 0 8px {c};"></div>
            <div class="tag-name">@{m['autore']}</div>
        </div>
        '''
    
    st.components.v1.html(f"{style}<div class='wall-grid'>{html_content}</div>", height=2000, scrolling=True)

# --- 5. ADMIN ---
with st.expander("MOD"):
    if st.text_input("Psw", type="password") == "chatitaly123":
        for m in messaggi:
            if st.button(f"X {m['id']}", key=f"d_{m['id']}"):
                supabase.table("muro").delete().eq("id", m['id']).execute()
                st.rerun()
