import streamlit as st

# 1. PAGE SETUP
st.set_page_config(
    page_title="ACC Command Surface",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Custom CSS for executive dark theme, hidden toolbars, and emerald scope box
st.markdown(
    """
<style>
    /* 🔒 HIDE STREAMLIT TOP BAR & FOOTER */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .scope-box {
        background-color: #062313;
        border: 1.5px solid #00e676;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 25px;
    }
    .scope-title {
        color: #00e676;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
    }
    .scope-role {
        color: #ffffff;
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 4px;
    }
</style>
""",
    unsafe_allow_html=True,
)


