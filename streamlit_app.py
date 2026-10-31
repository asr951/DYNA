"""DYNA ai on Streamlit.

Tab 1 runs the full DYNA ai web app inside Streamlit. All processing happens in the visitor's
browser, so nothing is uploaded to the Streamlit server.
Tab 2 is an optional server-side cleaner (tools/clean_veo_video.py). It DOES upload the video to
the machine running Streamlit and needs ffmpeg.

Run:  pip install -r requirements.txt  &&  streamlit run streamlit_app.py
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).parent

st.set_page_config(
    page_title="DYNA ai",
    page_icon=str(ROOT / "favicon.png"),
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      #MainMenu, footer, [data-testid="stHeader"], [data-testid="stToolbar"] {display:none !important;}
      .stApp {background:#0B0B0A;}
      .block-container {padding:0.4rem 0.6rem 0 !important; max-width:100% !important;}
      iframe {border:0; border-radius:0; width:100%;}
      button[data-baseweb="tab"] p {color:#F5F5F2; font-weight:600;}
      .stApp, .stApp p, .stApp label, .stApp li, .stApp h1, .stApp h2, .stApp h3 {color:#F5F5F2;}
      .stApp button[kind="primary"] {background:#F5F5F2 !important; border-color:#F5F5F2 !important;}
      .stApp button[kind="primary"] p {color:#0B0B0A !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Makes the iframe fill the browser window, and keeps in-page links (#how) working inside it.
FIT_SCRIPT = """
<script>
(function () {
  function fit() {
    try {
      var f = window.frameElement;
      if (f) f.style.setProperty('height', Math.max(560, window.parent.innerHeight - 76) + 'px', 'important');
    } catch (e) {}
  }
  fit();
  try { window.parent.addEventListener('resize', fit); } catch (e) {}
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="#"]');
    if (!a) return;
    e.preventDefault();
    var id = a.getAttribute('href').slice(1), t = id && document.getElementById(id);
    if (t) t.scrollIntoView({behavior: 'smooth'}); else window.scrollTo({top: 0, behavior: 'smooth'});
  }, true);
})();
</script>
"""


@st.cache_data(show_spinner=False)
def load_site() -> str:
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    i = html.rfind("</body>")
    return html[:i] + FIT_SCRIPT + html[i:] if i != -1 else html + FIT_SCRIPT


studio, cleaner = st.tabs(["Studio", "Python cleaner"])

with studio:
    components.html(load_site(), height=900, scrolling=True)

with cleaner:
    st.subheader("Python cleaner")
    st.write(
        "Removes a fixed, see-through watermark such as the Google Veo sparkle from a video. "
        "**This tab uploads your video to the machine running this app.** "
        "Use the Studio tab if you want everything to stay on your device."
    )
    if shutil.which("ffmpeg") is None:
        st.warning("ffmpeg was not found on this machine, so this tab cannot encode video. Install ffmpeg first.")
    up = st.file_uploader("Video", type=["mp4", "mov", "m4v"])
    region = st.text_input(
        "Search region x0,y0,x1,y1 (optional)",
        placeholder="Leave empty to search the bottom-right corner",
    )
    if up and st.button("Clean video", type="primary"):
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / ("input" + Path(up.name).suffix)
            src.write_bytes(up.getbuffer())
            out = Path(d) / "output.mp4"
            cmd = [sys.executable, str(ROOT / "tools" / "clean_veo_video.py"), str(src), str(out)]
            if region.strip():
                cmd += ["--region", region.strip()]
            with st.spinner("Cleaning every frame. Long clips can take several minutes."):
                run = subprocess.run(cmd, capture_output=True, text=True)
            if run.returncode == 0 and out.exists():
                st.session_state["clean"] = (out.read_bytes(), Path(up.name).stem + "-clean.mp4")
            else:
                st.session_state.pop("clean", None)
                st.error("The cleaner could not process this file.")
                st.code((run.stdout + run.stderr)[-2000:] or "No output.")
    if "clean" in st.session_state:
        data, name = st.session_state["clean"]
        st.success("Done. Check the result, then download it.")
        st.video(data)
        st.download_button("Download cleaned video", data, file_name=name, mime="video/mp4")
