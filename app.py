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

# --- 2. CSS ---
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
        text-shadow: 0 0 10px #FF00FF;
        font-size: 35px;
        font-weight: 900;
        padding: 15px;
        background: rgba(0,0,0,0.7);
    }
    .stTextInput input, .stTextArea textarea {
        background-color: rgba(0,0,0,0.8) !important;
        color: #00FF00 !important;
        border: 1px solid #444 !important;
    }
    .stButton button {
        background-color: #FF00FF !important;
        color: white !important;
        font-weight: bold !important;
        width: 100%;
    }
    /* Stile per la tabella di moderazione */
    .mod-table { color: white; background: rgba(0,0,0,0.5); padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FUNZIONI DATI ---
def carica_messaggi():
    try:
        res = supabase.table("muro").select("*").order("id", desc=True).limit(50).execute()
        return res.data
    except: return []

def elimina_messaggio(msg_id):
    try:
        supabase.table("muro").delete().eq("id", msg_id).execute()
        st.success(f"Messaggio {msg_id} eliminato!")
        st.rerun()
    except:
        st.error("Errore durante l'eliminazione")

# --- 4. INTERFACCIA UTENTE ---
st.markdown('<div class="neon-title">CHATITALY WALL</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    with st.form("spruzza_form", clear_on_submit=True):
        col_n, col_m = st.columns([1, 3])
        with col_n:
            nick_val = st.session_state.get("saved_nick", "")
            nick = st.text_input("NICK", value=nick_val, placeholder="Tag")
        with col_m:
            txt = st.text_area("MESSAGGIO", height=70, placeholder="Scrivi qui...")
        submitted = st.form_submit_button("SPRUZZA 🎨")

    if submitted and txt.strip():
        st.session_state["saved_nick"] = nick
        lunghezza = len(txt)
        if lunghezza > 100: f_size, rot, font = random.randint(14, 16), random.randint(-1, 1), "'Patrick Hand', cursive"
        elif lunghezza > 50: f_size, rot, font = random.randint(17, 20), random.randint(-2, 2), "'Patrick Hand', cursive"
        elif lunghezza > 20: f_size, rot, font = random.randint(22, 25), random.randint(-4, 4), "'Permanent Marker', cursive"
        else: f_size, rot, font = random.randint(26, 32), random.randint(-7, 7), "'Rock Salt', cursive"

        data = {"testo": txt, "autore": nick.upper() if nick.strip() else "ANONIMO", "colore": random.choice(["#39FF14", "#FF00FF", "#00FFFF", "#FFFF00", "#FF3131", "#FFFFFF"]), "font": font, "rotazione": rot, "font_size": f_size}
        try:
            supabase.table("muro").insert(data).execute()
            st.rerun()
        except: st.rerun()

# --- 5. IL MURO ---
messaggi = carica_messaggi()

if messaggi:
    scala = 0.85 if len(messaggi) > 25 else 1.0
    style_block = """
    <link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Rock+Salt&family=Patrick+Hand&display=swap" rel="stylesheet">
    <style>
        body { margin: 0; background: transparent; overflow-x: hidden; }
        .wall-container { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; padding: 30px; }
        .graffiti-box { padding: 10px; text-align: center; filter: drop-shadow(3px 3px 1px rgba(0,0,0,0.9)); white-space: pre-wrap; word-wrap: break-word; line-height: 1.2; max-width: 280px; }
        .author { display: block; font-family: sans-serif; font-size: 9px; color: #888; margin-top: 5px; text-transform: uppercase; border-top: 1px solid rgba(255,255,255,0.1); }
    </style>
    """
    content_html = ""
    for m in messaggi:
        current_size = int(m['font_size'] * scala)
        clean_text = str(m['testo']).replace("<", "&lt;")
        content_html += f'<div class="graffiti-box" style="transform: rotate({m["rotazione"]}deg); color: {m["colore"]}; font-family: {m["font"]}; font-size: {current_size}px;">{clean_text}<span class="author">BY {m["autore"]}</span></div>'
    
    st.components.v1.html(f"{style_block}<div class='wall-container'>{content_html}</div>", height=1500, scrolling=True)

# --- 6. ADMIN MODERAZIONE SELETTIVA ---
st.markdown("<br><hr style='opacity:0.1'>", unsafe_allow_html=True)
with st.expander("🛡️ Moderazione Messaggi"):
    pwd = st.text_input("Password Moderatore", type="password")
    if pwd == "chatitaly123":
        st.subheader("Gestione Graffiti")
        if st.button("Svuota tutto il muro (Reset Totale)"):
            supabase.table("muro").delete().neq("id", 0).execute()
            st.rerun()
        
        st.write("---")
        # Lista messaggi per eliminazione singola
        for m in messaggi:
            col_info, col_btn = st.columns([4, 1])
            with col_info:
                st.write(f"**{m['autore']}**: {m['testo'][:50]}...")
            with col_btn:
                if st.button(f"❌ Elimina", key=f"del_{m['id']}"):
                    elimina_messaggio(m['id'])
