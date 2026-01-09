import streamlit as st
import random
from datetime import datetime

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Il Muro di Chatitaly", layout="centered")

# CSS per forzare lo sfondo scuro e lo stile dei graffiti
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .main {
        background-color: #0e1117;
    }
    .graffiti-box {
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #ff00ff;
        background-color: #1a1c24;
        margin: 15px 0px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
    }
    /* Font di riserva se Google Fonts fallisce */
    @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&display=swap');
    </style>
    """, unsafe_allow_html=True)

# --- INIZIALIZZAZIONE DATI ---
if 'muro' not in st.session_state:
    st.session_state.muro = []

colore_lista = ["#FF00FF", "#00FFFF", "#FFD700", "#ADFF2F", "#FF4500", "#00FFAB", "#FF69B4"]

# --- FUNZIONI ---
def aggiungi_messaggio():
    testo = st.session_state.temp_text
    if testo.strip():
        nuovo_post = {
            "testo": testo,
            "colore": random.choice(colore_lista),
            "ora": datetime.now().strftime("%H:%M")
        }
        st.session_state.muro.append(nuovo_post)
        st.session_state.temp_text = "" # Resetta il campo dopo l'invio

# --- INTERFACCIA ---
st.markdown("<h1 style='text-align: center; color: #FF00FF;'>🖌️ IL MURO DI CHATITALY</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Scrivi il tuo messaggio... sparirà a mezzanotte.</p>", unsafe_allow_html=True)

# Campo di Input
st.text_input("Scrivi qui e premi Invio:", key="temp_text", on_change=aggiungi_messaggio)

st.markdown("---")

# --- VISUALIZZAZIONE MESSAGGI ---
if not st.session_state.muro:
    st.info("Il muro è ancora pulito. Scrivi qualcosa sopra!")
else:
    # Mostriamo i messaggi dall'ultimo al primo
    for m in reversed(st.session_state.muro):
        st.markdown(f"""
            <div class="graffiti-box">
                <p style="font-family: 'Permanent Marker', cursive; color: {m['colore']}; font-size: 32px; margin: 0;">
                    {m['testo']}
                </p>
                <small style="color: #555;">Inviato alle {m['ora']}</small>
            </div>
            """, unsafe_allow_html=True)

# --- PANNELLO ADMIN (In fondo) ---
st.write("##")
with st.expander("🛠️ Area Admin"):
    admin_pass = st.text_input("Password di moderazione", type="password")
    if admin_pass == "chatitaly123":
        if st.button("SVUOTA TUTTO IL MURO"):
            st.session_state.muro = []
            st.rerun()
        
        st.write("Elimina messaggi singoli:")
        for i, m in enumerate(st.session_state.muro):
            if st.button(f"Elimina: {m['testo'][:20]}...", key=f"btn_{i}"):
                st.session_state.muro.pop(i)
                st.rerun()
