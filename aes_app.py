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

# --- 2. STREAMLIT UI SETUP ---

st.set_page_config(page_title="Secure Envelope Encryptor", page_icon="🛡️")

st.title("🛡️ Secure Envelope Encryptor")

st.markdown("### Personal Cybersecurity Project")

if 'key' not in st.session_state:

    st.session_state.key = None

st.divider()

# --- 3. KEY MANAGEMENT ---

col1, col2 = st.columns(2)

with col1:

    if st.button("🆕 Generate Master Key", use_container_width=True):

        st.session_state.key = generate_key()

        st.success("New Key Generated!")

with col2:

    if st.session_state.key:

        st.download_button(

            label="💾 Save Key to PC",

            data=st.session_state.key,

            file_name="master_key.txt",

            mime="text/plain",

            use_container_width=True

        )

# --- 4. ENCRYPTION & DECRYPTION INTERFACE ---

if st.session_state.key:

    st.info(f"**Active Session Key:** `{st.session_state.key.decode()}`")

    

    st.subheader("Step 1: Encrypt a Message")

    text_to_encrypt = st.text_area("Enter the private message:", placeholder="Type here...")

    

    if st.button("🔐 Encrypt Now"):

        if text_to_encrypt:

            token = encrypt_message(text_to_encrypt, st.session_state.key)

            st.write("**Your Encrypted Token:**")

            st.code(token.decode(), language="text")

        else:

            st.warning("Please enter a message to encrypt.")

    st.divider()

    st.subheader("Step 2: Decrypt a Token")

    token_to_decrypt = st.text_input("Paste the encrypted token here:")

    

    if st.button("🔓 Decrypt Now"):

        if token_to_decrypt:

            try:

                decrypted = decrypt_message(token_to_decrypt.encode(), st.session_state.key)

                st.success(f"**Decrypted Message:** {decrypted}")

            except Exception:

                st.error("Decryption failed. Please ensure the Key and Token match.")

        else:

            st.warning("Please paste a token first.")

else:

    st.warning("Please click 'Generate Master Key' to begin using the encryptor.")

st.divider()

st.caption("Secure Envelope Encryptor | Personal Python Project")

```
