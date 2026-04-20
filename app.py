import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pytz

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="မြန်မာ ရွှေဈေး ခွဲခြမ်းစိတ်ဖြာမှု",
    page_icon="🥇",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  DARK THEME CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Myanmar:wght@400;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', 'Noto Sans Myanmar', sans-serif;
    background-color: #0D0F14;
    color: #E8ECF0;
}
.main { background-color: #0D0F14; }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #13161E 0%, #0D0F14 100%);
    border-right: 1px solid #1E2330;
}
section[data-testid="stSidebar"] * { color: #C8CDD8 !important; }

/* Metric Cards */
.metric-card {
    background: linear-gradient(135deg, #161B27 0%, #1A2035 100%);
    border: 1px solid #252D42;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 12px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    transition: transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
}
.metric-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #6B7A99;
    margin-bottom: 6px;
}
.metric-value {
    font-size: 28px;
    font-weight: 700;
    color: #F0C040;
    line-height: 1.2;
}
.metric-sub {
    font-size: 12px;
    color: #4CAF50;
    margin-top: 4px;
}
.metric-sub.negative { color: #F44336; }
.metric-sub.neutral  { color: #9E9E9E; }

/* Gold Price Hero Card */
.hero-card {
    background: linear-gradient(135deg, #1A1400 0%, #2A2000 50%, #1A1400 100%);
    border: 1px solid #F0C04040;
    border-radius: 18px;
    padding: 28px 32px;
    margin-bottom: 20px;
    box-shadow: 0 0 60px rgba(240,192,64,0.08), 0 4px 32px rgba(0,0,0,0.5);
    position: relative;
    overflow: hidden;
}
.hero-card::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(240,192,64,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.hero-label {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #F0C04099;
    margin-bottom: 8px;
}
.hero-value {
    font-size: 42px;
    font-weight: 700;
    color: #F0C040;
    line-height: 1;
    margin-bottom: 4px;
}
.hero-unit {
    font-size: 16px;
    color: #F0C04080;
    margin-left: 6px;
}

/* SMC Section */
.smc-card {
    background: #13161E;
    border: 1px solid #1E2330;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
}
.smc-header {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid #1E2330;
}
.smc-header.bullish { color: #26A69A; border-color: #26A69A30; }
.smc-header.bearish { color: #EF5350; border-color: #EF535030; }
.smc-header.neutral { color: #FFA726; border-color: #FFA72630; }
.smc-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 8px;
    font-size: 13.5px;
    color: #A8B0C0;
    line-height: 1.6;
}
.smc-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    margin-top: 7px;
    flex-shrink: 0;
}
.smc-dot.bullish { background: #26A69A; }
.smc-dot.bearish { background: #EF5350; }
.smc-dot.neutral { background: #FFA726; }

/* Badge */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
}
.badge-bullish { background: #26A69A20; color: #26A69A; border: 1px solid #26A69A40; }
.badge-bearish { background: #EF535020; color: #EF5350; border: 1px solid #EF535040; }
.badge-neutral  { background: #FFA72620; color: #FFA726; border: 1px solid #FFA72640; }

/* Divider */
.section-title {
    font-size: 15px;
    font-weight: 600;
    color: #8892AA;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin: 28px 0 14px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1E2330;
}

/* Streamlit overrides */
div[data-testid="stMetric"] {
    background: #161B27;
    border: 1px solid #252D42;
    border-radius: 12px;
    padding: 16px;
}
div[data-testid="stMetricValue"] { color: #F0C040 !important; }
div[data-testid="stMetricLabel"] { color: #6B7A99 !important; }
.stRadio > label { color: #C8CDD8 !important; }
.stNumberInput > label { color: #C8CDD8 !important; font-size: 13px !important; }
.stButton > button {
    background: linear-gradient(135deg, #F0C040, #E0A020);
    color: #0D0F14;
    border: none;
    border-radius: 8px;
    font-weight: 700;
    width: 100%;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #FFD060, #F0B030);
    color: #0D0F14;
}
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────
@st.cache_data(ttl=300)
def fetch_gold_data():
    """Fetch live + historical gold data from Yahoo Finance."""
    ticker = yf.Ticker("GC=F")
    hist   = ticker.history(period="6mo", interval="1d")
    info   = ticker.fast_info
    return hist, info


def calc_myanmar_gold(gold_usd: float, usd_rate: float) -> float:
    """((Gold_Price * 1.029) * USD_Rate) / 0.576"""
    return ((gold_usd * 1.029) * usd_rate) / 0.576


def format_mmk(value: float) -> str:
    return f"{value:,.0f} ကျပ်"


def price_change_class(change: float) -> str:
    if change > 0:  return "positive"
    if change < 0:  return "negative"
    return "neutral"


def smc_analysis(hist: pd.DataFrame):
    """Derive basic SMC signals from OHLC data."""
    if hist is None or len(hist) < 30:
        return {}

    close  = hist["Close"]
    high   = hist["High"]
    low    = hist["Low"]
    volume = hist["Volume"]

    # Daily (last 5 bars)
    d_close = close.iloc[-1]
    d_prev  = close.iloc[-2]
    d_high5 = high.iloc[-5:].max()
    d_low5  = low.iloc[-5:].min()
    d_vol_avg = volume.iloc[-10:].mean()
    d_vol_now = volume.iloc[-1]

    # Weekly (last 20 bars ~4 weeks)
    w_close = close.iloc[-1]
    w_open  = close.iloc[-20]
    w_high  = high.iloc[-20:].max()
    w_low   = low.iloc[-20:].min()
    w_ema20 = close.iloc[-20:].mean()

    # Monthly (last 60 bars ~3 months)
    m_close = close.iloc[-1]
    m_open  = close.iloc[-60] if len(close) >= 60 else close.iloc[0]
    m_high  = high.iloc[-60:].max() if len(high) >= 60 else high.max()
    m_low   = low.iloc[-60:].min()  if len(low)  >= 60 else low.min()
    m_trend = "Bullish" if m_close > m_open else "Bearish"

    # EMA signals
    ema9  = close.ewm(span=9,  adjust=False).mean().iloc[-1]
    ema21 = close.ewm(span=21, adjust=False).mean().iloc[-1]
    ema50 = close.ewm(span=50, adjust=False).mean().iloc[-1]

    daily_bias   = "Bullish" if d_close > d_prev  else "Bearish"
    weekly_bias  = "Bullish" if w_close > w_ema20 else "Bearish"
    monthly_bias = m_trend

    return {
        "daily": {
            "bias": daily_bias,
            "current": d_close,
            "high5": d_high5,
            "low5": d_low5,
            "vol_high": d_vol_now > d_vol_avg,
            "ema9": ema9,
            "ema21": ema21,
        },
        "weekly": {
            "bias": weekly_bias,
            "current": w_close,
            "high": w_high,
            "low": w_low,
            "ema20": w_ema20,
        },
        "monthly": {
            "bias": monthly_bias,
            "current": m_close,
            "high": m_high,
            "low": m_low,
            "open": m_open,
            "ema50": ema50,
        },
    }


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding: 16px 0 24px;'>
            <div style='font-size:36px; margin-bottom:6px;'>🥇</div>
            <div style='font-size:17px; font-weight:700; color:#F0C040;'>မြန်မာ ရွှေဈေး</div>
            <div style='font-size:11px; color:#6B7A99; letter-spacing:1px; margin-top:2px;'>GOLD ANALYSIS DASHBOARD</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("<div style='font-size:13px; font-weight:600; color:#8892AA; margin-bottom:10px;'>💱 ဒေါ်လာလဲနှုန်း သတ်မှတ်ချက်</div>", unsafe_allow_html=True)

    cbm_rate    = st.number_input("🏦 CBM တရားဝင်လဲနှုန်း (ကျပ်)", min_value=1000.0, max_value=99999.0, value=2100.0, step=10.0, format="%.0f")
    market_rate = st.number_input("🏪 ဈေးကွက် လဲနှုန်း (ကျပ်)", min_value=1000.0, max_value=99999.0, value=3800.0, step=10.0, format="%.0f")

    st.markdown("<div style='margin-top:14px; font-size:13px; font-weight:600; color:#8892AA; margin-bottom:8px;'>⚙️ တွက်ချက်မည့် နှုန်းရွေးချယ်ပါ</div>", unsafe_allow_html=True)
    rate_choice = st.radio(
        "နှုန်းရွေးချယ်ပါ",
        options=["CBM တရားဝင်နှုန်း", "ဈေးကွက်နှုန်း"],
        label_visibility="collapsed",
    )
    selected_rate = cbm_rate if rate_choice == "CBM တရားဝင်နှုန်း" else market_rate

    st.markdown("---")
    st.markdown(f"""
        <div style='background:#161B27; border:1px solid #252D42; border-radius:10px; padding:14px; margin-top:4px;'>
            <div style='font-size:11px; color:#6B7A99; letter-spacing:1px; margin-bottom:6px;'>အသုံးပြုသည့် နှုန်း</div>
            <div style='font-size:22px; font-weight:700; color:#F0C040;'>{selected_rate:,.0f} ကျပ်</div>
            <div style='font-size:11px; color:#4CAF50; margin-top:4px;'>✓ {rate_choice}</div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 ဈေးနှုန်း ပြန်ဆွဲမည်"):
        st.cache_data.clear()

    st.markdown("<br>", unsafe_allow_html=True)
    now_mmst = datetime.now(pytz.timezone("Asia/Rangoon"))
    st.markdown(f"<div style='font-size:11px; color:#3A4455; text-align:center;'>နောက်ဆုံးအချိန် {now_mmst.strftime('%Y-%m-%d %H:%M')} MMT</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MAIN CONTENT
# ─────────────────────────────────────────────
st.markdown("""
    <div style='display:flex; align-items:center; gap:14px; margin-bottom:6px;'>
        <div style='font-size:30px;'>🥇</div>
        <div>
            <div style='font-size:22px; font-weight:700; color:#F0C040;'>မြန်မာ ရွှေဈေး ခွဲခြမ်းစိတ်ဖြာမှု</div>
            <div style='font-size:12px; color:#6B7A99; letter-spacing:1px;'>Myanmar Gold Price Analysis · Smart Money Concepts</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Fetch data
with st.spinner("ရွှေဈေးနှုန်း ဆွဲနေသည်..."):
    try:
        hist, info = fetch_gold_data()
        data_ok = hist is not None and len(hist) > 0
    except Exception as e:
        st.error(f"ဒေတာဆွဲရာတွင် အမှားဖြစ်သည်: {e}")
        data_ok = False

if not data_ok:
    st.warning("ဈေးနှုန်းဒေတာ မရရှိပါ။ Internet ချိတ်ဆက်မှု စစ်ဆေးပါ။")
    st.stop()

# Current price data
gold_price  = hist["Close"].iloc[-1]
gold_prev   = hist["Close"].iloc[-2]
gold_change = gold_price - gold_prev
gold_pct    = (gold_change / gold_prev) * 100
gold_high   = hist["High"].iloc[-1]
gold_low    = hist["Low"].iloc[-1]
gold_open   = hist["Open"].iloc[-1]

mmk_price  = calc_myanmar_gold(gold_price, selected_rate)
mmk_prev   = calc_myanmar_gold(gold_prev,  selected_rate)
mmk_change = mmk_price - mmk_prev

week_high = hist["High"].iloc[-5:].max()
week_low  = hist["Low"].iloc[-5:].min()

change_color = "#4CAF50" if gold_change >= 0 else "#F44336"
change_icon  = "▲" if gold_change >= 0 else "▼"

# ── Hero Myanmar Gold Price ──
st.markdown(f"""
<div class="hero-card">
    <div class="hero-label">🇲🇲 မြန်မာ ရွှေဈေး (၁ ကျပ်သား)</div>
    <div style='display:flex; align-items:flex-end; gap:16px; flex-wrap:wrap;'>
        <div>
            <div class="hero-value">{mmk_price:,.0f}<span class="hero-unit">ကျပ်</span></div>
            <div style='font-size:13px; color:{"#4CAF50" if mmk_change>=0 else "#F44336"}; margin-top:6px;'>
                {"▲" if mmk_change>=0 else "▼"} {abs(mmk_change):,.0f} ကျပ် ({gold_pct:+.2f}%)
            </div>
        </div>
        <div style='flex:1; min-width:200px;'>
            <div style='font-size:12px; color:#6B7A99; margin-bottom:4px;'>တွက်ချက်ပုံစံ</div>
            <div style='font-size:12px; color:#4A5568; font-family:monospace;'>
                ((${gold_price:.2f} × 1.029) × {selected_rate:,.0f}) ÷ 0.576
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Top Metric Row ──
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🌐 ကမ္ဘာ့ ရွှေဈေး (USD)</div>
        <div class="metric-value">${gold_price:,.2f}</div>
        <div class="metric-sub {'negative' if gold_change<0 else ''}">
            {change_icon} ${abs(gold_change):.2f} ({gold_pct:+.2f}%)
        </div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📅 ယနေ့ အမြင့်ဆုံး</div>
        <div class="metric-value" style='font-size:22px;'>${gold_high:,.2f}</div>
        <div class="metric-sub neutral">အနိမ့်ဆုံး: ${gold_low:,.2f}</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📈 ၅ ရက် High / Low</div>
        <div class="metric-value" style='font-size:22px;'>${week_high:,.2f}</div>
        <div class="metric-sub neutral">${week_low:,.2f}</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">💱 သုံးသည့် ဒေါ်လာနှုန်း</div>
        <div class="metric-value" style='font-size:22px;'>{selected_rate:,.0f} ကျပ်</div>
        <div class="metric-sub neutral">{rate_choice}</div>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  CANDLESTICK CHART
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">📊 ရွှေဈေး Chart (နောက်ဆုံး ၆ လ)</div>', unsafe_allow_html=True)

chart_hist = hist.copy()
chart_hist.index = pd.to_datetime(chart_hist.index)

ema9_series  = chart_hist["Close"].ewm(span=9,  adjust=False).mean()
ema21_series = chart_hist["Close"].ewm(span=21, adjust=False).mean()
ema50_series = chart_hist["Close"].ewm(span=50, adjust=False).mean()

fig = go.Figure()

# Candlesticks
fig.add_trace(go.Candlestick(
    x=chart_hist.index,
    open=chart_hist["Open"],
    high=chart_hist["High"],
    low=chart_hist["Low"],
    close=chart_hist["Close"],
    name="XAUUSD",
    increasing_line_color="#26A69A",
    decreasing_line_color="#EF5350",
    increasing_fillcolor="#26A69A",
    decreasing_fillcolor="#EF5350",
))

# EMA Lines
for ema, color, name in [
    (ema9_series,  "#F0C040", "EMA 9"),
    (ema21_series, "#42A5F5", "EMA 21"),
    (ema50_series, "#AB47BC", "EMA 50"),
]:
    fig.add_trace(go.Scatter(
        x=chart_hist.index, y=ema,
        mode="lines", name=name,
        line=dict(color=color, width=1.5),
    ))

# Volume bars
vol_colors = ["#26A69A44" if c >= o else "#EF535044"
              for c, o in zip(chart_hist["Close"], chart_hist["Open"])]
fig.add_trace(go.Bar(
    x=chart_hist.index, y=chart_hist["Volume"],
    name="Volume", marker_color=vol_colors,
    yaxis="y2", showlegend=False,
))

fig.update_layout(
    paper_bgcolor="#0D0F14",
    plot_bgcolor="#0D0F14",
    font=dict(color="#8892AA", size=11),
    xaxis=dict(
        gridcolor="#1A2035", showgrid=True,
        rangeslider=dict(visible=False),
        color="#6B7A99",
    ),
    yaxis=dict(gridcolor="#1A2035", showgrid=True, color="#6B7A99", side="right"),
    yaxis2=dict(
        overlaying="y", side="left",
        showgrid=False, color="#3A4455",
        range=[0, chart_hist["Volume"].max() * 5],
    ),
    legend=dict(
        bgcolor="#13161E", bordercolor="#252D42",
        borderwidth=1, font=dict(size=11),
    ),
    margin=dict(l=10, r=60, t=20, b=20),
    height=460,
    hovermode="x unified",
)

st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────
#  SMC ANALYSIS
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">🧠 Smart Money Concepts ခွဲခြမ်းစိတ်ဖြာမှု</div>', unsafe_allow_html=True)

smc = smc_analysis(hist)

def bias_badge(bias):
    cls   = "bullish" if bias == "Bullish" else "bearish"
    label = "📈 Bullish (တက်မည်)" if bias == "Bullish" else "📉 Bearish (ကျမည်)"
    return f'<span class="badge badge-{cls}">{label}</span>'

if smc:
    d = smc["daily"]
    w = smc["weekly"]
    m = smc["monthly"]

    col1, col2, col3 = st.columns(3)

    # ── Daily ──
    with col1:
        d_bias_cls = d["bias"].lower()
        st.markdown(f"""
        <div class="smc-card">
            <div class="smc-header {d_bias_cls}">📅 နေ့စဉ် (Daily) {bias_badge(d['bias'])}</div>
            <div class="smc-item">
                <div class="smc-dot {d_bias_cls}"></div>
                <div>ရွှေဈေး EMA 9 ({d['ema9']:.2f}) {'အပေါ်' if d['current']>d['ema9'] else 'အောက်'} တွင်ရှိ၍
                {'အားကောင်းသော မတ်တည်မှု' if d['current']>d['ema9'] else 'ဖိအားကြုံနေ'}</div>
            </div>
            <div class="smc-item">
                <div class="smc-dot {d_bias_cls}"></div>
                <div>၅ ရက် အမြင့်ဆုံး ${d['high5']:,.2f} — Liquidity ကို Target ပြုနေ</div>
            </div>
            <div class="smc-item">
                <div class="smc-dot neutral"></div>
                <div>Volume {'ပုံမှန်ထက် မြင့်နေ၍ Institutional မောင်းနှင်မှု ရှိ' if d['vol_high'] else 'ပုံမှန်ကဲ့သို့ — ထပ်မံ Confirmation လိုအပ်'}</div>
            </div>
            <div class="smc-item">
                <div class="smc-dot {d_bias_cls}"></div>
                <div>ပြည်တွင်း ရွှေဈေး ယနေ့ {format_mmk(mmk_price)} နှင့် ရောက်ရှိ</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Weekly ──
    with col2:
        w_bias_cls = w["bias"].lower()
        st.markdown(f"""
        <div class="smc-card">
            <div class="smc-header {w_bias_cls}">📆 အပတ်စဉ် (Weekly) {bias_badge(w['bias'])}</div>
            <div class="smc-item">
                <div class="smc-dot {w_bias_cls}"></div>
                <div>Weekly EMA 20 = ${w['ema20']:,.2f} — ဈေး {'အပေါ်' if w['current']>w['ema20'] else 'အောက်'} ရှိ၍
                {'Buy Side Liquidity ဆီ တိုးတက်မှုမြင်တွေ့' if w['bias']=='Bullish' else 'Sell Side ကို ဆက်ကျနိုင်'}</div>
            </div>
            <div class="smc-item">
                <div class="smc-dot neutral"></div>
                <div>Weekly Range: ${w['low']:,.2f} – ${w['high']:,.2f}
                <br>Structure {'Bullish BOS ဖြစ်' if w['bias']=='Bullish' else 'Bearish BOS ဖြစ်'}</div>
            </div>
            <div class="smc-item">
                <div class="smc-dot {w_bias_cls}"></div>
                <div>Order Block Zone: ${w['low']:,.2f} – ${(w['low']+10):,.2f} ဧရိယာသည် Demand Zone</div>
            </div>
            <div class="smc-item">
                <div class="smc-dot {w_bias_cls}"></div>
                <div>{'Premium ဈေးဇုန်ကို ဆက်တက်နိုင်' if w['bias']=='Bullish' else 'Discount ဇုန်ဆင်း Smart Money စုဆောင်းနိုင်'}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Monthly ──
    with col3:
        m_bias_cls = m["bias"].lower()
        st.markdown(f"""
        <div class="smc-card">
            <div class="smc-header {m_bias_cls}">🗓️ လစဉ် (Monthly) {bias_badge(m['bias'])}</div>
            <div class="smc-item">
                <div class="smc-dot {m_bias_cls}"></div>
                <div>Monthly EMA 50 = ${m['ema50']:,.2f} — ရေရှည် Trend
                {'မြင့်တက်နေ (Higher Highs & Higher Lows)' if m['bias']=='Bullish' else 'ဆင်းနေ (Lower Highs & Lower Lows)'}</div>
            </div>
            <div class="smc-item">
                <div class="smc-dot neutral"></div>
                <div>Monthly Range: ${m['low']:,.2f} – ${m['high']:,.2f}
                <br>Equilibrium (50%): ${(m['high']+m['low'])/2:,.2f}</div>
            </div>
            <div class="smc-item">
                <div class="smc-dot {m_bias_cls}"></div>
                <div>Macro Bias {'Bullish — ကမ္ဘာ့ Central Bank ရွှေဝယ်မှု မြင့်တက်နေ' if m['bias']=='Bullish' else 'Bearish — Risk-On ပတ်ဝန်းကျင်ဖြစ်နေ'}</div>
            </div>
            <div class="smc-item">
                <div class="smc-dot neutral"></div>
                <div>မြန်မာ ၁ ကျပ်သား ရွှေဈေး monthly change ≈ {format_mmk(mmk_price - calc_myanmar_gold(m['open'], selected_rate))}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Summary Banner ──
    overall     = "Bullish" if sum([d["bias"]=="Bullish", w["bias"]=="Bullish", m["bias"]=="Bullish"]) >= 2 else "Bearish"
    overall_cls = overall.lower()
    overall_mm  = "တက်မည် (Bullish) 📈" if overall == "Bullish" else "ကျမည် (Bearish) 📉"
    st.markdown(f"""
    <div style='background: {"linear-gradient(135deg,#0D1A14,#122010)" if overall=="Bullish" else "linear-gradient(135deg,#1A0D0D,#200D0D)"};
                border: 1px solid {"#26A69A40" if overall=="Bullish" else "#EF535040"};
                border-radius:14px; padding:20px 24px; margin-top:6px;'>
        <div style='display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:14px;'>
            <div>
                <div style='font-size:12px; color:#6B7A99; letter-spacing:1px; margin-bottom:4px;'>SMC စုပေါင်း အဆင့်သတ်မှတ်</div>
                <div style='font-size:20px; font-weight:700; color:{"#26A69A" if overall=="Bullish" else "#EF5350"};'>{overall_mm}</div>
            </div>
            <div style='display:flex; gap:10px; flex-wrap:wrap;'>
                <span class='badge badge-{d["bias"].lower()}'>Daily {d["bias"]}</span>
                <span class='badge badge-{w["bias"].lower()}'>Weekly {w["bias"]}</span>
                <span class='badge badge-{m["bias"].lower()}'>Monthly {m["bias"]}</span>
            </div>
            <div style='font-size:13px; color:#6B7A99; max-width:340px;'>
                {"Smart Money အများစုက ဝယ်ဘက်ရပ်တည်နေ၍ Dip ဝယ်ခြင်းသည် Risk/Reward ကောင်း"
                 if overall=="Bullish" else
                 "Smart Money ရောင်းဘက်ရပ်တည်နေ၍ Rally ကို ရောင်းခြင်း သင့်တော်"}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style='margin-top:40px; padding:20px; text-align:center; border-top:1px solid #1E2330;'>
    <div style='font-size:12px; color:#3A4455;'>
        ⚠️ ဤ Dashboard သည် သတင်းအချက်အလက် ရည်ရွယ်ချက်သာဖြစ်သည်။ ရင်းနှီးမြှုပ်နှံမှု အကြံဉာဏ် မဟုတ်ပါ။
    </div>
    <div style='font-size:11px; color:#2A3040; margin-top:6px;'>
        Data: Yahoo Finance (GC=F) · Refreshes every 5 minutes · Built with Streamlit &amp; Plotly
    </div>
</div>
""", unsafe_allow_html=True)
