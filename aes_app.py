import streamlit as st
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# 1. Page configuration (Must be first)
st.set_page_config(page_title="Cyber Lab Encryptor", page_icon="🔐")

# 2. Reset Functionality using Session State
if 'reset_key' not in st.session_state:
    st.session_state.reset_key = 0

def reset_app():
    st.session_state.reset_key += 1

# 3. Professional Portfolio Header
st.markdown("""
# 🛡️ Cybersecurity Research Tool
### Penetration Testing & Ethical Hacking Framework

This application is a specialized tool designed to demonstrate core security concepts. 
It is part of a larger project within my **Cybersecurity** curriculum, focusing on 
secure data handling and cryptographic principles.

---

### 🔍 Project Features:
* **Secure Encryption:** Implementing robust algorithms to protect data integrity.
* **Vulnerability Analysis:** Tools designed for educational security assessments.
* **Technical Documentation:** A practical application of ethical hacking methodologies.

> **Note:** This tool is intended for **authorized educational use only**. Always ensure 
> you have explicit permission before performing any security testing.

---
""")

# 4. Secure Key Derivation Logic
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

# 5. Main UI with dynamic reset key
st.title("🔐 Professional AES Encryptor")
st.write("Enter a password and a message to securely encrypt or decrypt data.")

# Wrap inputs in a container that refreshes on reset
with st.container():
    pass_input = st.text_input("Enter Master Password:", type="password", key=f"pass_{st.session_state.reset_key}")
    message_input = st.text_area("Message to process (Text or Encrypted Token):", key=f"msg_{st.session_state.reset_key}")

# 6. The Logic Gate
if pass_input and message_input:
    # .strip() handles the mobile copy-paste space issue
    clean_message = message_input.strip()
    
    key = generate_key(pass_input)
    f = Fernet(key)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Encrypt"):
            token = f.encrypt(clean_message.encode())
            encrypted_text = token.decode()
            st.success("Message Encrypted!")
            st.code(encrypted_text, language="text")
            st.download_button(
                label="📥 Download",
                data=encrypted_text,
                file_name="secret_message.txt",
                mime="text/plain"
            )

    with col2:
        if st.button("Decrypt"):
            try:
                decoded = f.decrypt(clean_message.encode())
                st.info("Message Decrypted:")
                st.success(decoded.decode())
            except Exception:
                st.error("Error: Check your password or token.")

    with col3:
        # The Reset Button
        st.button("🧹 Clear All", on_click=reset_app)
else:
    st.info("Waiting for password and message input...")
    if st.button("🧹 Clear All", on_click=reset_app):
        pass
