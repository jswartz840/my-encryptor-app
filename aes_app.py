import streamlit as st
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# 1. Page Configuration (MUST be the first Streamlit command)
st.set_page_config(page_title="CyberShield", layout="wide")

# 2. Custom CSS for Dark/Professional Theme (Black and Red Accents)
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    h1, h2, h3 {
        color: #ff4b4b !important; /* Professional Red */
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Reset Functionality using Session State
if 'reset_key' not in st.session_state:
    st.session_state.reset_key = 0

def reset_app():
    st.session_state.reset_key += 1

# 4. Professional Portfolio Header
st.markdown("""
# 🛡️ Cybersecurity Research Tool
### Penetration Testing & Ethical Hacking Framework

This application is a specialized tool designed for secure data handling. 
It is part of a larger project within my **Cyber Lab** environment, focusing on 
secure data handling and cryptographic principles.
---
""")

# 5. Secure Key Derivation Logic
def generate_key(password: str):
    # Salt should ideally be random and stored, but using a fixed salt for this lab tool
    salt = b'\x00' * 16 
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    # Ensure password is encoded to bytes
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

# 6. Main UI
st.title("🔐 Professional AES Encryptor")
st.write("Enter a password and a message to securely encrypt or decrypt data.")

# Wrap inputs in a container that uses the reset_key to refresh on demand
with st.container():
    pass_input = st.text_input("Enter Master Password", type="password", key=f"pass_{st.session_state.reset_key}")
    message_input = st.text_area("Message to Process", key=f"msg_{st.session_state.reset_key}")

    if pass_input and message_input:
        clean_message = message_input.strip()
        
        # Generate the Fernet key from the password
        key = generate_key(pass_input)
        f = Fernet(key)

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Encrypt"):
                try:
                    token = f.encrypt(clean_message.encode())
                    encrypted_text = token.decode()
                    st.success("Message Encrypted!")
                    st.code(encrypted_text, language="text")
                    st.download_button(
                        label="📥 Download Encrypted Text",
                        data=encrypted_text,
                        file_name="secret_message.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"Encryption failed: {e}")

        with col2:
            if st.button("Decrypt"):
                try:
                    decoded_token = f.decrypt(clean_message.encode())
                    decrypted_text = decoded_token.decode()
                    st.success("Message Decrypted!")
                    st.info(decrypted_text)
                except Exception:
                    st.error("Decryption failed. Check your password or the encrypted string.")

        with col3:
            if st.button("Clear / Reset"):
                reset_app()
                st.rerun()

# 7. Project Features Footer
st.markdown("---")
st.subheader("🔍 Project Features:")
st.markdown("""
* **Secure Encryption:** Implementing robust AES-256 via the Fernet (cryptography) library.
* **Vulnerability Analysis:** Tools designed to demonstrate secure vs. insecure data transit.
* **Ethical Hacking Context:** Developed as a proof-of-concept for secure communication in red-team scenarios.
""")
