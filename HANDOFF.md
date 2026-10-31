# DYNA ai: project notes

Browser-only watermark remover for video and photos (mainly the Google Veo / Gemini sparkle). Nothing is uploaded.
Formerly "ClearFrame". Owner: Krishna Goel, WeSolveForYou.

## Files
| File | What it is |
|---|---|
| `index.html` | The whole site: landing page, editor and removal engine. Single file, open in Chrome or Edge. Loads mp4box.js and mp4-muxer from jsDelivr and fonts from Google Fonts. |
| `favicon.png` | Tab icon (white logo on black). |
| `assets/logo-white.png` | Logo, white on transparent. Also embedded in `index.html` as a CSS variable `--logo`. |
| `assets/logo-original.png` | Logo as supplied (black on white). |
| `tools/clean_veo_video.py` | Standalone Python version of the removal method. `pip install opencv-python numpy`, needs ffmpeg. `python clean_veo_video.py in.mp4 out.mp4` |
| `streamlit_app.py` | Streamlit wrapper. Studio tab embeds `index.html` (browser-only processing); Python cleaner tab runs `tools/clean_veo_video.py` on the server. Also `requirements.txt`, `packages.txt` (ffmpeg), `.streamlit/config.toml`. |
| `.nojekyll` | Lets GitHub Pages serve the files as they are. |

## Design
Monochrome from the logo: near-black #0B0B0A, off-white #F5F5F2, greys. Display font Archivo (wide, extra bold), body IBM Plex Sans.
The watermark overlay in the editor stays magenta on purpose, so it stands out. Layout is responsive from phones to ultrawide.
CSS order in `<style>`: base, then override blocks (CYBERPUNK THEME, COMPOSITION v2, BRAND v3, LEAN v4, RESPONSIVE v5). Later blocks win.

## How removal works
1. Find the mark: median Sobel gradient across frames, keep edges whose direction agrees in 60%+ of frames.
2. Measure opacity per pixel (median of (I-B)/(255-B)) and colour wash-out separately.
3. Per frame, search an opacity gain 0.7 to 1.4 that leaves no edge along the outline, subtract in YCrCb, rebuild the rim, smooth on flat backgrounds.
4. Solid marks fall back to fill (Smooth or Texture) with camera-motion tracking.
5. Export: WebCodecs decode, H.264 re-encode with mp4-muxer, original AAC audio copied. WEBM uses real-time MediaRecorder.

## Known limits
- A fully solid logo on a static shot cannot be recovered, only blended from its surroundings.
- Removing a visible mark does not remove invisible marks such as Google's SynthID. Use only on media you own or may edit.
- Inside claude.ai the page saves files through the `downloads` capability; elsewhere it uses normal downloads.
