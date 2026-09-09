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
            background: #F4EFE7 !important;
        }

        footer {
            display: none !important;
        }

        section[data-testid="stSidebar"] {
            display: none !important;
        }


        /* Login */

        .login-screen {
            width: 100%;
            box-sizing: border-box;

            display: flex;
            justify-content: center;

            padding: 8vh 24px 0 24px;
        }

        .login-inner {
            width: min(760px, 100%);
            text-align: center;
        }


        /* Internal access */

        .login-kicker {
            font-family:
                "Segoe UI",
                Arial,
                sans-serif;

            font-size: 11px;
            font-weight: 400;

            letter-spacing: 0.22em;
            text-transform: uppercase;

            color: #7A5F32;

            margin: 0;
        }


        /* Gold rule */

        .login-rule {
            width: 56px;
            height: 1px;

            background: #A68B5B;

            margin: 22px auto 24px auto;
        }


        /* Description */

        .login-description {
            font-family:
                Optima,
                "Optima nova",
                Candara,
                "Gill Sans",
                "Gill Sans MT",
                "Segoe UI",
                sans-serif;

            font-size: 16px;
            font-weight: 300;

            line-height: 1.55;

            color: #6E5A4C;

            margin: 0 auto 26px auto;

            text-align: center;
        }


        /* Password input */

        div[data-testid="stTextInput"] {
            width: 100% !important;
            max-width: none !important;

            margin: 0 !important;
            padding: 0 !important;
        }

        div[data-testid="stTextInput"] label {
            font-family:
                "SF Pro Text",
                "SF Pro Display",
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;

            color: #3A2B21 !important;

            font-size: 13px !important;
            font-weight: 400 !important;

            text-align: left !important;

            margin-bottom: 5px !important;
        }

        div[data-testid="stTextInput"] input {
            width: 100% !important;
            height: 46px !important;

            box-sizing: border-box !important;

            background: #FBF8F3 !important;
            color: #3A2B21 !important;

            border: 1px solid #CFC2AE !important;
            border-radius: 3px !important;

            font-family:
                "SF Pro Text",
                "SF Pro Display",
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;

            font-size: 15px !important;
            font-weight: 400 !important;

            box-shadow: none !important;
        }

        div[data-testid="stTextInput"] input:hover {
            border-color: #A68B5B !important;
        }

        div[data-testid="stTextInput"] input:focus {
            border-color: #4A3428 !important;
            box-shadow: 0 0 0 1px #4A3428 !important;
        }


        /* Enter button alignment */

        .enter-button-wrap {
            padding-top: 28px !important;
        }

        .enter-button-wrap div[data-testid="stButton"] {
            margin: 0 !important;
            padding: 0 !important;
        }

        .enter-button-wrap div[data-testid="stButton"] > button {
            width: 100% !important;

            height: 46px !important;
            min-height: 46px !important;

            background: #4A3428 !important;
            color: #F4EFE7 !important;

            border: 1px solid #4A3428 !important;
            border-radius: 3px !important;

            font-family:
                "SF Pro Text",
                "SF Pro Display",
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;

            font-size: 13px !important;
            font-weight: 400 !important;

            box-shadow: none !important;
        }

        .enter-button-wrap div[data-testid="stButton"] > button:hover {
            background: #39271E !important;
            color: #F4EFE7 !important;
            border-color: #39271E !important;
        }

        .enter-button-wrap div[data-testid="stButton"] > button:active,
        .enter-button-wrap div[data-testid="stButton"] > button:focus {
            background: #4A3428 !important;
            color: #F4EFE7 !important;
            border-color: #4A3428 !important;
            box-shadow: none !important;
        }


        /* Error */

        div[data-testid="stAlert"] {
            width: min(760px, 100%);

            margin: 14px auto 0 auto;

            font-family:
                "SF Pro Text",
                "SF Pro Display",
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;

            font-size: 13px;
        }


        /* Logout */

        .logout-bar {
            width: 100%;
            box-sizing: border-box;

            padding: 10px 24px;

            background: #F4EFE7;

            border-bottom: 1px solid #E0D6C6;

            display: flex;
            justify-content: flex-end;
        }

        .logout-button div[data-testid="stButton"] {
            margin: 0 !important;
        }

        .logout-button div[data-testid="stButton"] > button {
            height: 36px !important;
            min-height: 36px !important;

            padding: 0 16px !important;

            background: transparent !important;
            color: #6E5A4C !important;

            border: 1px solid #CFC2AE !important;
            border-radius: 3px !important;

            font-family:
                "SF Pro Text",
                "SF Pro Display",
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;

            font-size: 12px !important;
            font-weight: 400 !important;
        }

        .logout-button div[data-testid="stButton"] > button:hover {
            background: #FBF8F3 !important;
            color: #3A2B21 !important;
            border-color: #A68B5B !important;
        }


        /* Gallery */

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


        /* Mobile */

        @media (max-width: 700px) {

            .login-screen {
                padding: 7vh 20px 0 20px;
            }

            .enter-button-wrap {
                padding-top: 10px !important;
            }

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

                <div class="login-rule"></div>

                <div class="login-description">
                    This working document is restricted to the
                    Hiranandani internal team.
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


    # Password + Enter

    left, center, right = st.columns(
        [1, 8, 1]
    )

    with center:

        password_col, button_col = st.columns(
            [6, 1],
            gap="small"
        )

        with password_col:

            password = st.text_input(
                "Password",
                type="password",
                autocomplete="off",
            )

        with button_col:

            st.markdown(
                '<div class="enter-button-wrap">',
                unsafe_allow_html=True,
            )

            enter_clicked = st.button(
                "Enter",
                type="secondary",
                use_container_width=True,
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )


        if enter_clicked:

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


    return False


if password_gate():

    st.markdown(
        '<div class="logout-bar">',
        unsafe_allow_html=True,
    )

    left, right = st.columns(
        [20, 1]
    )

    with right:

        st.markdown(
            '<div class="logout-button">',
            unsafe_allow_html=True,
        )

        if st.button(
            "Logout",
            type="secondary",
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
