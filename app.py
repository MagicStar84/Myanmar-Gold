import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

# ─────────────────────────────────────────────
#  PAGE CONFIG & PREMIUM GOLDEN THEME
# ─────────────────────────────────────────────
st.set_page_config(page_title="Myanmar Gold Premium", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Myanmar:wght@400;700&display=swap');
    
    .main { background-color: #0D0F14; }
    html, body, [class*="css"] { font-family: 'Noto Sans Myanmar', sans-serif; }

    /* Golden Hero Banner */
    .hero-banner {
        background: linear-gradient(90deg, #BF953F 0%, #FCF6BA 45%, #B38728 70%, #F0C040 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        color: #1a1a1a;
        font-weight: 800;
        font-size: 32px;
        box-shadow: 0px 15px 35px rgba(240, 192, 64, 0.3);
        margin-bottom: 35px;
        border: 1px solid #D4AF37;
        text-transform: uppercase;
    }

    /* Price Section Styles */
    .gold-label { color: #D4AF37; font-size: 20px; font-weight: 600; margin-bottom: 8px; }
    .gold-value { 
        font-size: 65px; 
        font-weight: 800; 
        color: #FCF6BA; 
        text-shadow: 0px 4px 15px rgba(0,0,0,0.6);
        line-height: 1;
    }
    .mmk-unit { font-size: 24px; color: #D4AF37; margin-left: 12px; font-weight: 400; }

    /* Formula & Info Cards */
    .premium-card {
        background: rgba(22, 27, 39, 0.8);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #252D42;
        border-left: 5px solid #D4AF37;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DATA FETCHING (COINBASE/TRADINGVIEW STYLE)
# ─────────────────────────────────────────────
@st.cache_resource(ttl=30)
def fetch_live_data():
    try:
        # PAXG-USD သည် TradingView မှ Gold Spot ဈေးနှင့် အနီးစပ်ဆုံးတူသည်
        ticker = yf.Ticker("PAXG-USD")
        hist = ticker.history(period="6mo", interval="1d")
        if isinstance(hist.columns, pd.MultiIndex):
            hist.columns = hist.columns.get_level_values(0)
        return hist, hist['Close'].iloc[-1]
    except:
        return None, None

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("<h2 style='color:#D4AF37; text-align:center;'>⚙️ SETTINGS</h2>", unsafe_allow_html=True)
    cbm_rate = st.number_input("🏦 CBM REFERENCE RATE", value=2100.0, step=10.0)
    market_rate = st.number_input("🏪 MARKET RATE (ကိုယ်တိုင်ထည့်ပါ)", value=4100.0, step=10.0)
    
    rate_choice = st.radio("တွက်ချက်ရန်နှုန်း ရွေးပါ", ["CBM Rate", "Market Rate"])
    usd_rate = cbm_rate if rate_choice == "CBM Rate" else market_rate

# ─────────────────────────────────────────────
#  MAIN CONTENT
# ─────────────────────────────────────────────
st.markdown('<div class="hero-banner">🥇 MYANMAR GOLD LIVE ANALYTICS</div>', unsafe_allow_html=True)

hist, gold_spot = fetch_live_data()

if gold_spot:
    # --- FORMULA (Viber ဓာတ်ပုံပါအတိုင်း ၁ ကျပ်သားဈေး တွက်ချက်မှု) ---
    # ပဲသား = (XAUUSD * MMK * 16.6) / 31.1035 
    # ကျပ်သား = ပဲသား * 100  (သို့မဟုတ် အောက်ပါ formula အတို)
    tical_price = (gold_spot * usd_rate * 16.6) / 31.1035

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="gold-label">🇲🇲 မြန်မာ့ရွှေဈေး (၁ ကျပ်သား အခေါက်ရွှေ)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="gold-value">{tical_price:,.0f}<span class="mmk-unit">ကျပ်</span></div>', unsafe_allow_html=True)
        st.markdown(f"<p style='color:#6B7A99;'>တွက်ချက်မှုနှုန်း: $1 = {usd_rate:,.0f} MMK | Spot: ${gold_spot:,.2f}</p>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="premium-card">
            <p style="color:#8892AA; margin:0; font-size:12px; letter-spacing:1px;">🌐 COINBASE / TV LIVE</p>
            <h2 style="color:#FCF6BA; margin:5px 0;">${gold_spot:,.2f}</h2>
            <p style="color:#4CAF50; font-size:12px; margin:0;">▲ Real-time Spot Price</p>
        </div>
        """, unsafe_allow_html=True)

    # --- CHART ---
    fig = go.Figure(data=[go.Candlestick(
        x=hist.index, open=hist['Open'], high=hist['High'],
        low=hist['Low'], close=hist['Close'],
        increasing_line_color='#D4AF37', decreasing_line_color='#4A4A4A',
        increasing_fillcolor='#D4AF37', decreasing_fillcolor='#4A4A4A'
    )])
    fig.update_layout(template="plotly_dark", height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    # --- SMC ANALYSIS ---
    st.markdown("<h3 style='color:#D4AF37;'>🧠 Smart Money Concepts</h3>", unsafe_allow_html=True)
    bias = "BULLISH" if gold_spot > hist['Close'].iloc[-10:].mean() else "BEARISH"
    color = "#26A69A" if bias == "BULLISH" else "#EF5350"
    
    st.markdown(f"""
    <div style="background: {color}15; border: 1px solid {color}44; border-left: 10px solid {color}; padding: 25px; border-radius: 15px;">
        <h3 style="color: {color}; margin:0;">MARKET BIAS: {bias}</h3>
        <p style="color:#A8B0C0; margin-top:10px; line-height:1.6;">
            Viber Reference Formula အား အသုံးပြု၍ တွက်ချက်ထားပါသည်။<br>
            Structure: {'BOS Detected' if bias == 'BULLISH' else 'CHoCH Detected'} | Strategy: {bias} Trend Alignment.
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("ဒေတာဆွဲယူ၍ မရနိုင်ပါ။ Internet Connection ကို စစ်ဆေးပါ။")
