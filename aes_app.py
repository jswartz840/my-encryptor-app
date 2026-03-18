
import streamlit as st

import os

from cryptography.fernet import Fernet

from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import base64

# --- 1. RED AND BLACK THEME (CUSTOM CSS) ---

st.markdown("""

    <style>

    .stApp {

        background-color: #000000;

        color: #FFFFFF;

    }

    h1, h2, h3 {

        color: #FF0000 !important;

    }

    .stButton>button {

        background-color: #FF0000;

        color: white;

        border-radius: 5px;

        border: none;

    }

    .stButton>button:hover {

        background-color: #8B0000;

        color: white;

    }

    </style>

    """, unsafe_allow_html=True)

# --- 2. CORE ENCRYPTION LOGIC (SECURE DERIVATION) ---

def derive_key(password: str, salt: bytes):

    kdf = PBKDF2HMAC(

        algorithm=hashes.SHA256(),

        length=32,

        salt=salt,

        iterations=100000,

    )

    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

# --- 3. INTERFACE & FEATURES ---

st.title("🔴 Professional AES Encryptor")

st.subheader("Cybersecurity Research Tool")

if 'salt' not in st.session_state:

    st.session_state.salt = os.urandom(16)

pass_input = st.text_input("Enter Master Password", type="password")

col1, col2 = st.columns(2)

with col1:

    msg = st.text_area("Message to Encrypt")

    if st.button("Encrypt Message"):

        if pass_input and msg:

            key = derive_key(pass_input, st.session_state.salt)

            f = Fernet(key)

            token = f.encrypt(msg.encode())

            st.code(token.decode(), language="text")

        else:

            st.warning("Password and Message required.")

with col2:

    token_in = st.text_area("Token to Decrypt")

    if st.button("Decrypt Message"):

        if pass_input and token_in:

            try:

                key = derive_key(pass_input, st.session_state.salt)

                f = Fernet(key)

                decoded = f.decrypt(token_in.encode()).decode()

                st.success(f"Decrypted: {decoded}")

            except:

                st.error("Decryption failed. Check password/token.")

st.divider()

# FEATURE: Clear All Button

if st.button("Clear All Data"):

    st.rerun()

st.caption("Developed for Cybersecurity Competency Research")
