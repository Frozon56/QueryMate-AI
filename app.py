import html
import streamlit as st
from modules.internet import check_internet
from auth.auth import create_users_table, register_user, login_user
from modules.pdf_parser import extract_text_from_pdf
from modules.local_llm import ask_llm
from modules.speech_to_text import listen
from modules.text_to_speech import speak
from modules.history import (
    create_history_table,
    save_history,
    get_history
)

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    
    page_title="QueryMate",
    page_icon="📄",
    layout="wide"
)

# ============================================
# DATABASE
# ============================================

create_users_table()
create_history_table()

# ============================================
# SESSION STATE
# ============================================

defaults = {
    "logged_in": False,
    "pdf_text": "",
    "voice_query": "",
    "last_answer": "",
    "last_query": "",
    "language": "English",
    "username": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>

/* GLOBAL */
html, body, [class*="css"]{
    font-family: 'Segoe UI', sans-serif;
}

.stApp{
    background: linear-gradient(135deg,#0b1120,#172554,#1e293b);
    color: white;
}

header{ visibility: hidden; }

.block-container{
    padding-top: 1.5rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 1400px;
}

/* SIDEBAR */
section[data-testid="stSidebar"]{
    background: #06122b;
    border-right: 1px solid rgba(255,255,255,0.06);
    width: 320px !important;
}

/* LOGO */
.logo-text{
    text-align: center;
    color: white;
    font-size: 40px;
    font-weight: 800;
}

.logo-sub{
    text-align: center;
    color: #94a3b8;
    margin-bottom: 25px;
}

/* USER CARD */
.user-card{
    background: rgba(255,255,255,0.06);
    border-radius: 24px;
    padding: 28px;
    text-align: center;
    margin-bottom: 25px;
    border: 1px solid rgba(255,255,255,0.06);
}

.avatar{
    width: 85px;
    height: 85px;
    border-radius: 50%;
    background: linear-gradient(135deg,#06b6d4,#2563eb);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: auto;
    color: white;
    font-size: 34px;
    font-weight: bold;
    margin-bottom: 15px;
}

/* BUTTONS */
.stButton > button{
    width: 100%;
    border: none;
    border-radius: 14px;
    padding: 14px;
    color: white;
    font-weight: 700;
    background: linear-gradient(90deg,#06b6d4,#2563eb);
}

.stButton > button:hover{
    transform: translateY(-2px);
}

/* CARDS */
.main-card{
    background: rgba(255,255,255,0.06);
    border-radius: 24px;
    padding: 30px;
    border: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 25px;
}

/* INPUTS */
.stTextInput input{
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
    -webkit-text-fill-color: white !important;
    border-radius: 14px !important;
}

.stTextArea textarea{
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
    -webkit-text-fill-color: white !important;
    border-radius: 14px !important;
}

textarea::placeholder, input::placeholder{
    color: #94a3b8 !important;
}

/* SELECTBOX */
.stSelectbox div[data-baseweb="select"] > div{
    background: white !important;
    color: black !important;
    border-radius: 14px !important;
}

/* CHAT */
.user-question{
    background: linear-gradient(90deg,#2563eb,#3b82f6);
    padding: 16px 20px;
    border-radius: 18px 18px 4px 18px;
    margin-top: 20px;
    margin-left: 60px;
    color: white;
    word-wrap: break-word;
}

.ai-answer{
    background: rgba(255,255,255,0.07);
    padding: 20px;
    border-radius: 18px 18px 18px 4px;
    margin-top: 15px;
    margin-right: 60px;
    color: white;
    word-wrap: break-word;
    white-space: pre-wrap;
}

/* LOGIN */
.login-box{
    width: 450px;
    margin: auto;
    margin-top: 70px;
    background: rgba(255,255,255,0.06);
    padding: 35px;
    border-radius: 24px;
}

.main-title{
    text-align: center;
    font-size: 52px;
    font-weight: 800;
    color: white;
}

.sub-title{
    text-align: center;
    color: #cbd5e1;
    margin-bottom: 35px;
}

</style>
""", unsafe_allow_html=True)

# ============================================
# LOGIN PAGE
# ============================================

if not st.session_state.logged_in:

    st.markdown("<div class='login-box'>", unsafe_allow_html=True)

    st.markdown("""
    <div class='main-title'>📄 QueryMate</div>
    <div class='sub-title'>Smarter Answers from Your Documents</div>
    """, unsafe_allow_html=True)

    auth_mode = st.radio(
        "Select",
        ["Login", "Register"],
        horizontal=True
    )

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if auth_mode == "Register":
        if st.button("Create Account"):
            if username.strip() == "" or password.strip() == "":
                st.error("❌ Username and password cannot be empty.")
            elif register_user(username, password):
                st.success("✅ Registered Successfully!")
            else:
                st.error("❌ Username already exists")

    else:
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("❌ Invalid Credentials")

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# MAIN APP
# ============================================

else:

    online = check_internet()
    rows = get_history(st.session_state.username)

    # ── SIDEBAR ──────────────────────────────

    with st.sidebar:

        st.markdown("""
        <div class='logo-text'>📄 QueryMate</div>
        <div class='logo-sub'>AI PDF Assistant</div>
        """, unsafe_allow_html=True)

        # FIX 1: build the HTML string first, then pass to markdown
        # Avoids quote-clash that caused raw HTML to appear as text
        first_letter = st.session_state.username[0].upper()
        safe_username = html.escape(st.session_state.username)

        user_card_html = (
            "<div class='user-card'>"
            "<div class='avatar'>" + first_letter + "</div>"
            "<h3 style='color:white;'>" + safe_username + "</h3>"
            "<p style='color:#94a3b8;'>QueryMate User</p>"
            "</div>"
        )
        st.markdown(user_card_html, unsafe_allow_html=True)

        menu = st.selectbox(
            "Navigation",
            [
                "🏠 Dashboard",
                "📄 Upload PDF",
                "💬 Ask Query",
                "📜 History"
            ],
            label_visibility="collapsed"
        )

        language = st.selectbox(
            "🌍 Language",
            ["English", "Hindi", "Marathi"]
        )
        st.session_state.language = language

        if online:
            st.success("🟢 Online Mode")
        else:
            st.warning("🟠 Offline Mode")

        if st.button("🚪 Logout"):
            # FIX 2: clear all session state cleanly on logout
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # ── DASHBOARD ────────────────────────────

    if menu == "🏠 Dashboard":

        safe_uname = html.escape(st.session_state.username)
        st.markdown(
            f"<div class='main-card'>"
            f"<h1>👋 Welcome, {safe_uname}</h1>"
            f"<p>Your Intelligent AI PDF Assistant</p>"
            f"</div>",
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)
        col1.metric("📄 Documents", "1" if st.session_state.pdf_text else "0")
        col2.metric("💬 Questions", len(rows))
        col3.metric("⚡ Status", "Online" if online else "Offline")

    # ── PDF UPLOAD ───────────────────────────

    elif menu == "📄 Upload PDF":

        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.header("📄 Upload PDF")

        uploaded_file = st.file_uploader("Choose PDF", type=["pdf"])

        if uploaded_file:
            with st.spinner("📄 Extracting text..."):
                text = extract_text_from_pdf(uploaded_file)
                if text and text.strip():
                    st.session_state.pdf_text = text
                    # FIX 3: clear stale query/answer when a new PDF is uploaded
                    st.session_state.last_query = ""
                    st.session_state.last_answer = ""
                    st.session_state.voice_query = ""
                    st.success(f"✅ {uploaded_file.name} uploaded successfully!")
                else:
                    st.error("❌ Could not extract text. The PDF may be scanned or empty.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ── ASK QUERY ────────────────────────────

    elif menu == "💬 Ask Query":

        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.header("💬 Ask Questions")

        if not st.session_state.pdf_text:
            st.warning("⚠ Please upload a PDF first.")

        else:

            if st.button("🎤 Speak Question"):
                with st.spinner("🎤 Listening..."):
                    captured = listen()
                if captured:
                    st.session_state.voice_query = captured
                    st.success(f"🗣 You said: {captured}")
                else:
                    st.warning("⚠ Could not capture audio. Please try again.")

            query = st.text_area(
                "Type your question",
                value=st.session_state.voice_query,
                placeholder="Ask something from the document...",
                height=120,
                key="query_input"
            )

            if st.button("Submit Query"):
                if not query.strip():
                    st.warning("⚠ Please enter a question.")
                else:
                    st.session_state.last_query = query
                    # FIX 4: clear voice_query after submission so it doesn't
                    # re-populate the text area on the next rerun
                    st.session_state.voice_query = ""

                    with st.spinner("🤖 AI is thinking..."):
                        answer = ask_llm(
                            st.session_state.pdf_text,
                            query,
                            st.session_state.language
                        )
                        

                    saved = save_history(
                        st.session_state.username,
                        query,
                        answer
                    )

                    if not saved:
                        st.error("❌ Failed to save history")

                    st.session_state.last_answer = answer

        # ── Display last Q&A ──────────────────

        if st.session_state.last_query:
            safe_q = html.escape(st.session_state.last_query)
            st.markdown(
                f"<div class='user-question'>👤 {safe_q}</div>",
                unsafe_allow_html=True
            )

        if st.session_state.last_answer:
            # FIX 5: fully escape the LLM response so any HTML/tags the model
            # returns are shown as plain text, not rendered as HTML
            safe_a = html.escape(st.session_state.last_answer)

            st.markdown(
                f"""<div class='ai-answer'>
                    <div style='margin-bottom:10px;font-size:13px;
                                color:#60a5fa;font-weight:bold;'>
                        🤖 QUERYMATE AI
                    </div>
                    <p style='color:white;line-height:1.8;font-size:16px;
                              white-space:pre-wrap;'>
                        {safe_a}
                    </p>
                </div>""",
                unsafe_allow_html=True
            )

            if st.button("🔊 Speak Answer"):
                speak(st.session_state.last_answer)

        st.markdown("</div>", unsafe_allow_html=True)

    # ── HISTORY ──────────────────────────────

    elif menu == "📜 History":

        st.header("📜 Query History")

        if rows:
            for q, a, created_at in rows:
                safe_q = html.escape(q)
                safe_a = html.escape(a)

                card_html = (
                    "<div class='main-card'>"
                    "<div style='font-size:12px;color:#94a3b8;margin-bottom:10px;'>"
                    f"🕒 {created_at}"
                    "</div>"
                    f"<div class='user-question'>👤 {safe_q}</div>"
                    f"<div class='ai-answer' style='white-space:pre-wrap;'>🤖 {safe_a}</div>"
                    "</div>"
                )
                st.markdown(card_html, unsafe_allow_html=True)

        else:
            st.info("No history yet.")