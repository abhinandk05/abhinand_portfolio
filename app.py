import os
import re
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

# Configure Streamlit page layout & title
st.set_page_config(
    page_title="Abhinand K | AI & Data Science Specialist",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject CSS to remove Streamlit padding, header, footer for seamless full-bleed rendering
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stToolbar"] {visibility: hidden;}
    div[data-testid="stDecoration"] {display: none;}
    div[data-testid="stStatusWidget"] {display: none;}
    
    .main .block-container {
        padding: 0rem !important;
        margin: 0rem !important;
        max-width: 100% !important;
    }
    
    iframe {
        border: none !important;
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).parent
DIST_DIR = BASE_DIR / "dist"
INDEX_FILE = DIST_DIR / "index.html"

def get_bundled_html():
    if not INDEX_FILE.exists():
        return None

    html_content = INDEX_FILE.read_text(encoding="utf-8")

    # Inlining JavaScript assets
    def replace_js(match):
        rel_path = match.group(1).lstrip("/")
        target_file = DIST_DIR / rel_path
        if target_file.exists():
            js_code = target_file.read_text(encoding="utf-8")
            return f'<script type="module">{js_code}</script>'
        return match.group(0)

    # Inlining CSS assets
    def replace_css(match):
        rel_path = match.group(1).lstrip("/")
        target_file = DIST_DIR / rel_path
        if target_file.exists():
            css_code = target_file.read_text(encoding="utf-8")
            return f'<style>{css_code}</style>'
        return match.group(0)

    # Inline JS script tags
    html_content = re.sub(
        r'<script\s+[^>]*src=["\']([^"\']+)["\'][^>]*></script>',
        replace_js,
        html_content
    )

    # Inline CSS stylesheet links
    html_content = re.sub(
        r'<link\s+[^>]*href=["\']([^"\']+\.css)["\'][^>]*>',
        replace_css,
        html_content
    )

    return html_content

bundled_html = get_bundled_html()

if bundled_html:
    components.html(bundled_html, height=4500, scrolling=True)
else:
    st.error("⚠️ `dist/index.html` not found. Please build the project first by running `npm run build`.")
