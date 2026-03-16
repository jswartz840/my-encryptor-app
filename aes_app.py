import streamlit as st
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# This function turns your password into a secure key
def generate_key(password: str):
    salt = b'\x00' * 16 
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Cyber Lab Encryptor", page_icon="🔐")
st.title("🔐 Professional AES Encryptor")
st.write("Enter a password and a message to securely encrypt or decrypt data.")

# User Inputs
pass_input = st.text_input("Enter Master Password:", type="password")
message = st.text_area("Message to process (Text or Encrypted Token):")

if pass_input and message:
    # Setup the encryption engine
    key = generate_key(pass_input)
    f = Fernet(key)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Encrypt"):
            # Logic for Encrypting
            token = f.encrypt(message.encode())
            encrypted_text = token.decode()
            
            st.success("Message Encrypted!")
            st.code(encrypted_text, language="text")
            
            # --- THE DOWNLOAD BUTTON SPLICE ---
            st.download_button(
                label="📥 Download Encrypted File",
                data=encrypted_text,
                file_name="secret_message.txt",
                mime="text/plain"
            )

    with col2:
        if st.button("Decrypt"):
            # Logic for Decrypting
            try:
                decoded = f.decrypt(message.encode())
                st.info("Message Decrypted:")
                st.write(decoded.decode())
            except Exception:
                st.error("Error: Check your password or the encrypted code.")
else:
    st.info("Waiting for password and message input...")