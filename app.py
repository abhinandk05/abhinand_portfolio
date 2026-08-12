import os
import re
import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

# Streamlit page layout configuration
st.set_page_config(
    page_title="Abhinand K | AI & Data Science Specialist",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to hide default Streamlit chrome for full-bleed iframe embedding
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

def get_mime_type(file_path: Path) -> str:
    ext = file_path.suffix.lower()
    mimes = {
        ".svg": "image/svg+xml",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".woff": "font/woff",
        ".woff2": "font/woff2",
        ".ttf": "font/ttf",
    }
    return mimes.get(ext, "application/octet-stream")

def generate_standalone_html():
    # If dist folder missing, try building automatically
    if not INDEX_FILE.exists():
        try:
            os.system("npm run build")
        except Exception:
            pass

    if not INDEX_FILE.exists():
        return None

    html_content = INDEX_FILE.read_text(encoding="utf-8")

    # 1. Inline CSS stylesheets into <style> tags
    def replace_css(match):
        rel_path = match.group(1).lstrip("/")
        css_file = DIST_DIR / rel_path
        if css_file.exists():
            css_text = css_file.read_text(encoding="utf-8")
            return f'<style>\n{css_text}\n</style>'
        return match.group(0)

    # 2. Inline JavaScript files into <script> tags
    def replace_js(match):
        rel_path = match.group(1).lstrip("/")
        js_file = DIST_DIR / rel_path
        if js_file.exists():
            js_text = js_file.read_text(encoding="utf-8")
            return f'<script type="module">\n{js_text}\n</script>'
        return match.group(0)

    # Replace link stylesheets
    html_content = re.sub(
        r'<link\s+[^>]*href=["\']([^"\']+\.css)["\'][^>]*>',
        replace_css,
        html_content
    )

    # Replace script tags
    html_content = re.sub(
        r'<script\s+[^>]*src=["\']([^"\']+\.js)["\'][^>]*></script>',
        replace_js,
        html_content
    )

    # 3. Base64 encode SVG/image icon links
    def replace_icon_links(match):
        rel_path = match.group(1).lstrip("/")
        asset_file = DIST_DIR / rel_path
        if asset_file.exists() and asset_file.suffix.lower() in [".svg", ".png", ".jpg", ".ico"]:
            b64_data = base64.b64encode(asset_file.read_bytes()).decode("utf-8")
            mime = get_mime_type(asset_file)
            return f'href="data:{mime};base64,{b64_data}"'
        return match.group(0)

    html_content = re.sub(r'href=["\']([^"\']+\.(?:svg|png|jpg|ico))["\']', replace_icon_links, html_content)

    return html_content

html_bundle = generate_standalone_html()

if html_bundle:
    components.html(html_bundle, height=4500, scrolling=True)
else:
    st.error("⚠️ `dist/index.html` not found. Please run `npm run build` locally and commit the `dist/` folder to GitHub.")
