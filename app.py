import hashlib
import hmac
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Hiranandani Gallery — How we build it",
    page_icon="HG",
    layout="wide",
    initial_sidebar_state="collapsed",
)


MAX_ATTEMPTS = 5


st.markdown(
    """
    <style>
        .stApp {
            background: #F4EFE7;
            color: #3A2B21;
        }

        .block-container {
            max-width: 100%;
            padding: 0;
        }

        header[data-testid="stHeader"] {
            background: #4A3428;
        }

        footer {
            display: none;
        }

        section[data-testid="stSidebar"] {
            display: none;
        }

        /* Login header */
        .login-header {
            background: #4A3428;
            color: #F4EFE7;
            padding: 64px 7vw 56px 7vw;
        }

        .login-header h1 {
            font-family:
                Optima,
                "Optima Nova",
                Candara,
                "Gill Sans",
                "Gill Sans MT",
                "Segoe UI",
                sans-serif;

            font-size: clamp(38px, 5vw, 56px);
            font-weight: 400;
            line-height: 1.1;
            letter-spacing: -1px;

            margin: 0 0 20px 0;
            color: #F4EFE7;
        }

        .login-header p {
            font-family:
                Optima,
                "Optima Nova",
                Candara,
                "Gill Sans",
                "Gill Sans MT",
                "Segoe UI",
                sans-serif;

            font-size: 16px;
            font-weight: 400;
            line-height: 1.6;

            max-width: 620px;
            margin: 0;

            color: #F4EFE7;
            opacity: 0.9;
        }

        .login-rule {
            width: 56px;
            height: 1px;
            background: #A68B5B;
            margin-top: 28px;
        }

        /* Login content */
        .login-content {
            max-width: 1040px;
            margin: 0 auto;
            padding: 48px 28px 72px 28px;
        }

        .login-kick {
            font-family:
                "Segoe UI",
                Arial,
                sans-serif;

            font-size: 11px;
            font-weight: 400;
            letter-spacing: 0.18em;
            text-transform: uppercase;

            color: #7A5F32;
            margin-bottom: 14px;
        }

        .login-title {
            font-family:
                Optima,
                "Optima Nova",
                Candara,
                "Gill Sans",
                "Gill Sans MT",
                "Segoe UI",
                sans-serif;

            font-size: 32px;
            font-weight: 400;
            line-height: 1.2;

            color: #3A2B21;
            margin-bottom: 12px;
        }

        .login-description {
            font-family:
                Optima,
                "Optima Nova",
                Candara,
                "Gill Sans",
                "Gill Sans MT",
                "Segoe UI",
                sans-serif;

            font-size: 16px;
            font-weight: 400;
            line-height: 1.65;

            color: #6E5A4C;
            max-width: 680px;
        }

        /* Password input */
        div[data-testid="stTextInput"] {
            max-width: 620px;
            margin-left: auto;
            margin-right: auto;
        }

        div[data-testid="stTextInput"] label {
            font-family:
                "Segoe UI",
                Arial,
                sans-serif;

            color: #3A2B21 !important;
            font-size: 13px !important;
            font-weight: 400 !important;
        }

        div[data-testid="stTextInput"] input {
            background: #FBF8F3 !important;
            color: #3A2B21 !important;

            border: 1px solid #CFC2AE !important;
            border-radius: 3px !important;

            font-family:
                "Segoe UI",
                Arial,
                sans-serif;

            font-size: 16px !important;
            font-weight: 400 !important;

            height: 48px !important;
            box-shadow: none !important;
        }

        div[data-testid="stTextInput"] input:focus {
            border-color: #8C6D3F !important;
            box-shadow: none !important;
        }

        /* Enter button */
        .enter-wrap {
            max-width: 620px;
            margin: 16px auto 0 auto;
        }

        .enter-wrap .stButton > button {
            font-family:
                "Segoe UI",
                Arial,
                sans-serif;

            font-size: 13px;
            font-weight: 500;

            background: #7E6234;
            color: #FFFFFF;

            border: 1px solid #7E6234;
            border-radius: 3px;

            min-height: 42px;
            padding: 6px 22px;
        }

        .enter-wrap .stButton > button:hover {
            background: #6D542E;
            color: #FFFFFF;
            border-color: #6D542E;
        }

        /* Error messages */
        div[data-testid="stAlert"] {
            max-width: 620px;
            margin-left: auto;
            margin-right: auto;

            font-family:
                "Segoe UI",
                Arial,
                sans-serif;

            font-size: 13px;
        }

        /* Logout */
        .logout-bar {
            width: 100%;
            box-sizing: border-box;

            padding: 12px 28px;

            background: #F4EFE7;
            border-bottom: 1px solid #DDD1C0;
        }

        .logout-button .stButton > button {
            background: transparent;
            color: #6E5A4C;

            border: 1px solid #CFC2AE;
            border-radius: 3px;

            font-family:
                "Segoe UI",
                Arial,
                sans-serif;

            font-size: 12px;
            font-weight: 400;
        }

        .logout-button .stButton > button:hover {
            background: #FBF8F3;
            color: #3A2B21;
            border-color: #8C6D3F;
        }

        /* Existing HTML iframe */
        div[data-testid="stIFrame"] {
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        iframe {
            width: 100% !important;
            border: 0 !important;
            display: block !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

if "locked" not in st.session_state:
    st.session_state.locked = False


def verify_password(password: str) -> bool:
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


def password_gate():

    if st.session_state.authenticated:
        return True

    # Header
    st.html(
        """
        <div class="login-header">
            <h1>
                Hiranandani Gallery<br>
                How we build it
            </h1>

            <p>
                Five steps, in order. Pick the partners first,
                then work the list. Everything you tick is
                saved on this device.
            </p>

            <div class="login-rule"></div>
        </div>
        """
    )

    # Intro
    st.html(
        """
        <div class="login-content">
            <div class="login-kick">
                Internal access
            </div>

            <div class="login-title">
                Enter password
            </div>

            <div class="login-description">
                This working document is restricted to the
                Hiranandani internal team.
            </div>
        </div>
        """
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
    )

    st.markdown(
        '<div class="enter-wrap">',
        unsafe_allow_html=True,
    )

    if st.button(
        "Enter",
        type="primary",
    ):

        if verify_password(password):

            st.session_state.authenticated = True
            st.session_state.failed_attempts = 0
            st.session_state.locked = False

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

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

    return False


if password_gate():

    # Logout bar
    st.markdown(
        '<div class="logout-bar">',
        unsafe_allow_html=True,
    )

    left, right = st.columns([20, 1])

    with right:

        st.markdown(
            '<div class="logout-button">',
            unsafe_allow_html=True,
        )

        if st.button(
            "Logout",
            use_container_width=True,
        ):

            st.session_state.authenticated = False
            st.session_state.failed_attempts = 0
            st.session_state.locked = False

            st.rerun()

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

    # Existing Gallery
    html_file = Path(__file__).parent / "index.html"

    if not html_file.exists():

        st.error(
            "index.html could not be found."
        )

        st.stop()

    html = html_file.read_text(
        encoding="utf-8"
    )

    components.html(
        html,
        height=1400,
        scrolling=True,
    )
