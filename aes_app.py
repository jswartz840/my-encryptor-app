import streamlit as st

from cryptography.fernet import Fernet

import base64

# --- CORE ENCRYPTION LOGIC ---

def generate_key():

    return Fernet.generate_key()

def encrypt_message(message, key):

    f = Fernet(key)

    return f.encrypt(message.encode()).decode()

def decrypt_message(encrypted_message, key):

    f = Fernet(key)

    return f.decrypt(encrypted_message.encode()).decode()

# --- INTERFACE SETUP ---

st.set_page_config(page_title="Secure Envelope", page_icon="🔐")

st.title("🔐 Secure Envelope Encryptor")

# Initialize session state variables

if 'key' not in st.session_state:

    st.session_state.key = None

if 'encrypted_token' not in st.session_state:

    st.session_state.encrypted_token = None

st.write("Generate a unique master key to lock and unlock private data.")

# --- KEY MANAGEMENT ---

col1, col2 = st.columns(2)

with col1:

    if st.button("Generate Master Key", use_container_width=True):

        st.session_state.key = generate_key()

        st.success("New Key Active!")

with col2:

    if st.session_state.key:

        st.download_button(

            label="Save Key to PC",

            data=st.session_state.key,

            file_name="master_key.txt",

            mime="text/plain",

            use_container_width=True

        )

if st.session_state.key:

    st.info(f"Current Session Key: `{st.session_state.key.decode()}`")

else:

    st.warning("No Master Key active. Generate one above to begin.")

st.divider()

# --- ENCRYPTION SECTION ---

st.subheader("🛡️ Encrypt Section")

text_to_encrypt = st.text_area("Message to Lock", placeholder="Enter text here...")

if st.button("Generate Secure Token"):

    if not st.session_state.key:

        st.error("Error: You must generate a Master Key first!")

    elif text_to_encrypt:

        try:

            token = encrypt_message(text_to_encrypt, st.session_state.key)

            st.session_state.encrypted_token = token

            st.success("Message Encrypted!")

        except Exception as e:

            st.error(f"Encryption failed: {e}")

    else:

        st.warning("Please enter a message first.")

if st.session_state.encrypted_token:

    st.code(st.session_state.encrypted_token, language="text")

st.divider()

# --- DECRYPTION SECTION ---

st.subheader("🔓 Decrypt Section")

token_to_decrypt = st.text_input("Paste Token Here", placeholder="Paste encrypted token...")

if st.button("Reveal Message"):

    if not st.session_state.key:

        st.error("Error: Master Key missing.")

    elif token_to_decrypt:

        try:

            decrypted = decrypt_message(token_to_decrypt, st.session_state.key)

            st.success(f"**Decrypted Content:** {decrypted}")

        except Exception:

            st.error("Decryption failed. Ensure the Master Key matches the token.")

    else:

        st.warning("Please paste a token first.")

```
