import hashlib
import hmac
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Hiranandani Gallery",
    page_icon="HG",
    layout="wide",
    initial_sidebar_state="collapsed",
)


MAX_ATTEMPTS = 5


st.markdown(
    """
    <style>
        /* Page */
        .stApp {
            background: #F4EFE7;
            color: #3A2B21;
        }

        .block-container {
            max-width: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        header[data-testid="stHeader"] {
            background: #F4EFE7;
        }

        footer {
            display: none !important;
        }

        section[data-testid="stSidebar"] {
            display: none !important;
        }

        /* Remove default vertical spacing */
        div[data-testid="stVerticalBlock"] {
            gap: 0.5rem;
        }

        /* Login wrapper */
        .login-screen {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            box-sizing: border-box;
            padding: 40px 24px;
        }

        .login-inner {
            width: min(520px, 100%);
            text-align: center;
        }

        /* Typography */
        .login-kicker {
            font-family:
                "Segoe UI",
                Arial,
                sans-serif;

            font-size: 11px;
            font-weight: 400;
            letter-spacing: 0.22em;
            text-transform: uppercase;

            color: #80663D;
            margin-bottom: 18px;
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

            font-size: clamp(36px, 5vw, 48px);
            font-weight: 400;
            line-height: 1.1;
            letter-spacing: -0.5px;

            color: #3A2B21;
            margin: 0;
        }

        .login-rule {
            width: 56px;
            height: 1px;
            background: #A68B5B;

            margin: 26px auto 34px auto;
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

            font-size: 15px;
            font-weight: 400;
            line-height: 1.6;

            color: #765F4F;

            margin: 0 auto 34px auto;
        }

        /* Password field */
        div[data-testid="stTextInput"] {
            width: 100% !important;
            max-width: 520px !important;
            margin: 0 auto !important;
        }

        div[data-testid="stTextInput"] label {
            font-family:
                "Segoe UI",
                Arial,
                sans-serif;

            color: #3A2B21 !important;
            font-size: 12px !important;
            font-weight: 400 !important;

            text-align: left !important;
        }

        div[data-testid="stTextInput"] input {
            box-sizing: border-box !important;

            width: 100% !important;
            height: 48px !important;

            background: #FBF8F3 !important;
            color: #3A2B21 !important;

            border: 1px solid #CFC2AE !important;
            border-radius: 3px !important;

            font-family:
                "Segoe UI",
                Arial,
                sans-serif;

            font-size: 15px !important;
            font-weight: 400 !important;

            box-shadow: none !important;
        }

        div[data-testid="stTextInput"] input:hover {
            border-color: #B5A48C !important;
        }

        div[data-testid="stTextInput"] input:focus {
            border-color: #80663D !important;
            box-shadow: none !important;
        }

        /* Enter button */
        .enter-row {
            width: 100%;
            display: flex;
            justify-content: center;
            margin-top: 18px;
        }

        .enter-row .stButton > button {
            min-width: 92px;
            height: 42px;

            padding: 0 22px;

            background: #7C6035;
            color: #FFFFFF;

            border: 1px solid #7C6035;
            border-radius: 3px;

            font-family:
                "Segoe UI",
                Arial,
                sans-serif;

            font-size: 13px;
            font-weight: 500;

            box-shadow: none;
        }

        .enter-row .stButton > button:hover {
            background: #6C522E;
            color: #FFFFFF;
            border-color: #6C522E;
        }

        /* Error */
        div[data-testid="stAlert"] {
            width: 100%;
            max-width: 520px;

            margin: 18px auto 0 auto;

            font-family:
                "Segoe UI",
                Arial,
                sans-serif;

            font-size: 13px;
            text-align: left;
        }

        /* Logout */
        .logout-bar {
            width: 100%;
            box-sizing: border-box;

            padding: 12px 24px;

            background: #F4EFE7;
            border-bottom: 1px solid #DDD1C0;

            display: flex;
            justify-content: flex-end;
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
            border-color: #80663D;
        }

        /* Gallery iframe */
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

    st.html(
        """
        <div class="login-screen">
            <div class="login-inner">

                <div class="login-kicker">
                    Internal Access
                </div>

                <div class="login-title">
                    Enter password
                </div>

                <div class="login-rule"></div>

                <div class="login-description">
                    This working document is restricted to
                    the Hiranandani internal team.
                </div>

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
        '<div class="enter-row">',
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

    # Logout
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

    # Existing index.html
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
