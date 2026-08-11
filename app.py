import streamlit as st
from config import get_sector_book, sector_book_options

st.set_page_config(
    page_title="Executive Synthesis & Knowledge Engine",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Sector Router
st.sidebar.title("Navigation")
options = sector_book_options()
selected_key = st.sidebar.selectbox(
    "Active Sector Book",
    options=list(options.keys()),
    format_func=lambda x: options[x]
)

data = get_sector_book(selected_key)

# Theme Styling & Stealth Chrome Removal
st.markdown("""
    <style>
    /* Eradicate Streamlit Chrome, Header, Share Button & Manage App Badge */
    header, footer, #MainMenu, .stDeployButton, 
    [data-testid="stHeader"], 
    [data-testid="stToolbar"], 
    [data-testid="stDecoration"], 
    [data-testid="stStatusWidget"], 
    [data-testid="stAppDeployButton"],
    [data-testid="stSidebarNav"],
    div[class*="viewerBadge"],
    button[title*="Manage app"] {
        visibility: hidden !important;
        display: none !important;
    }

    .stApp { background-color: #0b0f17; color: #e6edf3; }
    .main-title { font-size: 2.2rem; font-weight: 800; color: #ffffff; margin-bottom: 1.5rem; }
    .bridge-banner { background-color: #0d1e36; border-left: 4px solid #2f81f7; padding: 1.1rem 1.3rem; border-radius: 6px; margin-bottom: 1.2rem; }
    .bridge-title { color: #58a6ff; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; margin-bottom: 0.3rem; }
    .bridge-text { color: #a5d6ff; font-size: 0.95rem; line-height: 1.5; }
    .metric-card { background-color: #131d2a; border: 1px solid #213043; border-radius: 8px; padding: 1.25rem; height: 100%; }
    .metric-label { font-size: 0.85rem; font-weight: 600; color: #8b949e; margin-bottom: 0.5rem; }
    .metric-value { font-size: 2.2rem; font-weight: 800; color: #ffffff; margin-bottom: 0.8rem; }
    .metric-basis { font-size: 0.78rem; color: #6e7681; }
    .footer-source { background-color: #0b1626; border: 1px solid #1e2d42; padding: 0.6rem 1rem; border-radius: 6px; font-size: 0.82rem; color: #58a6ff; margin-top: 1.5rem; }
    </style>
""", unsafe_allow_html=True)


# Render Header & Banner
st.markdown(f'<div class="main-title">{data["title"]}</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="bridge-banner">
    <div class="bridge-title">⚡ DIRECT OPERATIONAL BRIDGE</div>
    <div class="bridge-text">{data["bridge_text"]}</div>
</div>
""", unsafe_allow_html=True)

# Render Metric Cards
col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3]

for col, m in zip(cols, data["metrics"]):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{m['label']} 🛈</div>
            <div class="metric-value">{m['value']}</div>
            <div class="metric-basis">📊 Basis: {m['basis']}</div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown(f'<div class="footer-source">{data["footer"]}</div>', unsafe_allow_html=True)

