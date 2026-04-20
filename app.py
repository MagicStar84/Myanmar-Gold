"""
╔══════════════════════════════════════════════════════════════╗
║       မြန်မာ ရွှေဈေးနှုန်း PRO  ·  v3.0                   ║
║  Live XAUUSD · SMC Analysis · Myanmar Gold Calculations       ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import yfinance as yf
from datetime import datetime, timedelta

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="🥇 Myanmar Gold Pro",
    page_icon="🥇",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"About": "Myanmar Gold Market Pro · SMC Analysis Dashboard"}
)

# ═══════════════════════════════════════════════════════════════
# CUSTOM CSS  ·  Dark Gold Theme
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,600;0,9..40,700;0,9..40,800;1,9..40,400&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

/* ── Background ── */
.stApp { background: #08080c; color: #f0ead8; }
.stApp > header { background: transparent !important; }
[data-testid="stHeader"] { background: transparent !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0d0c09;
    border-right: 1px solid rgba(255,215,0,0.08);
}

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: linear-gradient(150deg,#14120e 0%,#0b0a07 100%);
    border: 1px solid rgba(255,215,0,0.12);
    border-radius: 14px;
    padding: 14px 18px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.4);
}
[data-testid="metric-container"] label {
    color: #c0a860 !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] > div {
    background: linear-gradient(135deg,#fff5b8,#ffd700,#e8a800);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
}
[data-testid="stMetricDelta"] svg { display: none; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,215,0,0.03);
    border: 1px solid rgba(255,215,0,0.07);
    border-radius: 12px;
    gap: 4px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    color: #887a5a !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    border-radius: 8px !important;
    padding: 8px 20px !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(255,215,0,0.1) !important;
    color: #ffd700 !important;
    border: 1px solid rgba(255,215,0,0.22) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 20px; }

/* ── Buttons ── */
.stButton > button {
    background: rgba(255,215,0,0.07) !important;
    border: 1px solid rgba(255,215,0,0.25) !important;
    color: #ffd700 !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    transition: all .15s !important;
}
.stButton > button:hover {
    background: rgba(255,215,0,0.15) !important;
    border-color: rgba(255,215,0,0.45) !important;
}

/* ── Inputs ── */
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,215,0,0.15) !important;
    border-radius: 10px !important;
    color: #ffd700 !important;
    font-weight: 700 !important;
    font-size: 18px !important;
}
.stSelectbox > div > div {
    background: rgba(20,18,14,0.9) !important;
    border: 1px solid rgba(255,215,0,0.15) !important;
    border-radius: 10px !important;
    color: #f0ead8 !important;
}

/* ── Radio ── */
.stRadio > div { gap: 8px !important; }
.stRadio label { color: #c0a860 !important; font-weight: 600 !important; }

/* ── Divider ── */
hr { border-color: rgba(255,215,0,0.07) !important; margin: 16px 0 !important; }

/* ── Spinner ── */
.stSpinner > div > div { border-top-color: #ffd700 !important; }

/* ── Alerts ── */
.stAlert { border-radius: 10px !important; }

/* ── Hide branding ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Custom card styles ── */
.gc { background:linear-gradient(150deg,#14120e 0%,#0b0a07 100%);
      border:1px solid rgba(255,215,0,0.13);border-radius:16px;
      padding:18px 20px;margin-bottom:12px;
      box-shadow:0 2px 20px rgba(0,0,0,0.45); }
.gc-hl { border-color:rgba(255,215,0,0.25);
          box-shadow:0 4px 28px rgba(255,215,0,0.06),inset 0 1px 0 rgba(255,215,0,0.06); }
.cl { font-size:10px;font-weight:700;color:#c0a860;text-transform:uppercase;
      letter-spacing:1.5px;margin-bottom:8px; }
.pb { font-size:40px;font-weight:800;line-height:1.05;
      background:linear-gradient(135deg,#fff5b8,#ffd700,#e8a800);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent; }
.up { color:#00ff88 !important;font-weight:700; }
.dn { color:#ff4455 !important;font-weight:700; }
.nt { color:#ffaa00 !important;font-weight:700; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:#0a0907; }
::-webkit-scrollbar-thumb { background:rgba(255,215,0,0.18);border-radius:3px; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════
TROY_OZ   = 31.1035
PAEL_G    = 16.6
CBM_FALLBACK = 2100.0

# ═══════════════════════════════════════════════════════════════
# ── DATA LAYER ──────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════

@st.cache_data(ttl=30, show_spinner=False)
def fetch_live() -> dict | None:
    """Binance XAUUSDT → Coinbase XAU-USD fallback"""
    # Binance
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol=XAUUSDT", timeout=8)
        d = r.json()
        if "lastPrice" in d:
            return dict(
                price=float(d["lastPrice"]), change=float(d["priceChange"]),
                pct=float(d["priceChangePercent"]),
                high=float(d["highPrice"]), low=float(d["lowPrice"]),
                vol=float(d["volume"]), src="Binance XAUUSDT"
            )
    except Exception:
        pass
    # Coinbase
    try:
        r = requests.get("https://api.coinbase.com/v2/prices/XAU-USD/spot", timeout=8)
        p = float(r.json()["data"]["amount"])
        return dict(price=p, change=0, pct=0, high=0, low=0, vol=0, src="Coinbase XAU-USD")
    except Exception:
        pass
    return None


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_cbm() -> dict:
    """CBM USD/MMK rate with fallbacks"""
    # CBM Direct
    try:
        r = requests.get("https://forex.cbm.gov.mm/api/latest", timeout=8)
        d = r.json(); rate = float(d["rates"]["USD"])
        if rate > 0:
            return dict(rate=rate, src="CBM Direct", date=d.get("info", {}).get("date", ""))
    except Exception:
        pass
    # AllOrigins proxy
    try:
        url = "https://api.allorigins.win/raw?url=" + \
              "https%3A%2F%2Fforex.cbm.gov.mm%2Fapi%2Flatest"
        r = requests.get(url, timeout=10); d = r.json()
        rate = float(d["rates"]["USD"])
        if rate > 0:
            return dict(rate=rate, src="CBM (proxy)", date="")
    except Exception:
        pass
    # Open ER-API
    try:
        r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=8)
        d = r.json(); rate = float(d["rates"]["MMK"])
        if rate > 0:
            return dict(rate=rate, src="Open ER-API", date="")
    except Exception:
        pass
    return dict(rate=CBM_FALLBACK, src="Offline default", date="")


@st.cache_data(ttl=300, show_spinner=False)
def fetch_ohlcv(period: str = "3mo", interval: str = "1d") -> pd.DataFrame:
    """Gold Futures OHLCV via yfinance (GC=F)"""
    try:
        df = yf.Ticker("GC=F").history(period=period, interval=interval)
        if df.empty:
            df = yf.Ticker("XAUUSD=X").history(period=period, interval=interval)
        df = df[["Open", "High", "Low", "Close", "Volume"]].dropna()
        df.index = pd.to_datetime(df.index).tz_localize(None)
        return df
    except Exception:
        return pd.DataFrame()

# ═══════════════════════════════════════════════════════════════
# ── SMC ENGINE ──────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════

def find_pivots(df: pd.DataFrame, left: int = 5, right: int = 5):
    n = len(df)
    sh, sl = [], []
    for i in range(left, n - right):
        h = df["High"].iloc[i]
        if all(h > df["High"].iloc[i-j] for j in range(1, left+1)) and \
           all(h > df["High"].iloc[i+j] for j in range(1, right+1)):
            sh.append({"idx": i, "price": h, "date": df.index[i]})
        l = df["Low"].iloc[i]
        if all(l < df["Low"].iloc[i-j] for j in range(1, left+1)) and \
           all(l < df["Low"].iloc[i+j] for j in range(1, right+1)):
            sl.append({"idx": i, "price": l, "date": df.index[i]})
    return sh, sl


def market_structure(df, sh, sl):
    """HH/HL/LH/LL → trend + BOS/CHoCH events"""
    trend, events = "RANGING", []
    if len(sh) < 2 or len(sl) < 2:
        return trend, events

    r_sh = sorted(sh, key=lambda x: x["idx"])[-4:]
    r_sl = sorted(sl, key=lambda x: x["idx"])[-4:]
    hh = r_sh[-1]["price"] > r_sh[-2]["price"]
    hl = r_sl[-1]["price"] > r_sl[-2]["price"]
    lh = r_sh[-1]["price"] < r_sh[-2]["price"]
    ll = r_sl[-1]["price"] < r_sl[-2]["price"]

    if hh and hl:   trend = "BULLISH"
    elif lh and ll: trend = "BEARISH"

    cp = df["Close"].iloc[-1]
    ph = sh[-1]["price"]; pl = sl[-1]["price"]

    if cp > ph:
        events.append(dict(type="BOS", dir="UP",   level=ph, label="BOS ▲"))
    if cp < pl:
        events.append(dict(type="BOS", dir="DOWN", level=pl, label="BOS ▼"))
    if trend == "BULLISH" and cp < pl:
        events.append(dict(type="CHoCH", dir="DOWN", level=pl, label="CHoCH ▼  (Reversal Alert)"))
    elif trend == "BEARISH" and cp > ph:
        events.append(dict(type="CHoCH", dir="UP",   level=ph, label="CHoCH ▲  (Reversal Alert)"))

    return trend, events


def order_blocks(df, sh, sl, n=4):
    """Bullish OB = last bearish candle before swing low; Bearish OB = vice versa"""
    obs = []
    for pt in sl[-n:]:
        for i in range(pt["idx"]-1, max(0, pt["idx"]-12), -1):
            o, c = df["Open"].iloc[i], df["Close"].iloc[i]
            if c < o:  # bearish candle → bullish OB
                obs.append(dict(type="BULLISH", top=o, bottom=c, mid=(o+c)/2,
                                date=df.index[i], idx=i, label="Bull OB"))
                break
    for pt in sh[-n:]:
        for i in range(pt["idx"]-1, max(0, pt["idx"]-12), -1):
            o, c = df["Open"].iloc[i], df["Close"].iloc[i]
            if c > o:  # bullish candle → bearish OB
                obs.append(dict(type="BEARISH", top=c, bottom=o, mid=(c+o)/2,
                                date=df.index[i], idx=i, label="Bear OB"))
                break
    cp = df["Close"].iloc[-1]
    # Keep active OBs only
    obs = [ob for ob in obs if (ob["type"]=="BULLISH" and cp > ob["bottom"])
                             or (ob["type"]=="BEARISH" and cp < ob["top"])]
    obs.sort(key=lambda x: x["idx"], reverse=True)
    return obs[:6]


def fair_value_gaps(df):
    """3-candle imbalance: H[i-2] < L[i] (bull) or L[i-2] > H[i] (bear)"""
    fvgs = []; start = max(2, len(df)-80)
    cp = df["Close"].iloc[-1]
    for i in range(start, len(df)):
        h0, h2 = df["High"].iloc[i-2], df["High"].iloc[i]
        l0, l2 = df["Low"].iloc[i-2],  df["Low"].iloc[i]
        if h0 < l2 and cp > h0:       # Bullish FVG
            fvgs.append(dict(type="BULLISH", top=l2, bottom=h0, mid=(l2+h0)/2,
                             size=l2-h0, date=df.index[i-1], idx=i-1,
                             filled=df["Low"].iloc[-1]<l2))
        if l0 > h2 and cp < l0:       # Bearish FVG
            fvgs.append(dict(type="BEARISH", top=l0, bottom=h2, mid=(l0+h2)/2,
                             size=l0-h2, date=df.index[i-1], idx=i-1,
                             filled=df["High"].iloc[-1]>h2))
    fvgs.sort(key=lambda x: x["idx"], reverse=True)
    return fvgs[:8]


def premium_discount(df, sh, sl):
    if not sh or not sl: return "NEUTRAL", 0.5
    hi = max(x["price"] for x in sh[-3:]) if len(sh)>=3 else sh[-1]["price"]
    lo = min(x["price"] for x in sl[-3:]) if len(sl)>=3 else sl[-1]["price"]
    rng = hi - lo if hi != lo else 1
    pct = (df["Close"].iloc[-1] - lo) / rng
    zone = "PREMIUM" if pct > 0.618 else "DISCOUNT" if pct < 0.382 else "EQUILIBRIUM"
    return zone, pct


def generate_signal(trend, evts, obs, fvgs, zone, cp):
    confs, bull, bear = [], 0, 0
    # Trend
    if   trend == "BULLISH": bull += 2; confs.append(("bull","Bullish Market Structure  HH+HL ✓"))
    elif trend == "BEARISH": bear += 2; confs.append(("bear","Bearish Market Structure  LH+LL ✓"))
    else:                              confs.append(("nt",  "No Clear Structure  —  Ranging"))
    # Zone
    if   zone == "DISCOUNT":     bull += 1; confs.append(("bull","Price in Discount Zone  (<38.2%)"))
    elif zone == "PREMIUM":      bear += 1; confs.append(("bear","Price in Premium Zone  (>61.8%)"))
    else:                                   confs.append(("nt",  "Price at Equilibrium  (38-62%)"))
    # OBs
    bull_obs = [ob for ob in obs if ob["type"]=="BULLISH"]
    bear_obs = [ob for ob in obs if ob["type"]=="BEARISH"]
    if bull_obs:
        nb = min(bull_obs, key=lambda x: abs(cp - x["mid"]))
        d  = abs(cp - nb["mid"]) / cp * 100
        if d < 0.8:  bull += 2; confs.append(("bull", f"Price AT Bullish OB  ({d:.2f}% dist)"))
        elif d < 2:  bull += 1; confs.append(("bull", f"Near Bullish OB  ({d:.2f}% dist)"))
    if bear_obs:
        nb = min(bear_obs, key=lambda x: abs(cp - x["mid"]))
        d  = abs(cp - nb["mid"]) / cp * 100
        if d < 0.8:  bear += 2; confs.append(("bear", f"Price AT Bearish OB  ({d:.2f}% dist)"))
        elif d < 2:  bear += 1; confs.append(("bear", f"Near Bearish OB  ({d:.2f}% dist)"))
    # FVGs
    open_bull = [f for f in fvgs if f["type"]=="BULLISH" and not f["filled"]]
    open_bear = [f for f in fvgs if f["type"]=="BEARISH" and not f["filled"]]
    if open_bull:
        nf = min(open_bull, key=lambda x: abs(cp - x["mid"]))
        if nf["bottom"] <= cp <= nf["top"]*1.015:
            bull += 1; confs.append(("bull","Price inside Bullish FVG"))
    if open_bear:
        nf = min(open_bear, key=lambda x: abs(cp - x["mid"]))
        if nf["bottom"]*0.985 <= cp <= nf["top"]:
            bear += 1; confs.append(("bear","Price inside Bearish FVG"))
    # Structure events
    for ev in evts:
        if ev["type"] == "BOS"   and ev["dir"] == "UP":
            bull += 1; confs.append(("bull","Bullish BOS confirmed"))
        elif ev["type"] == "BOS" and ev["dir"] == "DOWN":
            bear += 1; confs.append(("bear","Bearish BOS confirmed"))
        elif ev["type"] == "CHoCH":
            confs.append(("nt","CHoCH — potential reversal signal"))

    net = bull - bear
    strength = min(5, max(1, (bull + bear) // 2 + 1))
    if   net >= 3: sig, clr = "STRONG BUY",  "bull"
    elif net >= 1: sig, clr = "BUY",          "bull"
    elif net <= -3:sig, clr = "STRONG SELL", "bear"
    elif net <= -1:sig, clr = "SELL",         "bear"
    else:          sig, clr = "WAIT",         "nt"
    return sig, clr, strength, confs


# ═══════════════════════════════════════════════════════════════
# ── CHART BUILDER ───────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════

def build_chart(df: pd.DataFrame, sh, sl, obs, fvgs, cp, tf_label, interval="1d"):
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        vertical_spacing=0.03, row_heights=[0.77, 0.23]
    )
    # Candlestick
    fig.add_trace(go.Candlestick(
        x=df.index, open=df["Open"], high=df["High"],
        low=df["Low"],  close=df["Close"], name="XAUUSD",
        increasing=dict(line=dict(color="#00ff88",width=1), fillcolor="rgba(0,255,136,0.75)"),
        decreasing=dict(line=dict(color="#ff4455",width=1), fillcolor="rgba(255,68,85,0.75)"),
    ), row=1, col=1)

    # EMAs
    for sp, col, nm in [(21,"#ffd700","EMA 21"),(50,"#6495ed","EMA 50"),(200,"#ff8c00","EMA 200")]:
        if len(df) > sp:
            fig.add_trace(go.Scatter(
                x=df.index, y=df["Close"].ewm(span=sp).mean(), name=nm,
                line=dict(color=col, width=1, dash="dot"), opacity=0.7
            ), row=1, col=1)

    # Extend date
    td = timedelta(days=4) if interval=="1d" else (timedelta(weeks=3) if interval=="1wk" else timedelta(days=90))
    end = df.index[-1] + td

    # Order Blocks
    for ob in obs:
        fc = "rgba(0,255,136,0.07)"  if ob["type"]=="BULLISH" else "rgba(255,68,85,0.07)"
        lc = "rgba(0,255,136,0.35)"  if ob["type"]=="BULLISH" else "rgba(255,68,85,0.35)"
        tc = "#00ff88"               if ob["type"]=="BULLISH" else "#ff4455"
        fig.add_shape(type="rect", x0=ob["date"], x1=end,
                      y0=ob["bottom"], y1=ob["top"],
                      fillcolor=fc, line=dict(color=lc,width=1,dash="dot"),
                      row=1, col=1)
        fig.add_annotation(x=end, y=ob["mid"],
                           text=f" {ob['label']}", showarrow=False,
                           font=dict(size=9,color=tc),
                           xanchor="left", yanchor="middle", row=1, col=1)

    # FVGs
    for fvg in fvgs[:5]:
        fc = "rgba(0,200,255,0.05)"   if fvg["type"]=="BULLISH" else "rgba(255,165,0,0.05)"
        lc = "rgba(0,200,255,0.18)"   if fvg["type"]=="BULLISH" else "rgba(255,165,0,0.18)"
        fig.add_shape(type="rect", x0=fvg["date"], x1=end,
                      y0=fvg["bottom"], y1=fvg["top"],
                      fillcolor=fc, line=dict(color=lc,width=0.5,dash="dash"),
                      row=1, col=1)

    # Swing markers
    if sh:
        fig.add_trace(go.Scatter(
            x=[s["date"] for s in sh], y=[s["price"] for s in sh],
            mode="markers+text", name="Swing High",
            marker=dict(symbol="triangle-down", size=9, color="#ff4455"),
            text=["SH"]*len(sh), textposition="top center",
            textfont=dict(size=8, color="#ff4455"), showlegend=False
        ), row=1, col=1)
    if sl:
        fig.add_trace(go.Scatter(
            x=[s["date"] for s in sl], y=[s["price"] for s in sl],
            mode="markers+text", name="Swing Low",
            marker=dict(symbol="triangle-up", size=9, color="#00ff88"),
            text=["SL"]*len(sl), textposition="bottom center",
            textfont=dict(size=8, color="#00ff88"), showlegend=False
        ), row=1, col=1)

    # Current price line
    fig.add_hline(y=cp, line=dict(color="#ffd700", width=1, dash="dot"),
                  annotation_text=f"  ${cp:,.2f}",
                  annotation_position="right",
                  annotation_font=dict(color="#ffd700", size=11),
                  row=1, col=1)

    # Volume
    vol_colors = ["rgba(0,255,136,0.45)" if c>=o else "rgba(255,68,85,0.45)"
                  for c,o in zip(df["Close"], df["Open"])]
    fig.add_trace(go.Bar(
        x=df.index, y=df["Volume"], name="Volume",
        marker_color=vol_colors, showlegend=False
    ), row=2, col=1)

    # Layout
    fig.update_layout(
        paper_bgcolor="#08080c", plot_bgcolor="#09080a",
        font=dict(family="DM Sans", color="#c0a860", size=11),
        xaxis_rangeslider_visible=False,
        height=620,
        margin=dict(l=10, r=110, t=40, b=10),
        legend=dict(bgcolor="rgba(14,12,9,0.85)",
                    bordercolor="rgba(255,215,0,0.12)", borderwidth=1,
                    font=dict(size=10), x=0.01, y=0.99),
        title=dict(text=f"<b>XAUUSD  ·  {tf_label}</b>  —  SMC Chart",
                   font=dict(color="#ffd700", size=14), x=0.01, y=0.98)
    )
    axis_style = dict(gridcolor="rgba(255,215,0,0.04)",
                      zerolinecolor="rgba(255,215,0,0.08)",
                      tickfont=dict(color="#887a5a"),
                      linecolor="rgba(255,215,0,0.06)")
    fig.update_xaxes(**axis_style)
    fig.update_yaxes(**axis_style)
    fig.update_yaxes(tickprefix="$", row=1, col=1)
    return fig


# ═══════════════════════════════════════════════════════════════
# ── HELPERS ─────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════

def calc_gold(usd, mmk):
    g   = usd / TROY_OZ
    gm  = g * mmk
    pael= gm * PAEL_G
    kyat= pael * 100
    return dict(gram_usd=g, gram_mmk=gm, pael=pael, kyat=kyat)

fks  = lambda n: f"{int(n):,} Ks"
fusd = lambda n: f"${n:,.2f}"

def tbadge(t):
    m = {"BULLISH": ('<span style="color:#00ff88;background:rgba(0,255,136,0.09);'
                     'border:1px solid rgba(0,255,136,0.25);padding:4px 14px;'
                     'border-radius:8px;font-weight:800;font-size:13px">▲ BULLISH</span>'),
         "BEARISH": ('<span style="color:#ff4455;background:rgba(255,68,85,0.09);'
                     'border:1px solid rgba(255,68,85,0.25);padding:4px 14px;'
                     'border-radius:8px;font-weight:800;font-size:13px">▼ BEARISH</span>'),
         "RANGING": ('<span style="color:#ffaa00;background:rgba(255,170,0,0.09);'
                     'border:1px solid rgba(255,170,0,0.25);padding:4px 14px;'
                     'border-radius:8px;font-weight:800;font-size:13px">◆ RANGING</span>')}
    return m.get(t, m["RANGING"])

SIG_MM  = {"STRONG BUY":"💪 အင်မတန် ဝယ်ယူ", "BUY":"🟢 ဝယ်ယူ",
           "WAIT":"⏳ စောင့်ကြည့်", "SELL":"🔴 ရောင်းချ",
           "STRONG SELL":"💨 အင်မတန် ရောင်းချ"}
TRD_MM  = {"BULLISH":"📈 ဈေးတက် ဦးတည်ချက်","BEARISH":"📉 ဈေးကျ ဦးတည်ချက်",
           "RANGING":"↔️ ဈေးညီ / ဦးတည်ချက်မရှိ"}
ZONE_MM = {"DISCOUNT":"💚 လျော့ဈေးဇုန် — ဝယ်ယူသင့်သောနေရာ",
           "PREMIUM":"🔴 ဈေးကြီးဇုန် — ရောင်းသင့်သောနေရာ",
           "EQUILIBRIUM":"🟡 ညှိနှုန်းဇုန် (50% ဒေသ)","NEUTRAL":"⚪ ဒေသမဆုံးဖြတ်နိုင်"}
STARS   = lambda n: "⭐"*n + "☆"*(5-n)

CLR = {"bull":("#00ff88","rgba(0,255,136,0.08)","rgba(0,255,136,0.22)"),
       "bear":("#ff4455","rgba(255,68,85,0.08)","rgba(255,68,85,0.22)"),
       "nt":  ("#ffaa00","rgba(255,170,0,0.08)","rgba(255,170,0,0.22)")}

def conf_html(confs):
    html = ""
    for t, txt in confs:
        c,bg,bo = CLR.get(t, CLR["nt"])
        html += (f'<div style="background:{bg};border:1px solid {bo};border-radius:6px;'
                 f'padding:6px 10px;margin-bottom:5px;font-size:11px;color:{c}">{txt}</div>')
    return html


# ═══════════════════════════════════════════════════════════════
# ── SMC ANALYSIS BLOCK (reusable) ───────────────────────────────
# ═══════════════════════════════════════════════════════════════

def run_smc(df, lb):
    """Returns full SMC dict for given df + lookback"""
    sh, sl  = find_pivots(df, left=lb, right=lb)
    trend, evts = market_structure(df, sh, sl)
    obs     = order_blocks(df, sh, sl, n=4)
    fvgs    = fair_value_gaps(df)
    zone, zpct = premium_discount(df, sh, sl)
    cp      = df["Close"].iloc[-1]
    sig, clr, str_, confs = generate_signal(trend, evts, obs, fvgs, zone, cp)

    # Key levels
    b_ob_btm = [ob["bottom"] for ob in obs if ob["type"]=="BULLISH"]
    b_ob_top = [ob["top"]    for ob in obs if ob["type"]=="BEARISH"]
    stop   = min(b_ob_btm) if b_ob_btm else cp*0.990
    target = (min(b_ob_top) if b_ob_top and sig in ["BUY","STRONG BUY"]
              else max(b_ob_btm) if b_ob_btm and sig in ["SELL","STRONG SELL"]
              else (cp*1.02 if clr=="bull" else cp*0.98))
    rr = abs(target-cp)/abs(cp-stop) if abs(cp-stop)>0 else 0

    return dict(sh=sh, sl=sl, obs=obs, fvgs=fvgs, trend=trend, evts=evts,
                zone=zone, zpct=zpct, cp=cp,
                sig=sig, clr=clr, str_=str_, confs=confs,
                stop=stop, target=target, rr=rr)


# ═══════════════════════════════════════════════════════════════
# ── MAIN APP ────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════

def main():

    # ── HEADER ──
    st.markdown("""
    <div style="text-align:center;padding:22px 0 6px;position:relative">
      <div style="font-family:'Palatino Linotype',serif;font-size:56px;line-height:1;
          background:linear-gradient(135deg,#fff5b8 0%,#ffd700 45%,#e8a800 70%,#ffe066 100%);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent;
          filter:drop-shadow(0 0 22px rgba(255,215,0,0.28))">Au</div>
      <div style="font-size:12px;font-weight:800;color:#ffd700;letter-spacing:5px;
          margin-top:5px;text-transform:uppercase;
          text-shadow:0 0 14px rgba(255,215,0,0.35)">မြန်မာ ရွှေဈေးနှုန်း PRO</div>
      <div style="font-size:9px;color:#605848;letter-spacing:2.5px;margin-top:4px">
          SMART MONEY CONCEPTS  ·  LIVE ANALYSIS  ·  MYANMAR GOLD</div>
    </div>
    """, unsafe_allow_html=True)

    # ── FETCH DATA ──
    with st.spinner(""):
        live = fetch_live()
        cbm  = fetch_cbm()

    # ── TOP STRIP ──
    if live:
        is_up = live["pct"] >= 0
        arrow = "▲" if is_up else "▼"
        cc    = "#00ff88" if is_up else "#ff4455"
        dot   = f'<span style="background:#00ff88;width:8px;height:8px;border-radius:50%;' \
                f'display:inline-block;margin-right:6px;box-shadow:0 0 8px #00ff88"></span>'
        st.markdown(f"""
        <div style="background:rgba(255,215,0,0.03);border:1px solid rgba(255,215,0,0.09);
             border-radius:12px;padding:10px 18px;margin-bottom:16px;
             display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px">
          <div>
            <div style="font-size:9px;color:#887a5a;font-weight:700;letter-spacing:1.5px">
              {dot}XAUUSDT LIVE · {live['src']}</div>
            <div style="font-size:32px;font-weight:800;
                background:linear-gradient(135deg,#fff5b8,#ffd700);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent">
              ${live['price']:,.2f}</div>
            <div style="font-size:13px;color:{cc};font-weight:700">
              {arrow} {abs(live['pct']):.2f}%
              ({'+' if is_up else ''}{live['change']:,.2f})</div>
          </div>
          <div style="display:flex;gap:24px;flex-wrap:wrap">
            <div><div style="font-size:9px;color:#887a5a;letter-spacing:1px">24H HIGH</div>
              <div style="font-size:18px;font-weight:700;color:#ffd700">${live['high']:,.2f}</div></div>
            <div><div style="font-size:9px;color:#887a5a;letter-spacing:1px">24H LOW</div>
              <div style="font-size:18px;font-weight:700;color:#ffd700">${live['low']:,.2f}</div></div>
            <div><div style="font-size:9px;color:#887a5a;letter-spacing:1px">CBM RATE</div>
              <div style="font-size:18px;font-weight:700;color:#00dd77">{cbm['rate']:,.0f} Ks</div></div>
            <div><div style="font-size:9px;color:#887a5a;letter-spacing:1px">UPDATED</div>
              <div style="font-size:13px;font-weight:700;color:#887a5a">
              {datetime.now().strftime('%H:%M:%S')}</div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("⚠️ Live price ရှာမရ — Internet ချိတ်ဆက်မှု စစ်ဆေးပါ")

    # ── TABS ──
    t1, t2, t3 = st.tabs(["📊  Dashboard", "📈  Gold Chart", "🎯  SMC Analysis"])

    # ══════════════════════════════════════════════════════════
    # TAB 1 · DASHBOARD
    # ══════════════════════════════════════════════════════════
    with t1:
        if not live:
            st.error("Data မရှိ"); return

        p = live["price"]

        col_l, col_r = st.columns([1, 1.4])

        with col_l:
            st.markdown('<div class="cl">💵 USD → MMK လဲလှယ်နှုန်း</div>', unsafe_allow_html=True)
            mkt = st.number_input("🏪 Market Rate (Ks)", value=float(cbm["rate"]),
                                  step=10.0, format="%.0f",
                                  help="ဈေးကွက် လဲနှုန်းကို ကိုယ်တိုင်ထည့်ပါ")
            st.markdown(f"""
            <div style="display:flex;gap:8px;margin-top:6px;font-size:11px">
              <div style="background:rgba(0,221,119,0.06);border:1px solid rgba(0,221,119,0.15);
                   border-radius:6px;padding:5px 10px;color:#00dd77">
                🏦 CBM: <b>{cbm['rate']:,.0f} Ks</b></div>
              <div style="background:rgba(255,215,0,0.05);border:1px solid rgba(255,215,0,0.1);
                   border-radius:6px;padding:5px 10px;color:#c0a860">
                📡 {cbm['src']}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_r:
            st.markdown('<div class="cl">📐 တွက်ချက်နည်း Formula</div>', unsafe_allow_html=True)
            st.markdown("""
            <div style="font-family:'Courier New',monospace;font-size:12px;color:#d4c090;
                line-height:2.2;background:rgba(0,0,0,.32);border:1px solid rgba(255,215,0,0.06);
                border-radius:10px;padding:12px 16px;font-weight:600">
              ပဲသား &nbsp;= (XAUUSDT × MMK × 16.6) ÷ 31.1035<br>
              ကျပ်သား = ပဲသား × 100<br>
              1 gram&nbsp; = XAUUSDT ÷ 31.1035
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div style="margin-top:18px" class="cl">🇲🇲 မြန်မာ့ ရွှေဈေး တွက်ချက်မှု</div>', unsafe_allow_html=True)

        mc  = calc_gold(p, mkt)
        cc2 = calc_gold(p, cbm["rate"])

        a, b, c_, d = st.columns(4)
        with a:
            st.markdown(f"""<div class="gc gc-hl">
              <div class="cl">တစ်ကျပ်သား · Market Rate</div>
              <div class="pb">{fks(mc['kyat'])}</div>
              <div style="font-size:10px;color:#887a5a;margin-top:4px">
              ≈ {fusd(p * PAEL_G * 100 / TROY_OZ)}</div></div>""", unsafe_allow_html=True)
        with b:
            st.markdown(f"""<div class="gc">
              <div class="cl">တစ်ကျပ်သား · CBM Rate</div>
              <div style="font-size:24px;font-weight:800;color:#00dd77">{fks(cc2['kyat'])}</div>
              </div>""", unsafe_allow_html=True)
        with c_:
            st.markdown(f"""<div class="gc">
              <div class="cl">တစ်ပဲသား (16.6g)</div>
              <div style="font-size:22px;font-weight:800;color:#ffd700">{fks(mc['pael'])}</div>
              </div>""", unsafe_allow_html=True)
        with d:
            st.markdown(f"""<div class="gc">
              <div class="cl">1 Gram</div>
              <div style="font-size:15px;font-weight:700;color:#c0a860">
              USD <b style="color:#ffd700">{fusd(mc['gram_usd'])}</b></div>
              <div style="font-size:15px;font-weight:700;color:#c0a860;margin-top:4px">
              MMK <b style="color:#ffd700">{fks(mc['gram_mmk'])}</b></div>
              </div>""", unsafe_allow_html=True)

        # Compare table
        st.markdown("---")
        st.markdown('<div class="cl">⚖️ CBM Rate vs Market Rate နှိုင်းယှဉ်</div>', unsafe_allow_html=True)
        diff = mc["kyat"] - cc2["kyat"]
        st.markdown(f"""
        <div style="display:flex;gap:10px;flex-wrap:wrap">
          <div class="gc" style="flex:1;min-width:200px">
            <div style="font-size:10px;color:#887a5a">Market Rate Kyat</div>
            <div style="font-size:20px;font-weight:800;color:#ffd700">{fks(mc['kyat'])}</div>
          </div>
          <div class="gc" style="flex:1;min-width:200px">
            <div style="font-size:10px;color:#887a5a">CBM Rate Kyat</div>
            <div style="font-size:20px;font-weight:800;color:#00dd77">{fks(cc2['kyat'])}</div>
          </div>
          <div class="gc" style="flex:1;min-width:200px">
            <div style="font-size:10px;color:#887a5a">ကွာဟချက်</div>
            <div style="font-size:20px;font-weight:800;color:{'#ff6666' if diff>0 else '#00ff88'}">
              {'+' if diff>=0 else ''}{fks(diff)}</div>
            <div style="font-size:10px;color:#887a5a">Market {'above' if diff>0 else 'below'} CBM</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="text-align:center;font-size:10px;color:#504838;margin-top:18px;line-height:2">
          ⚠️ ခန့်မှန်းတွက်ချက်ဈေးသာ ဖြစ်ပါသည် — ဆိုင်ပေါက်ဈေးနှင့် ကွဲလွဲနိုင်သည်<br>
          📡 Gold Futures (GC=F) · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # TAB 2 · CHART
    # ══════════════════════════════════════════════════════════
    with t2:
        cc1, cc2_, cc3 = st.columns([2, 3, 1])
        with cc1:
            tf = st.selectbox("Timeframe", ["Daily (3M)","Weekly (1Y)","Monthly (3Y)"],
                              key="chart_tf")
        with cc3:
            if st.button("↻ Refresh", key="chart_ref"):
                st.cache_data.clear()

        TF = {"Daily (3M)":   ("3mo","1d", 5,"Daily"),
              "Weekly (1Y)":  ("1y", "1wk",3,"Weekly"),
              "Monthly (3Y)": ("3y", "1mo",2,"Monthly")}
        period, interval, lb, tflabel = TF[tf]

        with st.spinner("📊 Chart data ရယူနေသည်..."):
            df = fetch_ohlcv(period, interval)

        if df.empty:
            st.error("⚠️ yfinance data ရှာမရ — ပြန်ကြိုးစားပါ")
        else:
            A = run_smc(df, lb)
            fig = build_chart(df, A["sh"], A["sl"], A["obs"], A["fvgs"],
                              A["cp"], tflabel, interval)
            st.plotly_chart(fig, use_container_width=True,
                            config={"displayModeBar": True, "scrollZoom": True})

            # Stats row
            r = df.iloc[-1]; prev = df.iloc[-2] if len(df)>1 else r
            ch = (r["Close"]-prev["Close"])/prev["Close"]*100
            cols = st.columns(6)
            for col_, lbl, val in zip(cols,
                    ["Open","High","Low","Close","Change%","Volume"],
                    [f"${r['Open']:,.2f}",f"${r['High']:,.2f}",f"${r['Low']:,.2f}",
                     f"${r['Close']:,.2f}",f"{ch:+.2f}%",f"{r['Volume']:,.0f}"]):
                col_.metric(lbl, val)

    # ══════════════════════════════════════════════════════════
    # TAB 3 · SMC ANALYSIS
    # ══════════════════════════════════════════════════════════
    with t3:
        st.markdown("""
        <div style="font-size:11px;color:#887a5a;padding:10px 14px;
            background:rgba(255,215,0,0.025);border-radius:8px;
            border:1px solid rgba(255,215,0,0.06);margin-bottom:18px">
          ⚠️ <b style="color:#c0a860">Disclaimer:</b>  SMC Analysis သည် Technical Analysis ကိုသာ
          အခြေခံသည်။ ရင်းနှီးမြှုပ်နှံမှု အကြံပေးချက် <b>မဟုတ်ပါ</b>။
          ကိုယ်တိုင် Due Diligence ပြုလုပ်ပါ။
        </div>""", unsafe_allow_html=True)

        smc_tf = st.radio("📅 Timeframe ရွေးချယ်ပါ",
                          ["Daily  (တနေ့)", "Weekly  (တပတ်)", "Monthly  (တလ)"],
                          horizontal=True)
        SMC_TF = {"Daily  (တနေ့)":  ("3mo","1d", 5,"Daily"),
                  "Weekly  (တပတ်)": ("1y", "1wk",3,"Weekly"),
                  "Monthly  (တလ)":  ("3y", "1mo",2,"Monthly")}
        sp, si, slb, slbl = SMC_TF[smc_tf]

        with st.spinner("🧠 SMC ခွဲခြမ်းစိတ်ဖြာနေသည်..."):
            df_s = fetch_ohlcv(sp, si)

        if df_s.empty:
            st.error("Data ရှာမရ — ပြန်ကြိုးစားပါ"); return

        A = run_smc(df_s, slb)
        sig_c = CLR.get(A["clr"], CLR["nt"])

        # ── SIGNAL BOX ──
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,rgba(255,215,0,0.04),rgba(0,0,0,0));
             border:1px solid rgba(255,215,0,0.16);border-radius:18px;
             padding:24px;text-align:center;margin-bottom:20px">
          <div style="font-size:9px;color:#887a5a;letter-spacing:2.5px;margin-bottom:8px">
            {slbl.upper()} SMC SIGNAL  ·  XAUUSD</div>
          <div style="font-size:38px;font-weight:800;color:{sig_c[0]}">
            {SIG_MM.get(A['sig'], A['sig'])}</div>
          <div style="font-size:20px;margin-top:8px">{STARS(A['str_'])}</div>
          <div style="margin-top:14px">{tbadge(A['trend'])}</div>
          <div style="font-size:12px;color:#c0a860;margin-top:10px">
            {TRD_MM.get(A['trend'],'')}</div>
          <div style="font-size:12px;color:#887a5a;margin-top:6px">
            Current Price  <b style="color:#ffd700">${A['cp']:,.2f}</b></div>
        </div>
        """, unsafe_allow_html=True)

        # ── 3 COLUMNS ──
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f"""
            <div class="gc">
              <div class="cl">📍 Price Zone</div>
              <div style="font-size:13px;font-weight:700;margin-bottom:10px">
                {ZONE_MM.get(A['zone'],'')}</div>
              <div style="background:rgba(0,0,0,.3);border-radius:6px;height:8px;
                   border:1px solid rgba(255,215,0,0.08);overflow:hidden">
                <div style="height:100%;width:{A['zpct']*100:.1f}%;
                     background:linear-gradient(90deg,#00ff88,#ffd700);
                     border-radius:6px"></div>
              </div>
              <div style="display:flex;justify-content:space-between;
                   font-size:9px;color:#504838;margin-top:4px">
                <span>Discount 0%</span><span>50%</span><span>100% Premium</span></div>
              <div style="margin-top:12px">
                <div style="font-size:10px;color:#887a5a">Position</div>
                <div style="font-size:22px;font-weight:800;color:#ffd700">
                  {A['zpct']*100:.1f}%</div></div>
            </div>""", unsafe_allow_html=True)

        with c2:
            rr_c = "#00ff88" if A["rr"] >= 2 else "#ffaa00" if A["rr"] >= 1 else "#ff4455"
            st.markdown(f"""
            <div class="gc">
              <div class="cl">🎯 Key Levels</div>
              <div style="margin-bottom:10px">
                <div style="font-size:9px;color:#00ff88;letter-spacing:1px;
                     text-transform:uppercase">🎯 Target</div>
                <div style="font-size:22px;font-weight:800;color:#00ff88">
                  ${A['target']:,.2f}</div>
                <div style="font-size:10px;color:#887a5a">
                  {((A['target']-A['cp'])/A['cp']*100):+.2f}% from current</div>
              </div>
              <div style="margin-bottom:12px">
                <div style="font-size:9px;color:#ff4455;letter-spacing:1px;
                     text-transform:uppercase">🛡️ Stop Loss</div>
                <div style="font-size:22px;font-weight:800;color:#ff4455">
                  ${A['stop']:,.2f}</div>
                <div style="font-size:10px;color:#887a5a">
                  {((A['stop']-A['cp'])/A['cp']*100):+.2f}% from current</div>
              </div>
              <div style="background:rgba(255,215,0,0.04);border-radius:8px;
                   padding:8px 12px;border:1px solid rgba(255,215,0,0.1)">
                <div style="font-size:9px;color:#c0a860">Risk : Reward</div>
                <div style="font-size:20px;font-weight:800;color:{rr_c}">
                  1 : {A['rr']:.2f}</div>
              </div>
            </div>""", unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="gc">
              <div class="cl">🔗 Confluences ({len(A['confs'])})</div>
              {conf_html(A['confs'])}
            </div>""", unsafe_allow_html=True)

        # ── ORDER BLOCKS ──
        st.markdown("---")
        st.markdown('<div class="cl" style="margin-bottom:12px">📦 Active Order Blocks</div>',
                    unsafe_allow_html=True)
        if A["obs"]:
            ob_c = st.columns(min(len(A["obs"]), 3))
            for i, ob in enumerate(A["obs"][:3]):
                is_bull = ob["type"]=="BULLISH"
                dist = (A["cp"] - ob["mid"]) / ob["mid"] * 100
                bc = "rgba(0,255,136,0.18)" if is_bull else "rgba(255,68,85,0.18)"
                tc2= "#00ff88" if is_bull else "#ff4455"
                with ob_c[i]:
                    st.markdown(f"""
                    <div class="gc" style="border-color:{'rgba(0,255,136,0.2)' if is_bull else 'rgba(255,68,85,0.2)'}">
                      <div style="font-size:10px;font-weight:700;color:{tc2};margin-bottom:6px">
                        {'● BULLISH OB' if is_bull else '● BEARISH OB'}</div>
                      <div style="font-size:11px;color:#c0a860">
                        Top <b style="color:#ffd700">${ob['top']:,.2f}</b></div>
                      <div style="font-size:11px;color:#c0a860">
                        Mid <b style="color:#ffd700">${ob['mid']:,.2f}</b></div>
                      <div style="font-size:11px;color:#c0a860">
                        Bot <b style="color:#ffd700">${ob['bottom']:,.2f}</b></div>
                      <div style="margin-top:6px;background:{bc};border-radius:4px;
                           padding:4px 8px;font-size:10px;font-weight:700;color:{tc2}">
                        Distance {dist:+.2f}%</div>
                      <div style="font-size:9px;color:#504838;margin-top:4px">
                        {ob['date'].strftime('%Y-%m-%d')}</div>
                    </div>""", unsafe_allow_html=True)
        else:
            st.info("Active Order Blocks မတွေ့ပါ")

        # ── FVGs ──
        st.markdown('<div class="cl" style="margin-bottom:12px;margin-top:6px">⚡ Open Fair Value Gaps</div>',
                    unsafe_allow_html=True)
        open_fvgs = [f for f in A["fvgs"] if not f["filled"]]
        if open_fvgs:
            fvg_c = st.columns(min(len(open_fvgs), 4))
            for i, fvg in enumerate(open_fvgs[:4]):
                is_bull = fvg["type"]=="BULLISH"
                tc3 = "#00c8ff" if is_bull else "#ffa500"
                dist = (A["cp"] - fvg["mid"]) / fvg["mid"] * 100
                with fvg_c[i]:
                    st.markdown(f"""
                    <div class="gc" style="border-color:{'rgba(0,200,255,0.15)' if is_bull else 'rgba(255,165,0,0.15)'}">
                      <div style="font-size:10px;font-weight:700;color:{tc3};margin-bottom:4px">
                        {'⬆ Bull FVG' if is_bull else '⬇ Bear FVG'}</div>
                      <div style="font-size:11px;color:#c0a860">
                        Size <b style="color:#ffd700">${fvg['size']:,.2f}</b></div>
                      <div style="font-size:11px;color:#c0a860">
                        Mid  <b style="color:#ffd700">${fvg['mid']:,.2f}</b></div>
                      <div style="font-size:10px;color:#887a5a;margin-top:4px">
                        Dist {dist:+.2f}%</div>
                      <div style="font-size:9px;color:#504838">
                        {fvg['date'].strftime('%Y-%m-%d')}</div>
                    </div>""", unsafe_allow_html=True)
        else:
            st.info("Open FVGs မတွေ့ပါ")

        # ── STRUCTURE EVENTS ──
        if A["evts"]:
            st.markdown('<div class="cl" style="margin-bottom:8px;margin-top:6px">🏗️ Structure Events</div>',
                        unsafe_allow_html=True)
            for ev in A["evts"]:
                is_up = ev["dir"]=="UP"
                bc = "rgba(0,255,136,0.05)" if is_up else "rgba(255,68,85,0.05)"
                bo = "rgba(0,255,136,0.15)" if is_up else "rgba(255,68,85,0.15)"
                tc4= "#00ff88" if is_up else "#ff4455"
                st.markdown(f"""
                <div style="background:{bc};border:1px solid {bo};border-radius:8px;
                     padding:8px 14px;margin-bottom:6px;font-size:12px">
                  <b style="color:{tc4}">{ev['label']}</b>
                  <span style="color:#887a5a;margin-left:12px">
                    Level: <b style="color:#ffd700">${ev['level']:,.2f}</b></span>
                </div>""", unsafe_allow_html=True)

        # ── BURMESE SUMMARY ──
        st.markdown("---")
        sig_c2 = CLR.get(A["clr"], CLR["nt"])
        st.markdown(f"""
        <div class="gc gc-hl" style="margin-top:4px">
          <div class="cl">🇲🇲 ခွဲခြမ်းစိတ်ဖြာချက် — {slbl} Timeframe</div>
          <div style="font-size:13px;line-height:2.3;color:#c0a860">
            <div>📅 Timeframe: <b style="color:#ffd700">{slbl}</b></div>
            <div>📍 ဈေးနှုန်း Trend: <b style="color:#ffd700">{TRD_MM.get(A['trend'],'')}</b></div>
            <div>💹 ဈေးနေရာ: <b style="color:#ffd700">{ZONE_MM.get(A['zone'],'')}</b></div>
            <div>🎯 Signal: <b style="color:{sig_c2[0]}">{SIG_MM.get(A['sig'],'')}  {STARS(A['str_'])}</b></div>
            <div>💰 Current Price: <b style="color:#ffd700">${A['cp']:,.2f}</b></div>
            <div>🎯 Target Level: <b style="color:#00ff88">${A['target']:,.2f}
              ({((A['target']-A['cp'])/A['cp']*100):+.2f}%)</b></div>
            <div>🛡️ Stop Loss: <b style="color:#ff4455">${A['stop']:,.2f}
              ({((A['stop']-A['cp'])/A['cp']*100):+.2f}%)</b></div>
            <div>⚖️ Risk : Reward = <b style="color:#ffd700">1 : {A['rr']:.2f}</b></div>
          </div>
          <div style="margin-top:14px;padding:12px 14px;
               background:rgba(255,170,0,0.04);border-radius:8px;
               border:1px solid rgba(255,170,0,0.1);
               font-size:11px;color:#887a5a;line-height:1.7">
            ⚠️ ဤ SMC Analysis သည် Historical Price Action ကိုသာ အခြေခံသည်။
            Gold market သည် Geopolitical events, Fed policy, Dollar index ဆိုသည့်
            အချက်များကြောင့် Technical level များကို ကျော်ဝင်နိုင်သည်။
            ရင်းနှီးမြှုပ်နှံမှုဆုံးဖြတ်ချက်ချရာတွင် ကိုယ်တိုင်စီစစ်ပြီး တာဝန်ယူပါ။<br>
            <b style="color:#c0a860">Past performance does not guarantee future results.</b>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── QUICK MULTI-TF SUMMARY ──
        st.markdown("---")
        st.markdown('<div class="cl" style="margin-bottom:14px">📊 Multi-Timeframe Quick Summary</div>',
                    unsafe_allow_html=True)

        mt_cols = st.columns(3)
        MT = [("Daily","3mo","1d",5),("Weekly","1y","1wk",3),("Monthly","3y","1mo",2)]
        for col, (lbl, per, iv, lb2) in zip(mt_cols, MT):
            with col:
                with st.spinner(f""):
                    df_mt = fetch_ohlcv(per, iv)
                if not df_mt.empty:
                    Am = run_smc(df_mt, lb2)
                    sc = CLR.get(Am["clr"], CLR["nt"])
                    st.markdown(f"""
                    <div class="gc" style="text-align:center;border-color:{sc[2]}">
                      <div style="font-size:10px;color:#887a5a;letter-spacing:1.5px;
                           margin-bottom:8px">{lbl.upper()}</div>
                      <div style="font-size:20px;font-weight:800;color:{sc[0]}">
                        {SIG_MM.get(Am['sig'],Am['sig'])}</div>
                      <div style="font-size:14px;margin:4px 0">{STARS(Am['str_'])}</div>
                      <div style="margin-top:6px">{tbadge(Am['trend'])}</div>
                      <div style="font-size:10px;color:#887a5a;margin-top:8px">
                        Zone: <b style="color:#c0a860">{Am['zone']}</b></div>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div class="gc" style="text-align:center">
                      <div class="cl">{lbl}</div>
                      <div style="color:#504838">Data N/A</div></div>""",
                      unsafe_allow_html=True)


if __name__ == "__main__":
    main()
