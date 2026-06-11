import streamlit as st

from src.constants.colors import (
    ACCENT,
    BG_CARD,
    BG_DEEP,
    BG_SURFACE,
    BORDER,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)

_LIGHT = {
    "bg":     "#F0F4F8",
    "card":   "#FFFFFF",
    "sidebar":"#1A2332",
    "text":   "#0F172A",
    "text2":  "#334155",
    "border": "#CBD5E1",
    "muted":  "#64748B",
}


def inject_css():
    dark = st.session_state.get("dark_mode", True)

    bg     = BG_DEEP    if dark else _LIGHT["bg"]
    card   = BG_CARD    if dark else _LIGHT["card"]
    text   = TEXT_PRIMARY   if dark else _LIGHT["text"]
    text2  = TEXT_SECONDARY if dark else _LIGHT["text2"]
    border = BORDER     if dark else _LIGHT["border"]
    muted  = TEXT_MUTED if dark else _LIGHT["muted"]

    cal_css = f"""
    [data-testid="stDateInput"] input {{
        background-color: {"#0D1526" if dark else "#FFFFFF"} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        border-radius: 8px !important;
    }}
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] *,
    div[data-baseweb="calendar"],
    div[data-baseweb="calendar"] *,
    [role="grid"], [role="grid"] *,
    [role="gridcell"], [role="gridcell"] * {{
        background-color: #FFFFFF !important;
        color: #111827 !important;
        border-color: #E2E8F0 !important;
    }}
    div[data-baseweb="popover"] select {{
        background-color: #FFFFFF !important;
        color: #111827 !important;
    }}
    [role="columnheader"], [role="columnheader"] span {{
        color: #6B7280 !important;
    }}
    div[data-baseweb="calendar"] [aria-selected="true"] div,
    div[data-baseweb="calendar"] [aria-selected="true"] button {{
        background-color: {ACCENT} !important;
        color: #FFFFFF !important;
    }}
    """

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* ══════════════════════════════════════════════
       BASE
    ══════════════════════════════════════════════ */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
        background-color: {bg} !important;
        color: {text} !important;
        font-family: 'Inter', sans-serif !important;
    }}
    [data-testid="stMainBlockContainer"], section.main > div {{
        background-color: {bg} !important;
        padding-top: 1.5rem !important;
    }}

    /* ══════════════════════════════════════════════
       SIDEBAR
    ══════════════════════════════════════════════ */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0A1628 0%, #060B14 100%) !important;
        border-right: 1px solid {ACCENT}22 !important;
    }}
    [data-testid="stSidebar"] > div:first-child {{
        background: transparent !important;
        padding: 1.5rem 1rem !important;
    }}
    [data-testid="stSidebar"] * {{
        color: #E8F4FF !important;
    }}
    [data-testid="stSidebar"] .stMarkdown h2 {{
        font-size: 1.2rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
        color: #FFFFFF !important;
        margin-bottom: 0 !important;
    }}
    [data-testid="stSidebar"] .stMarkdown small,
    [data-testid="stSidebar"] .stCaptionContainer p {{
        color: {ACCENT} !important;
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
    }}

    /* Nav radio — styled as buttons */
    [data-testid="stSidebar"] [data-testid="stRadio"] > div {{
        gap: 4px !important;
        flex-direction: column !important;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] label {{
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
        display: flex !important;
        align-items: center !important;
        color: #C8DCF0 !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        margin: 0 !important;
        width: 100% !important;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] label p,
    [data-testid="stSidebar"] [data-testid="stRadio"] label span {{
        color: #C8DCF0 !important;
        font-weight: 500 !important;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {{
        background: rgba(0,168,255,0.1) !important;
        border-color: {ACCENT}44 !important;
        color: #FFFFFF !important;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover p,
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover span {{
        color: #FFFFFF !important;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"],
    [data-testid="stSidebar"] [data-testid="stRadio"] [aria-checked="true"] ~ div label {{
        background: rgba(0,168,255,0.18) !important;
        border-color: {ACCENT}66 !important;
        color: {ACCENT} !important;
        font-weight: 700 !important;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"] p,
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"] span {{
        color: {ACCENT} !important;
        font-weight: 700 !important;
    }}
    /* Hide the actual radio dot */
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"],
    [data-testid="stSidebar"] [data-testid="stRadio"] svg {{
        display: none !important;
    }}
    /* "Navigation" label above radio */
    [data-testid="stSidebar"] [data-testid="stRadio"] > label {{
        color: #7A9BBC !important;
        font-size: 0.65rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        padding: 0 !important;
        background: none !important;
        border: none !important;
    }}

    /* Settings toggle */
    [data-testid="stSidebar"] [data-testid="stToggle"] {{
        background: rgba(0,168,255,0.08) !important;
        border: 1px solid {ACCENT}22 !important;
        border-radius: 8px !important;
        padding: 6px 10px !important;
    }}

    /* Logged-in label */
    [data-testid="stSidebar"] small {{
        color: #6B8CAE !important;
        font-size: 0.72rem !important;
    }}
    [data-testid="stSidebar"] small b {{
        color: {ACCENT} !important;
    }}

    /* Sign out button */
    [data-testid="stSidebar"] [data-testid="stButton"] > button {{
        background: rgba(255,23,68,0.08) !important;
        color: #FF6B8A !important;
        border: 1px solid rgba(255,23,68,0.25) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
        width: 100% !important;
        padding: 0.5rem !important;
    }}
    [data-testid="stSidebar"] [data-testid="stButton"] > button:hover {{
        background: rgba(255,23,68,0.18) !important;
        border-color: rgba(255,23,68,0.5) !important;
        color: #FF4069 !important;
    }}
    [data-testid="stSidebar"] [data-testid="stButton"] > button p,
    [data-testid="stSidebar"] [data-testid="stButton"] > button span {{
        color: inherit !important;
    }}

    /* ══════════════════════════════════════════════
       MAIN CONTENT BUTTONS (non-sidebar)
    ══════════════════════════════════════════════ */
    [data-testid="stMain"] div[data-testid="stButton"] > button,
    [data-testid="stMain"] div[data-testid="stFormSubmitButton"] > button {{
        background: linear-gradient(135deg, {ACCENT} 0%, #0066CC 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        padding: 0.5rem 1.2rem !important;
        box-shadow: 0 4px 15px rgba(0,168,255,0.25) !important;
        letter-spacing: 0.01em !important;
        transition: all 0.2s ease !important;
    }}
    [data-testid="stMain"] div[data-testid="stButton"] > button:hover,
    [data-testid="stMain"] div[data-testid="stFormSubmitButton"] > button:hover {{
        box-shadow: 0 6px 20px rgba(0,168,255,0.4) !important;
        transform: translateY(-1px) !important;
        background: linear-gradient(135deg, #22C1FF 0%, {ACCENT} 100%) !important;
    }}
    [data-testid="stMain"] div[data-testid="stButton"] > button p,
    [data-testid="stMain"] div[data-testid="stButton"] > button span,
    [data-testid="stMain"] div[data-testid="stFormSubmitButton"] > button p,
    [data-testid="stMain"] div[data-testid="stFormSubmitButton"] > button span {{
        color: #FFFFFF !important;
    }}

    /* ══════════════════════════════════════════════
       FILE UPLOADER
    ══════════════════════════════════════════════ */
    [data-testid="stFileUploader"] section {{
        background: linear-gradient(135deg, {card} 0%, {"#0D1A2D" if dark else "#F8FBFF"} 100%) !important;
        border: 2px dashed {ACCENT}44 !important;
        border-radius: 12px !important;
        transition: border-color 0.2s !important;
    }}
    [data-testid="stFileUploader"] section:hover {{
        border-color: {ACCENT}99 !important;
    }}
    [data-testid="stFileUploader"] section span,
    [data-testid="stFileUploader"] section p,
    [data-testid="stFileUploader"] section small,
    [data-testid="stFileUploaderDropzoneInstructions"] span,
    [data-testid="stFileUploaderDropzoneInstructions"] p,
    [data-testid="stFileUploaderDropzoneInstructions"] small,
    [data-testid="stFileUploader"] * {{
        color: #FFFFFF !important;
    }}
    [data-testid="stFileUploader"] label {{
        color: {text} !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }}
    [data-testid="stFileUploader"] button,
    button[data-testid="baseButton-secondary"] {{
        background: linear-gradient(135deg, {ACCENT} 0%, #0066CC 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(0,168,255,0.2) !important;
    }}
    [data-testid="stFileUploader"] button span,
    button[data-testid="baseButton-secondary"] span {{
        color: #FFFFFF !important;
    }}
    [data-testid="stFileUploader"] button svg *,
    button[data-testid="baseButton-secondary"] svg * {{
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
    }}

    /* ══════════════════════════════════════════════
       METRICS
    ══════════════════════════════════════════════ */
    [data-testid="stMetric"] {{
        background: {card} !important;
        border: 1px solid {border} !important;
        border-top: 3px solid {ACCENT} !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2) !important;
    }}
    [data-testid="stMetricLabel"] > div,
    [data-testid="stMetricLabel"] p {{
        color: {muted} !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
    }}
    [data-testid="stMetricValue"] > div,
    [data-testid="stMetricValue"] p {{
        color: {ACCENT} !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
    }}

    /* ══════════════════════════════════════════════
       TEXT
    ══════════════════════════════════════════════ */
    [data-testid="stMain"] p,
    [data-testid="stMain"] li,
    [data-testid="stMain"] label {{
        color: {text} !important;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {text} !important;
        font-weight: 700 !important;
    }}
    [data-testid="stMarkdownContainer"] p {{
        color: {text2} !important;
    }}

    /* ══════════════════════════════════════════════
       ALERT / INFO BOXES — dark themed
    ══════════════════════════════════════════════ */
    [data-testid="stAlert"] {{
        background-color: {"rgba(0,168,255,0.08)" if dark else "#EFF6FF"} !important;
        border-left: 3px solid {ACCENT} !important;
        border-radius: 10px !important;
        border-top: none !important;
        border-right: none !important;
        border-bottom: none !important;
    }}
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span {{
        color: {ACCENT if dark else "#1D4ED8"} !important;
        font-weight: 500 !important;
    }}

    /* Success alert */
    [data-testid="stNotification"] {{
        background: rgba(0,230,118,0.1) !important;
        border-left: 3px solid #00E676 !important;
        border-radius: 10px !important;
    }}

    /* ══════════════════════════════════════════════
       TEXT INPUT
    ══════════════════════════════════════════════ */
    [data-testid="stTextInput"] input {{
        background-color: {card} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        border-radius: 10px !important;
        padding: 0.6rem 1rem !important;
        font-size: 0.95rem !important;
        transition: border-color 0.2s !important;
    }}
    [data-testid="stTextInput"] input:focus {{
        border-color: {ACCENT} !important;
        box-shadow: 0 0 0 3px {ACCENT}22 !important;
    }}
    [data-testid="stTextInput"] label {{
        color: {text} !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        letter-spacing: 0.02em !important;
    }}

    /* ══════════════════════════════════════════════
       DATAFRAME
    ══════════════════════════════════════════════ */
    [data-testid="stDataFrame"] {{
        border: 1px solid {border} !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15) !important;
    }}

    hr {{
        border: none !important;
        border-top: 1px solid {border} !important;
        opacity: 0.5 !important;
    }}

    /* Spinner */
    [data-testid="stSpinner"] p {{
        color: {ACCENT} !important;
    }}

    /* ══════════════════════════════════════════════
       CUSTOM COMPONENTS
    ══════════════════════════════════════════════ */
    .kpi-card {{
        background: {card} !important;
        border: 1px solid {border} !important;
        border-top: 3px solid {ACCENT} !important;
        border-radius: 14px !important;
        padding: 22px 20px !important;
        text-align: center !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2) !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
        position: relative !important;
        overflow: hidden !important;
    }}
    .kpi-card::before {{
        content: '' !important;
        position: absolute !important;
        top: 0; left: 0; right: 0 !important;
        height: 60px !important;
        background: linear-gradient(180deg, {ACCENT}0D 0%, transparent 100%) !important;
    }}
    .kpi-value {{
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        color: {ACCENT} !important;
        line-height: 1.1 !important;
        letter-spacing: -0.03em !important;
    }}
    .kpi-label {{
        font-size: 0.7rem !important;
        color: {muted} !important;
        margin-top: 6px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        font-weight: 700 !important;
    }}

    .section-title {{
        font-size: 0.7rem !important;
        font-weight: 800 !important;
        color: {ACCENT} !important;
        padding-bottom: 8px !important;
        border-bottom: 1px solid {ACCENT}33 !important;
        margin-bottom: 18px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.12em !important;
    }}

    .badge {{
        display: inline-flex !important;
        align-items: center !important;
        gap: 4px !important;
        padding: 4px 14px !important;
        border-radius: 999px !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
    }}
    .badge-green  {{ background: rgba(0,230,118,0.12) !important; color: #00E676 !important; border: 1px solid rgba(0,230,118,0.3) !important; }}
    .badge-red    {{ background: rgba(255,23,68,0.12) !important;  color: #FF1744 !important; border: 1px solid rgba(255,23,68,0.3) !important; }}
    .badge-yellow {{ background: rgba(255,145,0,0.12) !important;  color: #FF9100 !important; border: 1px solid rgba(255,145,0,0.3) !important; }}
    .badge-blue   {{ background: rgba(0,168,255,0.12) !important;  color: {ACCENT} !important; border: 1px solid rgba(0,168,255,0.3) !important; }}

    {cal_css}

    /* ══════════════════════════════════════════════
       TOP STATUS BAR
    ══════════════════════════════════════════════ */
    .status-bar {{
        display: flex !important;
        align-items: center !important;
        gap: 0 !important;
        background: {"#0A1628" if dark else "#FFFFFF"} !important;
        border: 1px solid {border} !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        margin-bottom: 6px !important;
        flex-wrap: wrap !important;
    }}
    .sb-item {{
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
        padding: 0 16px !important;
    }}
    .sb-sep {{
        width: 1px !important;
        height: 20px !important;
        background: {border} !important;
    }}
    .sb-label {{
        font-size: 0.62rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        color: {muted} !important;
    }}
    .sb-val {{
        font-size: 0.82rem !important;
        font-weight: 700 !important;
        color: {text} !important;
    }}
    .val-green {{ color: #00E676 !important; }}
    .val-gray  {{ color: #6B8CAE !important; }}
    .sb-dot {{ display:inline-block;width:8px;height:8px;border-radius:50%; }}
    .dot-green {{ background:#00E676 !important; box-shadow:0 0 6px #00E676 !important; }}
    .dot-gray  {{ background:#3A5A7A !important; }}
    .live-badge {{
        display: inline-flex !important;
        align-items: center !important;
        padding: 3px 10px !important;
        background: rgba(0,230,118,0.12) !important;
        color: #00E676 !important;
        border: 1px solid rgba(0,230,118,0.35) !important;
        border-radius: 999px !important;
        font-size: 0.68rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.08em !important;
    }}
    .live-badge-off {{
        display: inline-flex !important;
        align-items: center !important;
        padding: 3px 10px !important;
        background: rgba(107,140,174,0.1) !important;
        color: #6B8CAE !important;
        border: 1px solid rgba(107,140,174,0.3) !important;
        border-radius: 999px !important;
        font-size: 0.68rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.08em !important;
    }}

    /* ══════════════════════════════════════════════
       SCANNER FRAME
    ══════════════════════════════════════════════ */
    .scanner-frame {{
        position: relative !important;
        background: {"#070E1A" if dark else "#F0F4F8"} !important;
        border: 1px solid {border} !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        padding: 4px !important;
    }}
    .corner {{
        position: absolute !important;
        width: 18px !important;
        height: 18px !important;
        z-index: 10 !important;
        pointer-events: none !important;
    }}
    .corner-tl {{ top:8px; left:8px; border-top:2px solid {ACCENT}; border-left:2px solid {ACCENT}; border-radius:3px 0 0 0; }}
    .corner-tr {{ top:8px; right:8px; border-top:2px solid {ACCENT}; border-right:2px solid {ACCENT}; border-radius:0 3px 0 0; }}
    .corner-bl {{ bottom:8px; left:8px; border-bottom:2px solid {ACCENT}; border-left:2px solid {ACCENT}; border-radius:0 0 0 3px; }}
    .corner-br {{ bottom:8px; right:8px; border-bottom:2px solid {ACCENT}; border-right:2px solid {ACCENT}; border-radius:0 0 3px 0; }}
    .board-info-bar {{
        display: flex !important;
        gap: 0 !important;
        background: {"rgba(6,11,20,0.9)" if dark else "rgba(240,244,248,0.95)"} !important;
        border-top: 1px solid {border} !important;
        padding: 8px 16px !important;
        flex-wrap: wrap !important;
    }}
    .bi-item {{
        display: flex !important;
        flex-direction: column !important;
        gap: 1px !important;
        padding: 0 24px 0 0 !important;
    }}
    .bi-label {{
        font-size: 0.6rem !important;
        color: {muted} !important;
        font-weight: 700 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
    }}
    .bi-val {{
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        color: {text} !important;
        display: flex !important;
        align-items: center !important;
    }}

    /* ══════════════════════════════════════════════
       DETECTION SUMMARY MINI GRID
    ══════════════════════════════════════════════ */
    .mini-stats-grid {{
        display: grid !important;
        grid-template-columns: 1fr 1fr !important;
        gap: 8px !important;
        margin-bottom: 4px !important;
    }}
    .mini-stat-card {{
        background: {card} !important;
        border: 1px solid {border} !important;
        border-radius: 10px !important;
        padding: 12px 14px !important;
    }}
    .ms-green  {{ border-left: 3px solid #00E676 !important; }}
    .ms-red    {{ border-left: 3px solid #FF1744 !important; }}
    .ms-accent {{ border-left: 3px solid {ACCENT} !important; }}
    .ms-label {{
        font-size: 0.6rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        color: {muted} !important;
        margin-bottom: 4px !important;
    }}
    .ms-value {{
        font-size: 1.35rem !important;
        font-weight: 800 !important;
        color: {text} !important;
        letter-spacing: -0.02em !important;
        line-height: 1.1 !important;
    }}
    .ms-sub {{
        font-size: 0.68rem !important;
        color: {muted} !important;
        margin-top: 2px !important;
        font-weight: 600 !important;
    }}

    /* ══════════════════════════════════════════════
       LIVE DEFECTS LIST
    ══════════════════════════════════════════════ */
    .live-defects-list {{
        display: flex !important;
        flex-direction: column !important;
        gap: 4px !important;
    }}
    .ld-list-row {{
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
        padding: 7px 10px !important;
        background: {card} !important;
        border-radius: 8px !important;
        border: 1px solid {border} !important;
    }}
    .ld-dot {{
        width: 8px !important;
        height: 8px !important;
        border-radius: 50% !important;
        flex-shrink: 0 !important;
    }}
    .ld-time {{
        font-size: 0.68rem !important;
        color: {muted} !important;
        font-weight: 600 !important;
        min-width: 54px !important;
        font-family: monospace !important;
    }}
    .ld-type {{
        font-size: 0.78rem !important;
        font-weight: 700 !important;
        flex: 1 !important;
    }}
    .ld-conf {{
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        color: {muted} !important;
    }}

    /* ══════════════════════════════════════════════
       INSPECTION LOG
    ══════════════════════════════════════════════ */
    .inspection-log {{
        display: flex !important;
        flex-direction: column !important;
        gap: 3px !important;
        background: {card} !important;
        border: 1px solid {border} !important;
        border-radius: 10px !important;
        padding: 10px !important;
        font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    }}
    .log-row {{
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        padding: 4px 6px !important;
        border-radius: 5px !important;
        font-size: 0.75rem !important;
    }}
    .log-tag {{
        font-size: 0.65rem !important;
        font-weight: 800 !important;
        padding: 1px 6px !important;
        border-radius: 4px !important;
        flex-shrink: 0 !important;
    }}
    .tag-detect {{
        background: rgba(255,64,105,0.15) !important;
        color: #FF4069 !important;
        border: 1px solid rgba(255,64,105,0.3) !important;
    }}
    .log-time {{
        color: {muted} !important;
        font-size: 0.7rem !important;
        min-width: 56px !important;
    }}
    .log-type {{
        font-weight: 700 !important;
        flex: 1 !important;
    }}
    .log-conf {{
        color: {muted} !important;
        font-size: 0.7rem !important;
    }}

    /* ══════════════════════════════════════════════
       SIDEBAR MODEL INFO CARD
    ══════════════════════════════════════════════ */
    .model-info-card {{
        background: rgba(0,168,255,0.06) !important;
        border: 1px solid rgba(0,168,255,0.15) !important;
        border-radius: 10px !important;
        padding: 12px 14px !important;
        margin-top: 16px !important;
    }}
    .mi-label {{
        font-size: 0.6rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        color: #6B8CAE !important;
        margin-bottom: 3px !important;
    }}
    .mi-val {{
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        color: #E8F4FF !important;
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
    }}
    .mi-badge {{
        font-size: 0.6rem !important;
        background: rgba(0,168,255,0.2) !important;
        color: #00A8FF !important;
        padding: 1px 6px !important;
        border-radius: 4px !important;
        font-weight: 700 !important;
    }}

    /* ══════════════════════════════════════════════
       PAGE HEADER
    ══════════════════════════════════════════════ */
    .page-header {{
        margin-bottom: 24px !important;
    }}
    .page-title {{
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        color: {text} !important;
        letter-spacing: -0.03em !important;
        line-height: 1.1 !important;
    }}
    .page-subtitle {{
        font-size: 0.82rem !important;
        color: {muted} !important;
        margin-top: 4px !important;
        font-weight: 500 !important;
    }}

    /* ══════════════════════════════════════════════
       HERO STATUS CARD (Dashboard)
    ══════════════════════════════════════════════ */
    .hero-card {{
        background: linear-gradient(135deg, {"#0A1E3A" if dark else "#EFF6FF"} 0%, {card} 100%) !important;
        border: 1px solid {ACCENT}33 !important;
        border-left: 4px solid {ACCENT} !important;
        border-radius: 14px !important;
        padding: 24px 28px !important;
        box-shadow: 0 8px 32px rgba(0,168,255,0.08) !important;
    }}
    .hero-label {{
        font-size: 0.65rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.14em !important;
        text-transform: uppercase !important;
        color: {ACCENT} !important;
        margin-bottom: 8px !important;
    }}
    .hero-title {{
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        color: {text} !important;
        letter-spacing: -0.02em !important;
    }}
    .hero-sub {{
        font-size: 0.85rem !important;
        color: {muted} !important;
        margin-top: 4px !important;
    }}

    /* ══════════════════════════════════════════════
       STATUS CARDS (Live Detection sidebar)
    ══════════════════════════════════════════════ */
    .status-card {{
        background: {card} !important;
        border: 1px solid {border} !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        margin-bottom: 10px !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.15) !important;
    }}
    .status-card-icon {{
        font-size: 1.1rem !important;
        margin-bottom: 6px !important;
        opacity: 0.7 !important;
    }}
    .status-card-label {{
        font-size: 0.65rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        color: {muted} !important;
        margin-bottom: 2px !important;
    }}
    .status-card-value {{
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        color: {text} !important;
    }}
    .status-card-state {{
        font-size: 0.7rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.06em !important;
        margin-top: 4px !important;
    }}
    .state-ok  {{ color: #00E676 !important; }}
    .state-off {{ color: #6B8CAE !important; }}

    /* ══════════════════════════════════════════════
       STREAM OFFLINE PLACEHOLDER
    ══════════════════════════════════════════════ */
    .stream-offline {{
        background: {card} !important;
        border: 1px solid {border} !important;
        border-radius: 14px !important;
        padding: 60px 24px !important;
        text-align: center !important;
        min-height: 280px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    .stream-offline-icon {{
        font-size: 3rem !important;
        opacity: 0.25 !important;
        margin-bottom: 16px !important;
    }}
    .stream-offline-title {{
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        color: {text} !important;
        opacity: 0.7 !important;
    }}
    .stream-offline-sub {{
        font-size: 0.8rem !important;
        color: {muted} !important;
        margin-top: 6px !important;
    }}

    /* ══════════════════════════════════════════════
       EMPTY STATE (Manual Inspection)
    ══════════════════════════════════════════════ */
    .empty-state {{
        background: {card} !important;
        border: 2px dashed {ACCENT}33 !important;
        border-radius: 14px !important;
        padding: 60px 24px !important;
        text-align: center !important;
        margin: 8px 0 !important;
    }}
    .empty-state-icon {{
        font-size: 2.8rem !important;
        opacity: 0.3 !important;
        margin-bottom: 16px !important;
    }}
    .empty-state-title {{
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        color: {text} !important;
        margin-bottom: 6px !important;
    }}
    .empty-state-sub {{
        font-size: 0.82rem !important;
        color: {muted} !important;
    }}

    /* ══════════════════════════════════════════════
       LATEST DETECTION CARD
    ══════════════════════════════════════════════ */
    .latest-detection-card {{
        background: {card} !important;
        border: 1px solid {border} !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 8px !important;
    }}
    .ld-row {{
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
    }}
    .ld-key {{
        font-size: 0.72rem !important;
        color: {muted} !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
    }}
    .ld-val {{
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        color: {text} !important;
    }}
    .ld-val.accent {{ color: {ACCENT} !important; }}

    /* ══════════════════════════════════════════════
       SIDEBAR — ALWAYS VISIBLE, NO COLLAPSE
    ══════════════════════════════════════════════ */
    /* Force sidebar open regardless of saved state */
    [data-testid="stSidebar"] {{
        transform: translateX(0) !important;
        min-width: 244px !important;
        width: 244px !important;
        left: 0 !important;
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }}
    /* Hide the reopen arrow that appears when collapsed */
    [data-testid="collapsedControl"],
    button[data-testid="baseButton-header"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebar"] button[kind="header"],
    section[data-testid="stSidebar"] > div > div > button {{
        display: none !important;
    }}

    /* ══════════════════════════════════════════════
       HIDE STREAMLIT CHROME (header bar + toolbar)
    ══════════════════════════════════════════════ */
    #MainMenu, footer,
    [data-testid="stDeployButton"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stHeader"],
    header[data-testid="stHeader"],
    .stAppHeader,
    div[class*="AppHeader"] {{
        visibility: hidden !important;
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        max-height: 0 !important;
        overflow: hidden !important;
        padding: 0 !important;
        margin: 0 !important;
    }}
    </style>
    """, unsafe_allow_html=True)
