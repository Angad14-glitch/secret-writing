import streamlit as st
import string
import secrets
import hashlib

st.set_page_config(
    page_title="SecretVault",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at top left, #172554 0%, transparent 35%),
        radial-gradient(circle at bottom right, #312e81 0%, transparent 30%),
        #020617;
    color: #e2e8f0;
}

.hero {
    text-align: center;
    padding: 25px 10px 10px 10px;
}

.hero-title {
    font-size: 52px;
    font-weight: 900;
    letter-spacing: 2px;
    color: #f8fafc;
}

.hero-subtitle {
    font-size: 18px;
    color: #94a3b8;
    margin-top: -8px;
}

.card {
    background: rgba(15, 23, 42, 0.78);
    border: 1px solid rgba(148, 163, 184, 0.18);
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 20px;
    box-shadow: 0 10px 35px rgba(0, 0, 0, 0.25);
}

.status {
    background: rgba(30, 41, 59, 0.8);
    border-radius: 12px;
    padding: 14px;
    margin-top: 15px;
    border: 1px solid rgba(99, 102, 241, 0.3);
}

.metric {
    background: rgba(15, 23, 42, 0.8);
    border-radius: 14px;
    padding: 18px;
    text-align: center;
    border: 1px solid rgba(148, 163, 184, 0.12);
}

.metric-number {
    font-size: 30px;
    font-weight: 800;
    color: #a5b4fc;
}

.metric-label {
    font-size: 13px;
    color: #94a3b8;
}

.footer {
    text-align: center;
    color: #64748b;
    margin-top: 50px;
    padding: 20px;
    font-size: 13px;
}

div.stButton > button {
    border-radius: 10px;
    min-height: 45px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

ALPHABET = string.ascii_uppercase

def transform_text(text, key, encode=True):
    key = "".join(c for c in key.upper() if c.isalpha())

    if not key:
        return ""

    result = []
    key_index = 0

    for character in text:
        if character.isalpha():
            message_value = ord(character.upper()) - ord("A")
            key_value = ord(key[key_index % len(key)]) - ord("A")

            if encode:
                new_value = (message_value + key_value) % 26
            else:
                new_value = (message_value - key_value) % 26

            new_character = chr(new_value + ord("A"))

            if character.islower():
                new_character = new_character.lower()

            result.append(new_character)
            key_index += 1
        else:
            result.append(character)

    return "".join(result)

def generate_key(length=16):
    return "".join(
        secrets.choice(string.ascii_uppercase)
        for _ in range(length)
    )

def key_fingerprint(key):
    return hashlib.sha256(key.encode()).hexdigest()[:10].upper()

def calculate_stats(text):
    letters = sum(c.isalpha() for c in text)
    numbers = sum(c.isdigit() for c in text)
    spaces = sum(c.isspace() for c in text)
    symbols = sum(
        not c.isalnum() and not c.isspace()
        for c in text
    )
    return letters, numbers, spaces, symbols

if "generated_key" not in st.session_state:
    st.session_state.generated_key = ""

st.sidebar.markdown("## 🔐 SecretVault")

st.sidebar.write(
    "A personal message encoder built with Python."
)

st.sidebar.divider()

st.sidebar.markdown("### ⚙️ Cipher")

st.sidebar.info(
    "SecretVault uses a repeating key-based substitution cipher."
)

st.sidebar.markdown("### 🔑 Key Rules")

st.sidebar.write("• Use letters A–Z")
st.sidebar.write("• Spaces are allowed in messages")
st.sidebar.write("• The same key is required to decode")
st.sidebar.write("• Longer keys provide more variation")

st.sidebar.divider()

st.sidebar.markdown("### 🛡️ Privacy")

st.sidebar.write(
    "Your message is processed locally by this Streamlit application."
)

st.markdown("""
<div class="hero">
<div class="hero-title">
🔐 SECRET<span style="color:#818cf8;">VAULT</span>
</div>
<div class="hero-subtitle">
Turn ordinary messages into your own secret language.
</div>
</div>
""", unsafe_allow_html=True)

mode = st.radio(
    "Operation",
    [
        "🔐 Encrypt Message",
        "🔓 Decrypt Message"
    ],
    horizontal=True
)

st.write("")

if mode == "🔐 Encrypt Message":

    left, right = st.columns(2)

    with left:
        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.subheader("📝 Your Message")

        message = st.text_area(
            "Enter message",
            placeholder="Example:\nMeet me at the library at 6 PM.",
            height=230,
            label_visibility="collapsed"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.subheader("🔑 Secret Key")

        key = st.text_input(
            "Enter secret key",
            placeholder="Example: PASWAN",
            type="password"
        )

        if st.button(
            "🎲 Generate Random Key",
            use_container_width=True
        ):
            st.session_state.generated_key = generate_key(16)
            st.rerun()

        if st.session_state.generated_key:
            st.success(
                "Generated Key: " +
                st.session_state.generated_key
            )
            key = st.session_state.generated_key

        st.caption(
            "Remember this key. You need it to decrypt the message."
        )

        st.markdown("</div>", unsafe_allow_html=True)

    if st.button(
        "🔐 ENCRYPT MESSAGE",
        type="primary",
        use_container_width=True
    ):

        if not message.strip():
            st.warning("Please enter a message.")

        elif not key.strip():
            st.warning("Please enter a secret key.")

        elif not any(c.isalpha() for c in key):
            st.error("The key must contain at least one letter.")

        else:
            result = transform_text(
                message,
                key,
                encode=True
            )

            st.success("Message encrypted successfully!")

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True
            )

            st.subheader("🕵️ Encrypted Message")

            st.code(result, language=None)

            st.download_button(
                "📥 Download Encrypted Message",
                data=result,
                file_name="secret_message.txt",
                mime="text/plain",
                use_container_width=True
            )

            st.markdown("</div>", unsafe_allow_html=True)

            letters, numbers, spaces, symbols = calculate_stats(message)

            st.subheader("📊 Message Analysis")

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.markdown(
                    f"""
                    <div class="metric">
                    <div class="metric-number">{letters}</div>
                    <div class="metric-label">Letters</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c2:
                st.markdown(
                    f"""
                    <div class="metric">
                    <div class="metric-number">{numbers}</div>
                    <div class="metric-label">Numbers</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c3:
                st.markdown(
                    f"""
                    <div class="metric">
                    <div class="metric-number">{spaces}</div>
                    <div class="metric-label">Spaces</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c4:
                st.markdown(
                    f"""
                    <div class="metric">
                    <div class="metric-number">{len(result)}</div>
                    <div class="metric-label">Output Characters</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown(
                f"""
                <div class="status">
                🔑 Key fingerprint:
                <b>{key_fingerprint(key)}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

else:

    left, right = st.columns(2)

    with left:
        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.subheader("🕵️ Secret Message")

        encrypted_message = st.text_area(
            "Enter encrypted message",
            placeholder="Paste your encrypted message here...",
            height=230,
            label_visibility="collapsed"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.subheader("🔑 Secret Key")

        decrypt_key = st.text_input(
            "Enter decryption key",
            placeholder="Enter the original key",
            type="password"
        )

        st.caption(
            "Use exactly the same key that was used for encryption."
        )

        st.markdown("</div>", unsafe_allow_html=True)

    if st.button(
        "🔓 DECRYPT MESSAGE",
        type="primary",
        use_container_width=True
    ):

        if not encrypted_message.strip():
            st.warning("Please enter an encrypted message.")

        elif not decrypt_key.strip():
            st.warning("Please enter the secret key.")

        elif not any(c.isalpha() for c in decrypt_key):
            st.error("The key must contain at least one letter.")

        else:
            result = transform_text(
                encrypted_message,
                decrypt_key,
                encode=False
            )

            st.success("Message decrypted successfully!")

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True
            )

            st.subheader("📖 Original Message")

            st.code(result, language=None)

            st.download_button(
                "📥 Download Decrypted Message",
                data=result,
                file_name="original_message.txt",
                mime="text/plain",
                use_container_width=True
            )

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(
                f"""
                <div class="status">
                🔑 Key fingerprint:
                <b>{key_fingerprint(decrypt_key)}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

st.divider()

with st.expander("🧠 How SecretVault Works"):

    st.markdown("""
### 1. Enter a message

Example:

`HELLO ANGAD`

### 2. Choose a secret key

Example:

`PASWAN`

### 3. SecretVault combines the message with the key

Every alphabetic character is shifted according to the corresponding character of the key.

### 4. The same key reverses the process

The receiver needs the same key to recover the original message.

### Example

Message: HELLO

Key: KEY

The application produces a transformed message.

The cipher is designed for learning and demonstration, not for protecting sensitive real-world information.
""")

st.divider()

with st.expander("🔢 Classic A=1 to Z=26 Cipher"):

    st.write(
        "You can also use the original number-based method from your first idea."
    )

    st.code(
        "A = 1\n"
        "B = 2\n"
        "C = 3\n"
        "...\n"
        "Z = 26"
    )

    st.code(
        "HELLO\n\n"
        "8-5-12-12-15"
    )

st.markdown("""
<div class="footer">
🔐 SECRET VAULT<br>
Educational Cryptography Project<br><br>
Built with Python 🐍 + Streamlit ⚡
</div>
""", unsafe_allow_html=True)
