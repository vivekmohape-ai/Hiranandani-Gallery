import hashlib
import hmac
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components



# Page configuration


st.set_page_config(
    page_title="Hiranandani Gallery",
    page_icon="HG",
    layout="wide",
)



# Settings


MAX_ATTEMPTS = 5



# Initialize session state


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

if "locked" not in st.session_state:
    st.session_state.locked = False



# Password verification
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



# Password gate


def password_gate():

    if st.session_state.authenticated:
        return True

    st.title("Hiranandani Gallery")
    st.caption("Internal team access")

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

    if st.button("Enter", type="primary"):

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



# Main application


if password_gate():

    # Logout
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.failed_attempts = 0
        st.session_state.locked = False
        st.rerun()

    # Load existing HTML application
    html_file = Path(__file__).parent / "index.html"

    html = html_file.read_text(
        encoding="utf-8"
    )

    components.html(
        html,
        height=5000,
        scrolling=True,
    )
