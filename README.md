# DYNA ai

Watermark remover for video and photos. Runs entirely in the browser: nothing is uploaded.

Live site (after enabling GitHub Pages): https://asr951.github.io/DYNA-ai/

## Files
- `index.html` the whole site: landing page, editor and removal engine
- `favicon.png` tab icon
- `.nojekyll` tells GitHub Pages to serve the files as they are

## Notes
- Open in Chrome or Edge for the fastest video export (WebCodecs).
- Loads mp4box.js and mp4-muxer from jsDelivr, and fonts from Google Fonts, so it needs an internet connection.
- Use only on media you own or have permission to edit. Removing a visible mark does not remove invisible provenance marks such as SynthID.

## Run on Streamlit
```
pip install -r requirements.txt
streamlit run streamlit_app.py
```
- **Studio** tab: the full DYNA ai site inside Streamlit. Everything runs in the visitor's browser; nothing reaches the Streamlit server.
- **Python cleaner** tab: server-side version using `tools/clean_veo_video.py`. It uploads the video to the machine running Streamlit and needs ffmpeg (`packages.txt` installs it on Streamlit Community Cloud).

Deploy on Streamlit Community Cloud: push this folder to GitHub, then in share.streamlit.io choose the repo, branch `main`, main file `streamlit_app.py`.
