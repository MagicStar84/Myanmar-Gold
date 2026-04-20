import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

# ─────────────────────────────────────────────
#  PAGE CONFIG & PREMIUM GOLDEN CSS
# ─────────────────────────────────────────────
st.set_page_config(page_title="Myanmar Gold Premium", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Myanmar:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans Myanmar', sans-serif;
    background-color: #0D0F14;
}

/* Premium Golden Banner */
.hero-banner {
    background: linear-gradient(90deg, #BF953F 0%, #FCF6BA 45%, #B38728 70%, #F0C040 100%);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    color: #1a1a1a;
    font-weight: 800;
    font-size: 32px;
    box-shadow: 0px 15px 35px rgba(240, 192, 64, 0.25);
    margin-bottom: 35px;
    border: 1px solid #D4AF37;
}

/* Golden Price Display */
.gold-value { 
    font-size: 65px; 
    font-weight: 800; 
    color: #FCF6BA; 
    text-shadow: 0px 4px 15px rgba(0,0,0,0.6);
    line-height: 1;
}
.mmk-unit { font-size: 24px; color: #D4AF37; font-weight: 400; margin-left: 10px; }

.premium-card {
    background: rgba(22, 27, 39, 0.8);
    padding: 20px;
    border-radius: 15px;
    border-left: 5px solid #D4AF37;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DATA FETCHING (TRADING VIEW / COINBASE ALIGNMENT)
# ─────────────────────────────────────────────
@st.cache_resource(ttl=60)
def fetch_gold_data():
    try:
        # TradingView နှင့် ဈေးနှုန်းတူစေရန် 'PAXG-USD' (Digital Gold Spot) ကို သုံးထားသည်
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
    st.markdown("<h2 style='color:#D4AF37; text-align:center;'>🏆 Settings</h2>", unsafe_allow_html=True)
    cbm_rate = st.number_input("CBM ဒေါ်လာဈေး", value=2100.0)
    market_rate = st.number_input("ပြင်ပဒေါ်လာဈေး", value=4500.0)
    rate_choice = st.radio("တွက်ချက်ရန်နှုန်း", ["CBM နှုန်း", "ပြင်ပဈေး"])
    selected_rate = cbm_rate if rate_choice == "CBM နှုန်း" else market_rate

# ─────────────────────────────────────────────
#  MAIN UI
# ─────────────────────────────────────────────
st.markdown('<div class="hero-banner">🥇 MYANMAR GOLD MARKET ANALYTICS</div>', unsafe_allow_html=True)

hist, live_gold = fetch_gold_data()

if live_gold:
    # Formula အမှန် (၁ ကျပ်သားဈေး) 
    # Formula: ((World_Price * 1.029) * USD_Rate) / 0.576
    mm_price = (live_gold * 1.029 * selected_rate) / 0.576
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("<div style='color: #D4AF37; font-size: 20px;'>🇲🇲 မြန်မာ့ရွှေဈေး (၁ ကျပ်သား)</div>", unsafe_allow_html=True)
        st.markdown(f'<div class="gold-value">{mm_price:,.0f}<span class="mmk-unit">ကျပ်</span></div>', unsafe_allow_html=True)
        st.markdown(f"<p style='color:#6B7A99;'>တွက်ချက်မှုနှုန်း: $1 = {selected_rate:,.0f} MMK | Spot: ${live_gold:,.2f}</p>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="premium-card">
            <p style="color:#8892AA; margin:0; font-size:12px;">🌐 WORLD GOLD SPOT</p>
            <h2 style="color:#FCF6BA; margin:5px 0;">${live_gold:,.2f}</h2>
        </div>
        """, unsafe_allow_html=True)

    # Candlestick Chart 
    fig = go.Figure(data=[go.Candlestick(
        x=hist.index, open=hist['Open'], high=hist['High'],
        low=hist['Low'], close=hist['Close'],
        increasing_line_color='#D4AF37', decreasing_line_color='#4A4A4A'
    )])
    fig.update_layout(template="plotly_dark", height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

    # SMC Analysis Banner 
    bias = "BULLISH" if live_gold > hist['Close'].iloc[-10:].mean() else "BEARISH"
    color = "#26A69A" if bias == "BULLISH" else "#EF5350"
    st.markdown(f"""
    <div style="background: {color}22; border-left: 10px solid {color}; padding: 20px; border-radius: 12px;">
        <h3 style="color: {color}; margin:0;">MARKET BIAS: {bias}</h3>
        <p style="color:#E8ECF0; margin-top:10px;">SMC Structure အရ ဈေးကွက်လားရာသည် {bias} ဖြစ်နေသည်။</p>
    </div>
    """, unsafe_allow_html=True)
