import streamlit as st

from cryptography.fernet import Fernet

import base64

# --- 1. CORE ENCRYPTION LOGIC ---

def generate_key():

    return Fernet.generate_key()

def encrypt_message(message, key):

    f = Fernet(key)

    return f.encrypt(message.encode())

def decrypt_message(encrypted_message, key):

    f = Fernet(key)

    return f.decrypt(encrypted_message).decode()

# --- 2. INTERFACE SETUP ---

st.set_page_config(page_title="Secure Envelope", page_icon="🛡️")

st.title("🛡️ Secure Envelope Encryptor")

st.write("Generate a unique master key to lock and unlock private data.")

# Session State keeps the key active while you click buttons

if 'key' not in st.session_state:

    st.session_state.key = None

st.divider()

# --- 3. KEY MANAGEMENT (Two-Column Layout) ---

col1, col2 = st.columns(2)

with col1:

    if st.button("🆕 Generate Master Key", use_container_width=True):

        st.session_state.key = generate_key()

        st.success("New Key Active!")

with col2:

    if st.session_state.key:

        # This allows you to save the key as a .txt file to your PC

        st.download_button(

            label="💾 Save Key to PC",

            data=st.session_state.key,

            file_name="master_key.txt",

            mime="text/plain",

            use_container_width=True

        )

# --- 4. ENCRYPTION & DECRYPTION TOOLS ---

if st.session_state.key:

    # Shows the key currently in use

    st.info(f"**Current Session Key:** `{st.session_state.key.decode()}`")

    

    # --- Encrypt Section ---

    st.subheader("Encrypt Message")

    text_to_encrypt = st.text_area("Message to Lock:", placeholder="Enter text here...")

    

    if st.button("🔐 Generate Secure Token"):

        if text_to_encrypt:

            token = encrypt_message(text_to_encrypt, st.session_state.key)

            st.write("**Encrypted Token:**")

            st.code(token.decode(), language="text")

        else:

            st.warning("Please enter a message first.")

    st.divider()

    # --- Decrypt Section ---

    st.subheader("Decrypt Token")

    token_to_decrypt = st.text_input("Paste Token Here:")

    

    if st.button("🔓 Reveal Message"):

        if token_to_decrypt:

            try:

                decrypted = decrypt_message(token_to_decrypt.encode(), st.session_state.key)

                st.success(f"**Decrypted Content:** {decrypted}")

            except Exception:

                st.error("Decryption failed. Check if the Master Key is correct.")

        else:

            st.warning("Please paste a token first.")

else:

    st.warning("Start by generating a Master Key above.")

st.divider()

st.caption("Secure Envelope | AES-128 Encryption Interface")

```
