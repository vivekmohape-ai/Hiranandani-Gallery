import hashlib
import hmac
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Hiranandani Gallery",
    page_icon="HG",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# SETTINGS
# ============================================================

MAX_ATTEMPTS = 5


# ============================================================
# STREAMLIT UI — BLACK BACKGROUND
# ============================================================

st.markdown(
    """
    <style>

    /* Entire Streamlit application */
    .stApp {
        background: #000000;
        color: #FFFFFF;
    }

    /* Remove default Streamlit top spacing */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }

    /* Hide Streamlit header */
    header[data-testid="stHeader"] {
        background: #000000;
    }

    /* Hide footer */
    footer {
        visibility: hidden;
    }

    /* Hide sidebar */
    section[data-testid="stSidebar"] {
        display: none;
    }

    /* Password input */
    div[data-testid="stTextInput"] label {
        color: #FFFFFF !important;
    }

    div[data-testid="stTextInput"] input {
        background: #111111 !important;
        color: #FFFFFF !important;
        border: 1px solid #444444 !important;
        border-radius: 6px !important;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #FFFFFF !important;
        box-shadow: none !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 6px;
        border: 1px solid #444444;
        background: #111111;
        color: #FFFFFF;
        padding: 0.5rem 1.2rem;
    }

    .stButton > button:hover {
        border-color: #FFFFFF;
        background: #1A1A1A;
        color: #FFFFFF;
    }

    /* Primary Enter button */
    .stButton > button[kind="primary"] {
        background: #FFFFFF;
        color: #000000;
        border: 1px solid #FFFFFF;
    }

    .stButton > button[kind="primary"]:hover {
        background: #EAEAEA;
        color: #000000;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

if "locked" not in st.session_state:
    st.session_state.locked = False


# ============================================================
# PASSWORD VERIFICATION
# ============================================================

def verify_password(password: str) -> bool:
    """
    Compare the entered password against the password
    stored in Streamlit Secrets.

    The plaintext password is never stored in app.py.
    """

    entered_hash = hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()

    stored_hash = hashlib.sha256(
        st.secrets["APP_PASSWORD"].encode("utf-8")
    ).hexdigest()

    return hmac.compare_digest(
        entered_hash,
        stored_hash
    )


# ============================================================
# PASSWORD SCREEN
# ============================================================

def password_gate():

    if st.session_state.authenticated:
        return True

    # Center the login area
    left, center, right = st.columns([1, 2, 1])

    with center:

        st.markdown(
            """
            <div style="
                margin-top: 15vh;
                margin-bottom: 30px;
            ">
                <h1 style="
                    color: #FFFFFF;
                    font-size: 42px;
                    font-weight: 500;
                    margin-bottom: 8px;
                ">
                    Hiranandani Gallery
                </h1>

                <p style="
                    color: #999999;
                    font-size: 15px;
                    margin-top: 0;
                ">
                    Internal team access
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.session_state.locked:

            st.error(
                "Too many incorrect attempts. "
                "Access has been locked for this session."
            )

            return False

        password = st.text_input(
            "Password",
            type="password",
            autocomplete="off",
            label_visibility="visible",
        )

        if st.button(
            "Enter",
            type="primary",
            use_container_width=False,
        ):

            if verify_password(password):

                st.session_state.authenticated = True
                st.session_state.failed_attempts = 0

                st.rerun()

            else:

                st.session_state.failed_attempts += 1

                remaining = (
                    MAX_ATTEMPTS
                    - st.session_state.failed_attempts
                )

                if remaining <= 0:

                    st.session_state.locked = True

                    st.error(
                        "Too many incorrect attempts. "
                        "Access has been locked for this session."
                    )

                else:

                    st.error(
                        f"Incorrect password. "
                        f"{remaining} attempt(s) remaining."
                    )

    return False


# ============================================================
# MAIN APPLICATION
# ============================================================

if password_gate():

    # --------------------------------------------------------
    # Top control bar
    # --------------------------------------------------------

    top_left, top_right = st.columns([8, 1])

    with top_right:

        if st.button(
            "Logout",
            use_container_width=True,
        ):

            st.session_state.authenticated = False
            st.session_state.failed_attempts = 0
            st.session_state.locked = False

            st.rerun()

    # --------------------------------------------------------
    # Load existing HTML
    # --------------------------------------------------------

    html_file = Path(__file__).parent / "index.html"

    if not html_file.exists():

        st.error(
            "index.html could not be found. "
            "Make sure it is in the same GitHub repository "
            "as app.py."
        )

        st.stop()

    html = html_file.read_text(
        encoding="utf-8"
    )

    # --------------------------------------------------------
    # Display existing Gallery
    # --------------------------------------------------------

    components.html(
        html,
        height=5000,
        scrolling=True,
    )
