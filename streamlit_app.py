import streamlit as st
import random
import time
from main import agent_loop

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="JokeBot Live",
    page_icon="🎭",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Session state ─────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "performances": 0,
        "laughs": 0,
        "history": [],
        "current_joke": None,
        "show_joke": False,
        "liked_jokes": set(),
        "theme": "dark",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── Theme palettes ────────────────────────────────────────────────────────────
THEMES = {
    "dark": {
        "bg": "#0a0a0f",
        "stage": "#1a1008",
        "curtain": "#8b0000",
        "curtain2": "#6b0000",
        "gold": "#f0c040",
        "gold2": "#c8960c",
        "neon": "#bf5fff",
        "neon2": "#9b30ff",
        "text": "#f5f0e8",
        "subtext": "#a09080",
        "card": "#12100a",
        "card_border": "#f0c040",
        "spotlight": "rgba(255,240,180,0.18)",
        "booth": "#1a1408",
        "booth_border": "#f0c040",
    },
    "vintage": {
        "bg": "#1a0f05",
        "stage": "#0f0800",
        "curtain": "#7a2000",
        "curtain2": "#5a1800",
        "gold": "#e8a820",
        "gold2": "#b87a08",
        "neon": "#ff6b35",
        "neon2": "#e84f1a",
        "text": "#f5e8d0",
        "subtext": "#9a7850",
        "card": "#0f0800",
        "card_border": "#e8a820",
        "spotlight": "rgba(255,200,120,0.15)",
        "booth": "#150b02",
        "booth_border": "#e8a820",
    },
}

T = THEMES[st.session_state.theme]

# ── CSS ────────────────────────────────────────────────────────────────────────
def inject_css(t):
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Raleway:wght@300;400;600;700&family=Special+Elite&display=swap');

/* ── Reset ── */
html, body, [class*="css"] {{
  font-family: 'Raleway', sans-serif !important;
  background: {t['bg']} !important;
  color: {t['text']} !important;
}}
.stApp {{ background: {t['bg']} !important; }}
.block-container {{
  padding: 1.5rem 1rem 3rem !important;
  max-width: 820px !important;
}}

/* ── Hide streamlit chrome ── */
#MainMenu, footer, header {{ visibility: hidden; }}
div[data-testid="stDecoration"] {{ display: none; }}
.stDeployButton {{ display: none; }}

/* ══════════════════════════════════════
   NEON SIGN
══════════════════════════════════════ */
.neon-sign {{
  text-align: center;
  padding: 28px 0 8px;
  position: relative;
}}
.neon-title {{
  font-family: 'Special Elite', cursive !important;
  font-size: clamp(2rem, 6vw, 3.2rem);
  color: {t['neon']} !important;
  text-shadow:
    0 0 6px {t['neon']},
    0 0 20px {t['neon']},
    0 0 40px {t['neon2']},
    0 0 80px {t['neon2']};
  animation: neonFlicker 4s infinite;
  letter-spacing: 4px;
  margin: 0;
}}
.neon-subtitle {{
  font-family: 'Raleway', sans-serif !important;
  font-size: 0.78rem;
  letter-spacing: 0.35em;
  text-transform: uppercase;
  color: {t['gold']} !important;
  margin-top: 6px;
  opacity: 0.85;
}}
.neon-divider {{
  height: 2px;
  background: linear-gradient(90deg, transparent, {t['gold']}, {t['neon']}, {t['gold']}, transparent);
  margin: 18px auto 0;
  max-width: 500px;
  border-radius: 2px;
}}
@keyframes neonFlicker {{
  0%,19%,21%,23%,25%,54%,56%,100% {{
    text-shadow:
      0 0 6px {t['neon']},
      0 0 20px {t['neon']},
      0 0 40px {t['neon2']},
      0 0 80px {t['neon2']};
  }}
  20%,24%,55% {{
    text-shadow: none;
    color: {t['neon2']} !important;
  }}
}}

/* ══════════════════════════════════════
   CURTAIN STAGE
══════════════════════════════════════ */
.theater-stage {{
  position: relative;
  width: 100%;
  min-height: 320px;
  background: radial-gradient(ellipse 70% 60% at 50% 40%, {t['spotlight']}, {t['stage']} 70%);
  border-radius: 8px 8px 0 0;
  overflow: hidden;
  margin: 20px 0 0;
  border: 1px solid #2a2010;
}}

/* Stage floor */
.stage-floor {{
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 60px;
  background: linear-gradient(180deg, #2a1a08 0%, #1a0e04 100%);
  border-top: 3px solid #3a2412;
}}
.stage-floor::before {{
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent, {t['gold']}, transparent);
  opacity: 0.6;
}}

/* Stage planks */
.stage-planks {{
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 60px;
  background-image: repeating-linear-gradient(
    90deg,
    transparent,
    transparent 48px,
    rgba(255,200,100,0.06) 48px,
    rgba(255,200,100,0.06) 50px
  );
}}

/* Curtains */
.curtain-left, .curtain-right {{
  position: absolute;
  top: 0; bottom: 0;
  width: 22%;
  z-index: 3;
}}
.curtain-left {{
  left: 0;
  background: linear-gradient(90deg, {t['curtain']} 60%, {t['curtain2']} 85%, transparent 100%);
  animation: curtainOpenLeft 1.8s cubic-bezier(0.4,0,0.2,1) forwards;
}}
.curtain-right {{
  right: 0;
  background: linear-gradient(270deg, {t['curtain']} 60%, {t['curtain2']} 85%, transparent 100%);
  animation: curtainOpenRight 1.8s cubic-bezier(0.4,0,0.2,1) forwards;
}}
.curtain-left::after, .curtain-right::after {{
  content: '';
  position: absolute;
  top: 0; bottom: 0;
  width: 100%;
  background-image: repeating-linear-gradient(
    90deg,
    rgba(0,0,0,0.12) 0px,
    rgba(255,255,255,0.04) 6px,
    rgba(0,0,0,0.12) 12px
  );
}}
@keyframes curtainOpenLeft {{
  0%   {{ transform: translateX(0); }}
  100% {{ transform: translateX(-80%); }}
}}
@keyframes curtainOpenRight {{
  0%   {{ transform: translateX(0); }}
  100% {{ transform: translateX(80%); }}
}}

/* Curtain top valance */
.curtain-valance {{
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 40px;
  background: linear-gradient(180deg, {t['curtain']} 0%, {t['curtain2']} 60%, transparent 100%);
  z-index: 4;
  border-bottom: 2px solid {t['gold']};
}}
.curtain-valance::after {{
  content: '✦  ✦  ✦  THE JOKEBOT LIVE  ✦  ✦  ✦';
  position: absolute;
  bottom: -1px; left: 0; right: 0;
  text-align: center;
  font-size: 0.55rem;
  letter-spacing: 0.3em;
  color: {t['gold']};
  font-family: 'Raleway', sans-serif;
  font-weight: 700;
}}

/* Spotlight beams */
.spotlight-beam {{
  position: absolute;
  top: -10px;
  width: 0;
  height: 0;
  border-left: 40px solid transparent;
  border-right: 40px solid transparent;
  border-top: 200px solid rgba(255,240,180,0.06);
  z-index: 1;
  animation: spotlightPulse 3s ease-in-out infinite;
}}
.spotlight-beam.s1 {{ left: 20%; transform: rotate(-12deg); animation-delay: 0s; }}
.spotlight-beam.s2 {{ left: 45%; border-top-color: rgba(255,240,180,0.1); animation-delay: 0.8s; }}
.spotlight-beam.s3 {{ right: 18%; transform: rotate(12deg); animation-delay: 1.6s; }}
@keyframes spotlightPulse {{
  0%,100% {{ opacity: 0.6; }}
  50%      {{ opacity: 1; }}
}}

/* Stage lights bar */
.stage-lights {{
  position: absolute;
  top: 40px; left: 0; right: 0;
  display: flex;
  justify-content: space-evenly;
  z-index: 5;
  padding: 0 8%;
}}
.stage-light {{
  width: 16px; height: 22px;
  border-radius: 0 0 8px 8px;
  position: relative;
}}
.stage-light::after {{
  content: '';
  position: absolute;
  top: 20px; left: 50%;
  transform: translateX(-50%);
  width: 0; height: 0;
  border-left: 14px solid transparent;
  border-right: 14px solid transparent;
  border-top: 60px solid;
  opacity: 0.15;
}}
.sl-gold {{ background: {t['gold']}; box-shadow: 0 0 12px {t['gold']}, 0 0 24px {t['gold']}; }}
.sl-gold::after {{ border-top-color: {t['gold']}; opacity: 0.12; }}
.sl-neon {{ background: {t['neon']}; box-shadow: 0 0 12px {t['neon']}, 0 0 24px {t['neon']}; }}
.sl-neon::after {{ border-top-color: {t['neon']}; opacity: 0.1; }}
.sl-white {{ background: #fff8e8; box-shadow: 0 0 12px #fff8e8, 0 0 24px #fff8e8; }}
.sl-white::after {{ border-top-color: #fff8e8; opacity: 0.18; }}
.sl-animate {{ animation: lightFlash 2.5s ease-in-out infinite; }}
.sl-animate-slow {{ animation: lightFlash 4s ease-in-out infinite; }}
@keyframes lightFlash {{
  0%,100% {{ opacity: 1; }}
  50%      {{ opacity: 0.5; }}
}}

/* Microphone */
.mic-wrap {{
  position: absolute;
  bottom: 52px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 6;
  text-align: center;
  animation: micBounce 2.5s ease-in-out infinite;
}}
.mic-icon {{
  font-size: 3rem;
  filter: drop-shadow(0 0 12px {t['gold']}) drop-shadow(0 0 24px {t['gold2']});
}}
.mic-stand {{
  width: 3px;
  height: 28px;
  background: linear-gradient(180deg, {t['gold']}, {t['gold2']});
  margin: 0 auto;
  border-radius: 2px;
}}
.mic-base {{
  width: 40px;
  height: 4px;
  background: linear-gradient(90deg, transparent, {t['gold']}, transparent);
  margin: 0 auto;
  border-radius: 2px;
}}
@keyframes micBounce {{
  0%,100% {{ transform: translateX(-50%) translateY(0); }}
  50%      {{ transform: translateX(-50%) translateY(-6px); }}
}}

/* Audience silhouettes */
.audience {{
  position: relative;
  width: 100%;
  height: 70px;
  background: {t['bg']};
  overflow: hidden;
  border-radius: 0 0 8px 8px;
}}
.audience-svg {{
  width: 100%;
  height: 100%;
}}

/* ══════════════════════════════════════
   JOKE CARD
══════════════════════════════════════ */
.joke-card {{
  background: linear-gradient(145deg, {t['card']} 0%, #0d0c06 100%);
  border: 1.5px solid {t['card_border']};
  border-radius: 12px;
  padding: 36px 32px 28px;
  position: relative;
  box-shadow:
    0 0 0 1px rgba(240,192,64,0.15),
    0 8px 40px rgba(0,0,0,0.7),
    inset 0 1px 0 rgba(240,192,64,0.2);
  animation: jokeReveal 0.7s cubic-bezier(0.34,1.56,0.64,1) forwards;
  overflow: hidden;
  margin: 20px 0;
}}
.joke-card::before {{
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, {t['gold']}, {t['neon']}, {t['gold']}, transparent);
  border-radius: 12px 12px 0 0;
}}
.joke-card::after {{
  content: '';
  position: absolute;
  top: -50%; left: -50%;
  width: 200%; height: 200%;
  background: radial-gradient(ellipse at 50% 0%, rgba(240,192,64,0.04), transparent 60%);
  pointer-events: none;
}}
.joke-card-header {{
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}}
.joke-card-label {{
  font-size: 0.62rem;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: {t['gold']} !important;
  font-weight: 600;
}}
.joke-card-num {{
  font-size: 0.6rem;
  color: {t['subtext']} !important;
  margin-left: auto;
  letter-spacing: 0.1em;
}}
.joke-text {{
  font-family: 'Playfair Display', serif !important;
  font-size: clamp(1.05rem, 3vw, 1.4rem) !important;
  color: {t['text']} !important;
  line-height: 1.75 !important;
  margin: 0 0 24px !important;
  font-style: italic;
}}
.joke-card-footer {{
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  border-top: 1px solid rgba(240,192,64,0.15);
  padding-top: 16px;
}}
@keyframes jokeReveal {{
  0%   {{ opacity: 0; transform: translateY(30px) scale(0.95); }}
  100% {{ opacity: 1; transform: translateY(0) scale(1); }}
}}

/* Floating emoji */
.emoji-float {{
  position: fixed;
  font-size: 2rem;
  pointer-events: none;
  z-index: 9999;
  animation: floatUp 3s ease-out forwards;
}}
@keyframes floatUp {{
  0%   {{ opacity: 1; transform: translateY(0) rotate(0deg); }}
  100% {{ opacity: 0; transform: translateY(-300px) rotate(20deg); }}
}}

/* ── SEND button — gold filled, stands out ── */
.send-btn-wrap .stButton > button {{
  background: linear-gradient(135deg, {t['gold']}, {t['gold2']}) !important;
  color: #0a0a0f !important;
  border: none !important;
  border-radius: 8px !important;
  font-weight: 700 !important;
  font-size: 0.82rem !important;
  letter-spacing: 0.06em !important;
  box-shadow: 0 0 16px rgba(240,192,64,0.35) !important;
  padding: 14px 4px !important;
}}
.send-btn-wrap .stButton > button:hover {{
  background: linear-gradient(135deg, #ffe066, {t['gold']}) !important;
  box-shadow: 0 0 28px rgba(240,192,64,0.55) !important;
  transform: translateY(-2px) !important;
  color: #0a0a0f !important;
}}

/* ── REQUEST BOOTH
══════════════════════════════════════ */
.booth-wrap {{
  background: linear-gradient(145deg, {t['booth']} 0%, #0f0c04 100%);
  border: 1.5px solid {t['booth_border']};
  border-radius: 12px;
  padding: 24px 24px 20px;
  margin: 8px 0 16px;
  position: relative;
  box-shadow: 0 4px 24px rgba(0,0,0,0.5), inset 0 1px 0 rgba(240,192,64,0.15);
}}
.booth-wrap::before {{
  content: '🎟️  REQUEST BOOTH';
  display: block;
  font-size: 0.6rem;
  letter-spacing: 0.3em;
  color: {t['gold']} !important;
  margin-bottom: 14px;
  font-weight: 700;
}}
.stTextInput > div > div > input {{
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(240,192,64,0.3) !important;
  border-radius: 8px !important;
  color: {t['text']} !important;
  font-family: 'Raleway', sans-serif !important;
  font-size: 0.92rem !important;
  padding: 14px 18px !important;
  transition: border-color 0.3s, box-shadow 0.3s !important;
}}
.stTextInput > div > div > input:focus {{
  border-color: {t['gold']} !important;
  box-shadow: 0 0 0 3px rgba(240,192,64,0.12), 0 0 20px rgba(240,192,64,0.08) !important;
  outline: none !important;
}}
.stTextInput > div > div > input::placeholder {{ color: rgba(160,144,128,0.6) !important; }}
.stTextInput > div {{ border: none !important; }}
.stTextInput > div > div {{ border: none !important; box-shadow: none !important; }}

/* ══════════════════════════════════════
   PERFORMANCE BUTTONS
══════════════════════════════════════ */
.stButton > button {{
  background: linear-gradient(135deg, rgba(240,192,64,0.12), rgba(240,192,64,0.06)) !important;
  color: {t['gold']} !important;
  border: 1px solid rgba(240,192,64,0.35) !important;
  border-radius: 8px !important;
  font-family: 'Raleway', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.8rem !important;
  letter-spacing: 0.06em !important;
  padding: 11px 8px !important;
  transition: all 0.25s ease !important;
  position: relative !important;
  overflow: hidden !important;
}}
.stButton > button::before {{
  content: '' !important;
  position: absolute !important;
  top: 0; left: -100%; width: 100%; height: 100% !important;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent) !important;
  transition: left 0.4s ease !important;
}}
.stButton > button:hover {{
  background: linear-gradient(135deg, rgba(240,192,64,0.25), rgba(240,192,64,0.12)) !important;
  border-color: {t['gold']} !important;
  box-shadow: 0 0 20px rgba(240,192,64,0.2), 0 4px 12px rgba(0,0,0,0.4) !important;
  transform: translateY(-2px) !important;
  color: #fff8d0 !important;
}}
.stButton > button:hover::before {{ left: 100% !important; }}
.stButton > button:active {{ transform: translateY(0) !important; }}

/* Action row inline card buttons */
.joke-action-btn {{
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 7px 14px;
  border: 1px solid rgba(240,192,64,0.25);
  border-radius: 20px;
  font-size: 0.72rem;
  color: {t['gold']};
  cursor: pointer;
  transition: all 0.2s;
  background: rgba(240,192,64,0.06);
  font-family: 'Raleway', sans-serif;
  font-weight: 600;
  letter-spacing: 0.05em;
}}
.joke-action-btn:hover {{
  background: rgba(240,192,64,0.15);
  border-color: {t['gold']};
  box-shadow: 0 0 12px rgba(240,192,64,0.15);
}}

/* ══════════════════════════════════════
   SIDEBAR / BACKSTAGE
══════════════════════════════════════ */
section[data-testid="stSidebar"] {{
  background: #07060a !important;
  border-right: 1px solid rgba(240,192,64,0.15) !important;
}}
section[data-testid="stSidebar"] * {{
  color: {t['text']} !important;
  font-family: 'Raleway', sans-serif !important;
}}
section[data-testid="stSidebar"] hr {{
  border-color: rgba(240,192,64,0.15) !important;
}}
.backstage-title {{
  font-family: 'Special Elite', cursive !important;
  font-size: 0.9rem;
  letter-spacing: 0.2em;
  color: {t['gold']} !important;
  text-align: center;
  padding: 8px 0 4px;
}}
.backstage-subtitle {{
  font-size: 0.6rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: {t['subtext']} !important;
  text-align: center;
  margin-bottom: 12px;
}}
.stat-card {{
  background: linear-gradient(135deg, rgba(240,192,64,0.06), rgba(191,95,255,0.04));
  border: 1px solid rgba(240,192,64,0.15);
  border-radius: 10px;
  padding: 14px 16px;
  margin: 8px 0;
  text-align: center;
}}
.stat-num {{
  font-family: 'Playfair Display', serif !important;
  font-size: 2.2rem;
  color: {t['gold']} !important;
  line-height: 1;
  text-shadow: 0 0 20px rgba(240,192,64,0.3);
}}
.stat-lbl {{
  font-size: 0.62rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: {t['subtext']} !important;
  margin-top: 4px;
}}
section[data-testid="stSidebar"] .stButton > button {{
  background: linear-gradient(135deg, rgba(240,192,64,0.1), rgba(240,192,64,0.05)) !important;
  color: {t['gold']} !important;
  border: 1px solid rgba(240,192,64,0.3) !important;
  border-radius: 8px !important;
}}
section[data-testid="stSidebar"] .stButton > button:hover {{
  background: rgba(240,192,64,0.2) !important;
  border-color: {t['gold']} !important;
}}
.comedian-card {{
  background: rgba(240,192,64,0.04);
  border: 1px solid rgba(240,192,64,0.12);
  border-radius: 10px;
  padding: 14px;
  text-align: center;
  margin: 10px 0;
}}
.comedian-avatar {{
  font-size: 2.8rem;
  display: block;
  margin-bottom: 6px;
  filter: drop-shadow(0 0 10px {t['gold']});
}}
.comedian-name {{
  font-family: 'Playfair Display', serif !important;
  font-size: 1rem;
  color: {t['gold']} !important;
}}
.comedian-bio {{
  font-size: 0.7rem;
  color: {t['subtext']} !important;
  line-height: 1.6;
  margin-top: 6px;
}}

/* ══════════════════════════════════════
   HISTORY ROW
══════════════════════════════════════ */
.hist-label {{
  font-size: 0.6rem;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: {t['subtext']} !important;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 28px 0 14px;
}}
.hist-label::before, .hist-label::after {{
  content: '';
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(240,192,64,0.2), transparent);
}}
.hist-item {{
  background: rgba(240,192,64,0.03);
  border: 1px solid rgba(240,192,64,0.08);
  border-radius: 8px;
  padding: 12px 16px;
  margin: 8px 0;
  display: flex;
  gap: 12px;
  align-items: flex-start;
  transition: border-color 0.2s;
}}
.hist-item:hover {{
  border-color: rgba(240,192,64,0.2);
}}
.hist-num {{
  font-size: 0.6rem;
  color: {t['gold']} !important;
  opacity: 0.5;
  min-width: 20px;
  padding-top: 2px;
  font-weight: 700;
}}
.hist-text {{
  font-family: 'Playfair Display', serif !important;
  font-size: 0.82rem;
  color: rgba(245,240,232,0.7) !important;
  line-height: 1.5;
  font-style: italic;
}}

/* ══════════════════════════════════════
   FOOTER
══════════════════════════════════════ */
.theater-footer {{
  text-align: center;
  padding: 24px 0 8px;
  border-top: 1px solid rgba(240,192,64,0.12);
  margin-top: 32px;
}}
.theater-footer p {{
  font-size: 0.62rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: {t['subtext']} !important;
  margin: 4px 0;
}}

/* ══════════════════════════════════════
   CONFETTI CANVAS
══════════════════════════════════════ */
#confetti-canvas {{
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  pointer-events: none;
  z-index: 9998;
}}

/* ══════════════════════════════════════
   SELECT / RADIO
══════════════════════════════════════ */
.stSelectbox > div > div {{
  background: rgba(255,255,255,0.03) !important;
  border-color: rgba(240,192,64,0.3) !important;
  color: {t['text']} !important;
}}
.stRadio label {{ color: {t['text']} !important; }}

/* Mobile */
@media (max-width: 600px) {{
  .joke-text {{ font-size: 1rem !important; }}
  .theater-stage {{ min-height: 240px; }}
  .neon-title {{ font-size: 1.8rem; }}
}}
</style>
""", unsafe_allow_html=True)

inject_css(T)

# ── JS: confetti + floating emojis ────────────────────────────────────────────
def inject_js():
    st.markdown("""
<canvas id="confetti-canvas"></canvas>
<script>
(function() {
  // Confetti
  var canvas = document.getElementById('confetti-canvas');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  var pieces = [];
  var colors = ['#f0c040','#bf5fff','#ff6b6b','#4ecdc4','#fff8d0','#c8960c'];
  for (var i = 0; i < 120; i++) {
    pieces.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height - canvas.height,
      r: Math.random() * 7 + 3,
      d: Math.random() * 3 + 1,
      color: colors[Math.floor(Math.random() * colors.length)],
      tilt: Math.random() * 20 - 10,
      tiltAngle: 0,
      tiltAngleInc: Math.random() * 0.07 + 0.05
    });
  }
  var angle = 0;
  var frames = 0;
  var maxFrames = 220;
  function draw() {
    if (frames > maxFrames) { ctx.clearRect(0, 0, canvas.width, canvas.height); return; }
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    angle += 0.01;
    frames++;
    pieces.forEach(function(p) {
      p.tiltAngle += p.tiltAngleInc;
      p.y += (Math.cos(angle + p.d) + p.d + 0.5) * 1.8;
      p.x += Math.sin(angle) * 1.2;
      p.tilt = Math.sin(p.tiltAngle) * 15;
      ctx.beginPath();
      ctx.lineWidth = p.r / 2;
      ctx.strokeStyle = p.color;
      ctx.moveTo(p.x + p.tilt + p.r / 4, p.y);
      ctx.lineTo(p.x + p.tilt, p.y + p.tilt + p.r / 4);
      ctx.stroke();
    });
    requestAnimationFrame(draw);
  }
  draw();

  // Floating emojis
  var emojis = ['😂','🤣','😄','😆','💛','🎭','🎤','✨','🌟','👏'];
  for (var j = 0; j < 12; j++) {
    (function(delay) {
      setTimeout(function() {
        var el = document.createElement('div');
        el.style.cssText = 'position:fixed;font-size:' + (Math.random()*1.5+1.2) + 'rem;' +
          'left:' + (Math.random()*90+5) + '%;bottom:20%;pointer-events:none;z-index:9999;' +
          'animation:floatUp ' + (Math.random()*2+2.5) + 's ease-out forwards;';
        el.textContent = emojis[Math.floor(Math.random()*emojis.length)];
        document.body.appendChild(el);
        setTimeout(function() { el.remove(); }, 5000);
      }, delay);
    })(j * 200);
  }
})();
</script>
<style>
@keyframes floatUp {
  0%   { opacity:1; transform: translateY(0) rotate(0deg) scale(1); }
  100% { opacity:0; transform: translateY(-400px) rotate(25deg) scale(0.5); }
}
</style>
""", unsafe_allow_html=True)

# ── Reusable render functions ─────────────────────────────────────────────────

def render_stage(has_joke: bool):
    """Render the comedy stage SVG and elements."""
    curtain_style = "animation: none; transform: translateX(-80%);" if has_joke else ""
    curtain_style_r = "animation: none; transform: translateX(80%);" if has_joke else ""
    spotlight_opacity = "0.28" if has_joke else "0.14"

    stage_html = f"""
    <div class="theater-stage">
      <!-- Spotlight beams -->
      <div class="spotlight-beam s1"></div>
      <div class="spotlight-beam s2" style="border-top-color: rgba(255,240,180,{spotlight_opacity});"></div>
      <div class="spotlight-beam s3"></div>

      <!-- Top valance -->
      <div class="curtain-valance"></div>

      <!-- Stage lights -->
      <div class="stage-lights" style="margin-top:40px;">
        <div class="stage-light sl-gold sl-animate"></div>
        <div class="stage-light sl-white sl-animate-slow"></div>
        <div class="stage-light sl-neon sl-animate"></div>
        <div class="stage-light sl-gold sl-animate-slow"></div>
        <div class="stage-light sl-white sl-animate"></div>
        <div class="stage-light sl-neon sl-animate-slow"></div>
        <div class="stage-light sl-gold sl-animate"></div>
      </div>

      <!-- Curtains -->
      <div class="curtain-left" style="{curtain_style}"></div>
      <div class="curtain-right" style="{curtain_style_r}"></div>

      <!-- Microphone -->
      <div class="mic-wrap">
        <div class="mic-icon">🎤</div>
        <div class="mic-stand"></div>
        <div class="mic-base"></div>
      </div>

      <!-- Stage floor -->
      <div class="stage-floor">
        <div class="stage-planks"></div>
      </div>
    </div>

    <!-- Audience -->
    <div class="audience">
      <svg class="audience-svg" viewBox="0 0 820 70" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
        <defs>
          <radialGradient id="headGlow" cx="50%" cy="30%" r="60%">
            <stop offset="0%" stop-color="#2a1a08"/>
            <stop offset="100%" stop-color="#0a0a0f"/>
          </radialGradient>
        </defs>
        <!-- Row of audience silhouettes -->
        {"".join([f'<ellipse cx="{20+i*38}" cy="58" rx="14" ry="10" fill="#0f0a04"/><ellipse cx="{20+i*38}" cy="44" rx="9" ry="10" fill="url(#headGlow)"/>' for i in range(22)])}
        <!-- Glow bar -->
        <rect x="0" y="65" width="820" height="5" fill="url(#barGlow)" opacity="0.4"/>
        <defs>
          <linearGradient id="barGlow" x1="0" x2="1" y1="0" y2="0">
            <stop offset="0%" stop-color="transparent"/>
            <stop offset="50%" stop-color="#f0c040"/>
            <stop offset="100%" stop-color="transparent"/>
          </linearGradient>
        </defs>
      </svg>
    </div>
    """
    st.markdown(stage_html, unsafe_allow_html=True)


def render_joke_card(joke: str, num: int):
    """Render the premium joke display card."""
    st.markdown(f"""
    <div class="joke-card">
      <div class="joke-card-header">
        <span style="font-size:1.1rem">🎤</span>
        <span class="joke-card-label">Tonight's Performance</span>
        <span class="joke-card-num">No. {num:03d}</span>
      </div>
      <p class="joke-text">{joke}</p>
      <div class="joke-card-footer">
        <span class="joke-action-btn">👍 Like</span>
        <span class="joke-action-btn">📋 Copy</span>
        <span class="joke-action-btn">🔁 Encore</span>
        <span class="joke-action-btn">🌐 Share</span>
      </div>
    </div>
    """, unsafe_allow_html=True)


def render_neon_sign():
    st.markdown("""
    <div class="neon-sign">
      <div class="neon-title">😂 JokeBot Live</div>
      <div class="neon-subtitle">Tonight's Special Performance</div>
      <div class="neon-divider"></div>
    </div>
    """, unsafe_allow_html=True)


def render_request_booth():
    """Booth label + input + Send button all in one styled container."""
    st.markdown("""
    <div style="
      background: linear-gradient(145deg, #1a1408 0%, #0f0c04 100%);
      border: 1.5px solid #f0c040;
      border-radius: 12px;
      padding: 20px 20px 16px;
      margin: 8px 0 4px;
      box-shadow: 0 4px 24px rgba(0,0,0,0.5), inset 0 1px 0 rgba(240,192,64,0.15);
    ">
      <div style="font-size:0.6rem;letter-spacing:0.3em;color:#f0c040;font-weight:700;margin-bottom:12px;">
        🎟️&nbsp;&nbsp;REQUEST BOOTH
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Input + Send side by side
    col_in, col_btn = st.columns([5, 1])
    with col_in:
        user_input = st.text_input(
            "request",
            placeholder="What should our comedian perform today?",
            label_visibility="collapsed",
            key="user_request",
        )
    with col_btn:
        # Wrap only this button in a marker div so CSS can target it
        st.markdown('<div class="send-btn-wrap">', unsafe_allow_html=True)
        send = st.button("🎬 Send", use_container_width=True, key="btn_send")
        st.markdown('</div>', unsafe_allow_html=True)

    return user_input, send


def render_action_buttons():
    st.markdown("""
    <div style="font-size:0.6rem;letter-spacing:0.25em;text-transform:uppercase;
    color:#a09080;margin:14px 0 8px;text-align:center;">
      ✦ &nbsp; Quick Requests &nbsp; ✦
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    tell     = c1.button("🎤 Tell a Joke",       use_container_width=True, key="btn_tell")
    surprise = c2.button("🎲 Surprise Me",        use_container_width=True, key="btn_surprise")
    encore   = c3.button("👏 Encore",             use_container_width=True, key="btn_encore")
    random_  = c4.button("🎭 Random",             use_container_width=True, key="btn_random")
    return tell, surprise, encore, random_


def render_history():
    if not st.session_state.history:
        return
    st.markdown('<div class="hist-label">Previous Performances</div>', unsafe_allow_html=True)
    for i, item in enumerate(reversed(st.session_state.history), 1):
        n = len(st.session_state.history) - i + 1
        st.markdown(f"""
        <div class="hist-item">
          <span class="hist-num">#{n}</span>
          <span class="hist-text">{item}</span>
        </div>
        """, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="backstage-title">⭐ BACKSTAGE ⭐</div>', unsafe_allow_html=True)
        st.markdown('<div class="backstage-subtitle">Comedian\'s Lounge</div>', unsafe_allow_html=True)
        st.markdown("---")

        # Comedian card
        st.markdown(f"""
        <div class="comedian-card">
          <span class="comedian-avatar">🎭</span>
          <div class="comedian-name">JokeBot 3000</div>
          <div class="comedian-bio">
            AI comedian. Never sleeps. Tells jokes 24/7.<br>
            Powered by OpenRouter + API-Ninjas.<br>
            <em style="color:#f0c040;font-size:0.65rem;">⭐⭐⭐⭐⭐ — The Audience</em>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

        # Stats
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
              <div class="stat-num">{st.session_state.performances}</div>
              <div class="stat-lbl">Performances</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-card">
              <div class="stat-num">{st.session_state.laughs}</div>
              <div class="stat-lbl">Laughs</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("---")

        # Theme switcher
        st.markdown('<div style="font-size:0.62rem;letter-spacing:0.2em;text-transform:uppercase;color:#a09080;margin-bottom:8px;">🎨 Stage Theme</div>', unsafe_allow_html=True)
        theme_choice = st.radio(
            "theme",
            options=["dark", "vintage"],
            index=0 if st.session_state.theme == "dark" else 1,
            label_visibility="collapsed",
            horizontal=True,
        )
        if theme_choice != st.session_state.theme:
            st.session_state.theme = theme_choice
            st.rerun()

        st.markdown("---")
        if st.button("🗑️ Clear Stage", use_container_width=True):
            st.session_state.history      = []
            st.session_state.performances = 0
            st.session_state.laughs       = 0
            st.session_state.current_joke = None
            st.session_state.show_joke    = False
            st.rerun()


def fetch_joke(prompt: str) -> str:
    try:
        return agent_loop(prompt)
    except Exception as e:
        return f"The comedian tripped backstage: {e}"


# ── Main app ─────────────────────────────────────────────────────────────────
render_sidebar()
render_neon_sign()
render_stage(has_joke=st.session_state.show_joke)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# Request booth + buttons
user_input, send = render_request_booth()
tell, surprise, encore, random_ = render_action_buttons()

# Determine what to do
prompt_map = {
    "surprise": "Tell me a surprising joke",
    "encore":   "Tell me another joke, make it different",
    "random":   "Give me a completely random joke",
}
final_prompt = None
if (send or tell) and user_input.strip(): final_prompt = user_input.strip()
if (send or tell) and not user_input.strip(): final_prompt = "Tell me a joke"
if surprise: final_prompt = prompt_map["surprise"]
if encore:   final_prompt = prompt_map["encore"]
if random_:  final_prompt = prompt_map["random"]

if final_prompt:
    with st.spinner("🎤 The comedian is warming up..."):
        joke = fetch_joke(final_prompt)
    st.session_state.current_joke  = joke
    st.session_state.show_joke     = True
    st.session_state.performances += 1
    st.session_state.laughs       += random.randint(3, 12)
    if joke not in st.session_state.history:
        st.session_state.history.append(joke)
    inject_js()
    st.rerun()

# Show joke card
if st.session_state.show_joke and st.session_state.current_joke:
    render_joke_card(st.session_state.current_joke, st.session_state.performances)

render_history()

# Footer
st.markdown("""
<div class="theater-footer">
  <p>✦ &nbsp; JokeBot Live &nbsp; ✦</p>
  <p>Powered by OpenRouter &nbsp;·&nbsp; API-Ninjas &nbsp;·&nbsp; Streamlit</p>
</div>
""", unsafe_allow_html=True)