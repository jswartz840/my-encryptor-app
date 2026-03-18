import streamlit as st

from cryptography.fernet import Fernet

import base64

# --- 1. PROFESSIONAL RED & BLACK AESTHETIC ---

st.set_page_config(page_title="AES Security Console", page_icon="🔴")

st.markdown("""

    <style>

    .stApp {

        background-color: #000000;

        color: #FFFFFF;

    }

    h1, h2, h3 {

        color: #FF0000 !important;

        font-family: 'Courier New', Courier, monospace;

        text-transform: uppercase;

        letter-spacing: 2px;

    }

    .stButton>button {

        background-color: #FF0000;

        color: white;

        border-radius: 2px;

        border: 1px solid #8B0000;

        width: 100%;

        font-weight: bold;

    }

    .stButton>button:hover {

        background-color: #8B0000;

        border: 1px solid #FF0000;

    }

    .stTextInput>div>div>input, .stTextArea>div>div>textarea {

        background-color: #1A1A1A;

        color: #00FF00;

        border: 1px solid #FF0000;

        font-family: 'Courier New', monospace;

    }

    .stInfo {

        background-color: #1A0000;

        color: #FF0000;

        border: 1px solid #FF0000;

    }

    </style>

    """, unsafe_allow_html=True)

# --- 2. CORE SECURITY LOGIC ---

def generate_key():

    return Fernet.generate_key()

def encrypt_message(message, key):

    f = Fernet(key)

    return f.encrypt(message.encode())

def decrypt_message(encrypted_message, key):

    f = Fernet(key)

    return f.decrypt(encrypted_message).decode()

# --- 3. SIDEBAR: APP CAPABILITIES & BOASTING ---

with st.sidebar:

    st.title("🔴 SYSTEM SPECS")

    st.markdown("### **Professional Features:**")

    st.info("🛡️ **AES-128 Bit Encryption**\nIndustry-standard symmetric-key algorithm.")

    st.info("🔑 **Dynamic Key Generation**\nUnique cryptographic keys for every session.")

    st.info("☣️ **Zero-Persistence**\nKeys are held in volatile RAM (Session State) only.")

    st.info("🎨 **High-Contrast UI**\nOptimized for low-light security environments.")

    

    st.divider()

    st.markdown("### **Project Scope:**")

    st.write("This application demonstrates competency in Python-based cryptography and secure interface design.")

# --- 4. MAIN INTERFACE ---

st.title("🛡️ SECURE ENVELOPE v3.0")

st.write("Advanced Cryptographic Interface")

if 'key' not in st.session_state:

    st.session_state.key = None

st.divider()

# KEY MANAGEMENT

col1, col2 = st.columns(2)

with col1:

    if st.button("🆕 GENERATE MASTER KEY"):

        st.session_state.key = generate_key()

        st.success("NEW KEY ACTIVE")

with col2:

    if st.session_state.key:

        st.download_button(

            label="💾 EXPORT KEY (.txt)",

            data=st.session_state.key,

            file_name="master_key.txt",

            mime="text/plain"

        )

if st.session_state.key:

    st.info(f"**ACTIVE SESSION KEY:** `{st.session_state.key.decode()}`")

    

    st.divider()

    

    # ENCRYPT/DECRYPT TOOLS

    tab1, tab2 = st.tabs(["ENCRYPT PAYLOAD", "DECRYPT TOKEN"])

    

    with tab1:

        st.subheader("LOCK DATA")

        msg = st.text_area("Plaintext Input", placeholder="Enter sensitive data...")

        if st.button("EXECUTE ENCRYPTION"):

            if msg:

                token = encrypt_message(msg, st.session_state.key)

                st.code(token.decode(), language="text")

            else:

                st.warning("Input required.")

                

    with tab2:

        st.subheader("UNLOCK DATA")

        token_in = st.text_input("Encrypted Token Input")

        if st.button("EXECUTE DECRYPTION"):

            if token_in:

                try:

                    decoded = decrypt_message(token_in.encode(), st.session_state.key)

                    st.success(f"PAYLOAD RECOVERED: {decoded}")

                except:

                    st.error("DECRYPTION FAILED: Invalid Token or Key")

else:

    st.warning("SYSTEM STANDBY: Please generate a Master Key to initialize.")

st.divider()

st.caption("SECURE ENVELOPE | AES-128 | PYTHON 3.x")
