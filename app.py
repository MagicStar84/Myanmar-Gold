"""
╔══════════════════════════════════════════════════════════════════╗
║   မြန်မာ ရွှေဈေးကွက် · Myanmar Gold Market Price  v4.0         ║
║   Live XAUUSD · SMC Pro Analysis · Kyat / Pae Calculations       ║
╚══════════════════════════════════════════════════════════════════╝

Formula (Verified):
  1 ကျပ်သား = 16.329 grams  (Myanmar standard tical)
  1 ပဲသား   = 16.329 / 16 = 1.02056 grams
  ကျပ်သားဈေး  = (XAUUSD ÷ 31.1035) × MMK_rate × 16.329
  ပဲသားဈေး   = ကျပ်သားဈေး ÷ 16
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
    page_title="Myanmar Gold Market Price",
    page_icon="🥇",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"About": "Myanmar Gold Market Price · SMC Pro Analysis · v4.0"}
)

# ═══════════════════════════════════════════════════════════════
# CUSTOM CSS
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700;9..40,800;9..40,900&family=Playfair+Display:wght@700;800;900&display=swap');
*{box-sizing:border-box}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif!important}
.stApp{background:#07070b;color:#f0ead8;
  background-image:
    radial-gradient(ellipse 900px 500px at 50% 0%,rgba(255,200,0,.045) 0%,transparent 70%),
    radial-gradient(ellipse 500px 300px at 0% 100%,rgba(255,180,0,.02) 0%,transparent 60%)}
.stApp>header,[data-testid="stHeader"]{background:transparent!important}
[data-testid="stDecoration"]{display:none}
#MainMenu,footer{visibility:hidden}
.block-container{padding-top:0!important;max-width:1280px!important}
section[data-testid="stSidebar"]{background:#0a0908;border-right:1px solid rgba(255,215,0,.07)}
.stTabs [data-baseweb="tab-list"]{background:rgba(255,215,0,.025);border:1px solid rgba(255,215,0,.07);border-radius:14px;gap:4px;padding:5px}
.stTabs [data-baseweb="tab"]{color:#756858!important;font-weight:700!important;font-size:13px!important;border-radius:10px!important;padding:8px 22px!important;transition:all .15s}
.stTabs [aria-selected="true"]{background:rgba(255,215,0,.09)!important;color:#ffd700!important;border:1px solid rgba(255,215,0,.2)!important}
.stTabs [data-baseweb="tab-panel"]{padding-top:22px}
.stButton>button{background:rgba(255,215,0,.06)!important;border:1px solid rgba(255,215,0,.22)!important;color:#ffd700!important;font-weight:700!important;border-radius:10px!important;transition:all .15s!important}
.stButton>button:hover{background:rgba(255,215,0,.14)!important;border-color:rgba(255,215,0,.42)!important;transform:translateY(-1px)}
.stNumberInput>div>div>input,.stTextInput>div>div>input{background:rgba(255,255,255,.025)!important;border:1px solid rgba(255,215,0,.15)!important;border-radius:12px!important;color:#ffd700!important;font-weight:800!important;font-size:22px!important}
.stSelectbox>div>div{background:rgba(14,12,9,.9)!important;border:1px solid rgba(255,215,0,.14)!important;border-radius:10px!important;color:#f0ead8!important}
[data-testid="metric-container"]{background:linear-gradient(150deg,#131108 0%,#0a0908 100%);border:1px solid rgba(255,215,0,.11);border-radius:14px;padding:14px 18px;box-shadow:0 2px 18px rgba(0,0,0,.45)}
[data-testid="metric-container"] label{color:#b09848!important;font-size:10px!important;font-weight:700!important;letter-spacing:1.5px!important;text-transform:uppercase!important}
[data-testid="stMetricValue"]>div{color:#ffd700!important;font-weight:800!important}
.stRadio>div{gap:8px!important}
.stRadio label{color:#b09848!important;font-weight:600!important}
::-webkit-scrollbar{width:4px;height:4px}
::-webkit-scrollbar-track{background:#08070a}
::-webkit-scrollbar-thumb{background:rgba(255,215,0,.16);border-radius:3px}
.gc{background:linear-gradient(150deg,#131108 0%,#0a0908 100%);border:1px solid rgba(255,215,0,.11);border-radius:16px;padding:18px 20px;margin-bottom:10px;box-shadow:0 2px 20px rgba(0,0,0,.45)}
.gc-hl{border-color:rgba(255,215,0,.22);box-shadow:0 4px 32px rgba(255,215,0,.055),inset 0 1px 0 rgba(255,215,0,.055)}
.cl{font-size:9.5px;font-weight:800;color:#b09848;text-transform:uppercase;letter-spacing:1.8px;margin-bottom:9px}
.pb{font-size:42px;font-weight:900;line-height:1.05;
  background:linear-gradient(135deg,#fff8c0,#ffd700,#e0a000,#ffd700);
  background-size:200% 200%;animation:gs 5s ease infinite;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  filter:drop-shadow(0 1px 10px rgba(255,215,0,.14))}
@keyframes gs{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
@keyframes bgs{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
.up{color:#00e676!important;font-weight:700}
.dn{color:#ff4455!important;font-weight:700}
hr{border-color:rgba(255,215,0,.06)!important;margin:14px 0!important}
.stSpinner>div>div{border-top-color:#ffd700!important}
.stAlert{border-radius:12px!important}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════
TROY_OZ = 31.1035        # 1 troy oz in grams
KYAT_G  = 16.329         # 1 ကျပ်သား = 16.329g  (Myanmar tical standard)
PAE_G   = KYAT_G / 16   # 1 ပဲသား   = 1.0206g   (1/16 of kyattha)
CBM_DEF = 2100.0

# ═══════════════════════════════════════════════════════════════
# DATA LAYER
# ═══════════════════════════════════════════════════════════════

@st.cache_data(ttl=30, show_spinner=False)
def fetch_live():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol=XAUUSDT", timeout=8)
        d = r.json()
        if "lastPrice" in d:
            return dict(price=float(d["lastPrice"]), change=float(d["priceChange"]),
                        pct=float(d["priceChangePercent"]), high=float(d["highPrice"]),
                        low=float(d["lowPrice"]), vol=float(d["volume"]), src="Binance XAUUSDT")
    except Exception:
        pass
    try:
        r = requests.get("https://api.coinbase.com/v2/prices/XAU-USD/spot", timeout=8)
        p = float(r.json()["data"]["amount"])
        return dict(price=p, change=0, pct=0, high=0, low=0, vol=0, src="Coinbase XAU-USD")
    except Exception:
        pass
    return None

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_cbm():
    sources = [
        lambda: _cbm_parse(requests.get("https://forex.cbm.gov.mm/api/latest",timeout=8).json(), "CBM Direct"),
        lambda: _cbm_parse(requests.get("https://api.allorigins.win/raw?url=https%3A%2F%2Fforex.cbm.gov.mm%2Fapi%2Flatest",timeout=10).json(), "CBM proxy"),
        lambda: dict(rate=float(requests.get("https://open.er-api.com/v6/latest/USD",timeout=8).json()["rates"]["MMK"]), src="ER-API", date=""),
    ]
    for fn in sources:
        try:
            res = fn()
            if res and res["rate"] > 100:
                return res
        except Exception:
            pass
    return dict(rate=CBM_DEF, src="Offline", date="")

def _cbm_parse(d, src):
    rate = float(d["rates"]["USD"])
    return dict(rate=rate, src=src, date=d.get("info",{}).get("date",""))

@st.cache_data(ttl=300, show_spinner=False)
def fetch_ohlcv(period="3mo", interval="1d"):
    for ticker in ["GC=F", "XAUUSD=X"]:
        try:
            df = yf.Ticker(ticker).history(period=period, interval=interval)
            if not df.empty and len(df) > 10:
                df = df[["Open","High","Low","Close","Volume"]].dropna()
                df.index = pd.to_datetime(df.index).tz_localize(None)
                if 800 < df["Close"].median() < 15000:
                    return df
        except Exception:
            pass
    return pd.DataFrame()

# ═══════════════════════════════════════════════════════════════
# MYANMAR GOLD CALC  (Fixed Formula)
# ═══════════════════════════════════════════════════════════════

def calc_gold(gold_usd, mmk_rate):
    """
    Verified Myanmar Gold Formula:
      usd_per_gram = gold_usd / 31.1035
      kyat_mmk     = usd_per_gram × mmk_rate × 16.329   ← 1 ကျပ်သားprice
      pae_mmk      = kyat_mmk / 16                        ← 1 ပဲသားprice
    """
    usd_per_gram = gold_usd / TROY_OZ
    mmk_per_gram = usd_per_gram * mmk_rate
    kyat_mmk     = mmk_per_gram * KYAT_G        # ← FIXED: direct × 16.329, no ×100
    pae_mmk      = kyat_mmk / 16               # ← 1/16 of kyattha
    return dict(usd_per_gram=usd_per_gram, mmk_per_gram=mmk_per_gram,
                kyat_mmk=kyat_mmk, pae_mmk=pae_mmk)

# ═══════════════════════════════════════════════════════════════
# SMC ENGINE
# ═══════════════════════════════════════════════════════════════

def find_pivots(df, left=5, right=5):
    n = len(df); sh, sl = [], []
    for i in range(left, n-right):
        h = df["High"].iloc[i]
        if all(h >= df["High"].iloc[i-j] for j in range(1,left+1)) and \
           all(h >= df["High"].iloc[i+j] for j in range(1,right+1)):
            sh.append({"idx":i,"price":h,"date":df.index[i]})
        l = df["Low"].iloc[i]
        if all(l <= df["Low"].iloc[i-j] for j in range(1,left+1)) and \
           all(l <= df["Low"].iloc[i+j] for j in range(1,right+1)):
            sl.append({"idx":i,"price":l,"date":df.index[i]})
    return sh, sl

def market_structure(df, sh, sl):
    """
    BOS  = trend continuation, breaks LAST confirmed swing in trend direction
    CHoCH = trend reversal, breaks OPPOSITE swing  (mutually exclusive with BOS of same dir)
    """
    trend = "RANGING"; events = []
    cp = float(df["Close"].iloc[-1])
    if len(sh) < 2 or len(sl) < 2:
        return trend, events
    r_sh = sorted(sh, key=lambda x:x["idx"])[-4:]
    r_sl = sorted(sl, key=lambda x:x["idx"])[-4:]
    hh = r_sh[-1]["price"] > r_sh[-2]["price"]
    hl = r_sl[-1]["price"] > r_sl[-2]["price"]
    lh = r_sh[-1]["price"] < r_sh[-2]["price"]
    ll = r_sl[-1]["price"] < r_sl[-2]["price"]
    if hh and hl:   trend = "BULLISH"
    elif lh and ll: trend = "BEARISH"
    last_sh = r_sh[-1]["price"]
    last_sl = r_sl[-1]["price"]

    if trend == "BULLISH":
        if cp > last_sh:
            events.append(dict(type="BOS",   dir="UP",   level=last_sh, label="BOS ▲  Bullish Continuation"))
        elif cp < last_sl:
            events.append(dict(type="CHoCH", dir="DOWN", level=last_sl, label="CHoCH ▼  Bearish Reversal Alert"))
    elif trend == "BEARISH":
        if cp < last_sl:
            events.append(dict(type="BOS",   dir="DOWN", level=last_sl, label="BOS ▼  Bearish Continuation"))
        elif cp > last_sh:
            events.append(dict(type="CHoCH", dir="UP",   level=last_sh, label="CHoCH ▲  Bullish Reversal Alert"))
    return trend, events

def order_blocks(df, sh, sl, n=4):
    obs = []; cp = float(df["Close"].iloc[-1])
    for pt in sl[-n:]:
        for i in range(pt["idx"]-1, max(0,pt["idx"]-15), -1):
            o,c = df["Open"].iloc[i], df["Close"].iloc[i]
            if c < o:
                mit = len(df)>pt["idx"]+1 and df["Close"].iloc[pt["idx"]+1:].min() < c
                if not mit:
                    obs.append(dict(type="BULLISH",top=o,bottom=c,mid=(o+c)/2,
                                    date=df.index[i],idx=i,label="Bull OB"))
                break
    for pt in sh[-n:]:
        for i in range(pt["idx"]-1, max(0,pt["idx"]-15), -1):
            o,c = df["Open"].iloc[i], df["Close"].iloc[i]
            if c > o:
                mit = len(df)>pt["idx"]+1 and df["Close"].iloc[pt["idx"]+1:].max() > c
                if not mit:
                    obs.append(dict(type="BEARISH",top=c,bottom=o,mid=(c+o)/2,
                                    date=df.index[i],idx=i,label="Bear OB"))
                break
    obs.sort(key=lambda x:x["idx"], reverse=True)
    deduped=[]
    for ob in obs:
        if not any(abs(ob["mid"]-x["mid"])/ob["mid"]<0.005 for x in deduped):
            deduped.append(ob)
    return deduped[:6]

def fair_value_gaps(df):
    fvgs=[]; start=max(2,len(df)-100)
    for i in range(start,len(df)):
        h0,l0=df["High"].iloc[i-2],df["Low"].iloc[i-2]
        h2,l2=df["High"].iloc[i], df["Low"].iloc[i]
        if h0<l2:
            filled=df["Low"].iloc[i:].min()<h0
            fvgs.append(dict(type="BULLISH",top=l2,bottom=h0,mid=(l2+h0)/2,
                             size=l2-h0,date=df.index[i-1],idx=i-1,filled=filled))
        if l0>h2:
            filled=df["High"].iloc[i:].max()>l0
            fvgs.append(dict(type="BEARISH",top=l0,bottom=h2,mid=(l0+h2)/2,
                             size=l0-h2,date=df.index[i-1],idx=i-1,filled=filled))
    fvgs.sort(key=lambda x:x["idx"],reverse=True)
    return fvgs[:10]

def premium_discount(df,sh,sl):
    if not sh or not sl: return "NEUTRAL",0.5
    hi = max(x["price"] for x in sh[-3:]) if len(sh)>=3 else sh[-1]["price"]
    lo = min(x["price"] for x in sl[-3:]) if len(sl)>=3 else sl[-1]["price"]
    rng = hi-lo if hi!=lo else 1
    pct = max(0.0, min(1.0, (df["Close"].iloc[-1]-lo)/rng))
    zone = "PREMIUM" if pct>0.618 else "DISCOUNT" if pct<0.382 else "EQUILIBRIUM"
    return zone, pct

def generate_signal(trend,events,obs,fvgs,zone,cp):
    confs=[]; bull=0; bear=0
    if   trend=="BULLISH": bull+=2; confs.append(("bull","✓  Bullish Market Structure  (HH + HL)"))
    elif trend=="BEARISH": bear+=2; confs.append(("bear","✓  Bearish Market Structure  (LH + LL)"))
    else:                           confs.append(("nt",  "◆  Ranging — No Clear Structure"))
    if   zone=="DISCOUNT":     bull+=1; confs.append(("bull","✓  Discount Zone  <38.2%  (Demand Area)"))
    elif zone=="PREMIUM":      bear+=1; confs.append(("bear","✓  Premium Zone   >61.8%  (Supply Area)"))
    else:                               confs.append(("nt",  "◆  Equilibrium Zone  38–62%"))
    bull_obs=[o for o in obs if o["type"]=="BULLISH"]
    bear_obs=[o for o in obs if o["type"]=="BEARISH"]
    if bull_obs:
        nb=min(bull_obs,key=lambda x:abs(cp-x["mid"])); d=abs(cp-nb["mid"])/cp*100
        if d<0.5:   bull+=3; confs.append(("bull",f"✓  AT Bullish Order Block  ({d:.2f}% dist)"))
        elif d<1.5: bull+=2; confs.append(("bull",f"✓  Near Bullish OB  ({d:.2f}% dist)"))
        elif d<3.0: bull+=1; confs.append(("bull",f"◑  Bullish OB in Range  ({d:.2f}% dist)"))
    if bear_obs:
        nb=min(bear_obs,key=lambda x:abs(cp-x["mid"])); d=abs(cp-nb["mid"])/cp*100
        if d<0.5:   bear+=3; confs.append(("bear",f"✓  AT Bearish Order Block  ({d:.2f}% dist)"))
        elif d<1.5: bear+=2; confs.append(("bear",f"✓  Near Bearish OB  ({d:.2f}% dist)"))
        elif d<3.0: bear+=1; confs.append(("bear",f"◑  Bearish OB in Range  ({d:.2f}% dist)"))
    for f in fvgs:
        if not f["filled"]:
            if f["type"]=="BULLISH" and f["bottom"]*.998<=cp<=f["top"]*1.002:
                bull+=1; confs.append(("bull","✓  Inside Bullish FVG"))
            elif f["type"]=="BEARISH" and f["bottom"]*.998<=cp<=f["top"]*1.002:
                bear+=1; confs.append(("bear","✓  Inside Bearish FVG"))
    for ev in events:
        if ev["type"]=="BOS" and ev["dir"]=="UP":
            bull+=1; confs.append(("bull",f"✓  BOS ▲ Bullish Break  ${ev['level']:,.2f}"))
        elif ev["type"]=="BOS" and ev["dir"]=="DOWN":
            bear+=1; confs.append(("bear",f"✓  BOS ▼ Bearish Break  ${ev['level']:,.2f}"))
        elif ev["type"]=="CHoCH" and ev["dir"]=="UP":
            bull+=2; confs.append(("bull",f"✓  CHoCH ▲ Bullish Reversal  ${ev['level']:,.2f}"))
        elif ev["type"]=="CHoCH" and ev["dir"]=="DOWN":
            bear+=2; confs.append(("bear",f"✓  CHoCH ▼ Bearish Reversal  ${ev['level']:,.2f}"))
    net   = bull-bear
    stars = min(5,max(1,1+(bull+bear)//3))
    if   net>=5: sig,clr="STRONG BUY","bull"
    elif net>=2: sig,clr="BUY","bull"
    elif net<=-5:sig,clr="STRONG SELL","bear"
    elif net<=-2:sig,clr="SELL","bear"
    else:        sig,clr="WAIT","nt"
    return sig,clr,stars,confs

def smc_levels(cp,sig,obs,sh,sl,fvgs):
    bull_obs=sorted([o for o in obs if o["type"]=="BULLISH"],key=lambda x:x["mid"])
    bear_obs=sorted([o for o in obs if o["type"]=="BEARISH"],key=lambda x:x["mid"])
    if sig in ("BUY","STRONG BUY"):
        above=[o for o in bear_obs if o["mid"]>cp]
        a_sh =[x["price"] for x in sh if x["price"]>cp]
        target=(above[0]["bottom"] if above else min(a_sh) if a_sh else cp*1.025)
        below=[o for o in bull_obs if o["bottom"]<cp]
        b_sl =[x["price"] for x in sl if x["price"]<cp]
        stop =(below[-1]["bottom"]*0.999 if below else max(b_sl)*0.999 if b_sl else cp*0.982)
    elif sig in ("SELL","STRONG SELL"):
        below=[o for o in bull_obs if o["mid"]<cp]
        b_sl =[x["price"] for x in sl if x["price"]<cp]
        target=(below[-1]["top"] if below else max(b_sl) if b_sl else cp*0.975)
        above=[o for o in bear_obs if o["top"]>cp]
        a_sh =[x["price"] for x in sh if x["price"]>cp]
        stop =(above[0]["top"]*1.001 if above else min(a_sh)*1.001 if a_sh else cp*1.018)
    else:
        target=(bear_obs[0]["bottom"] if bear_obs else cp*1.02)
        stop  =(bull_obs[-1]["bottom"] if bull_obs else cp*0.98)
    rr=abs(target-cp)/abs(cp-stop) if abs(cp-stop)>0 else 0
    return target,stop,rr

# ═══════════════════════════════════════════════════════════════
# CHART
# ═══════════════════════════════════════════════════════════════

def build_chart(df,sh,sl,obs,fvgs,cp,tflabel,interval="1d"):
    fig=make_subplots(rows=2,cols=1,shared_xaxes=True,
                      vertical_spacing=0.025,row_heights=[0.76,0.24])
    fig.add_trace(go.Candlestick(x=df.index,open=df["Open"],high=df["High"],
        low=df["Low"],close=df["Close"],name="XAUUSD",
        increasing=dict(line=dict(color="#00e676",width=1),fillcolor="rgba(0,230,118,.78)"),
        decreasing=dict(line=dict(color="#ff4455",width=1),fillcolor="rgba(255,68,85,.78)")),row=1,col=1)
    for sp,col,nm in [(21,"#ffd700","EMA 21"),(50,"#7eb3ff","EMA 50"),(200,"#ff8f00","EMA 200")]:
        if len(df)>sp:
            fig.add_trace(go.Scatter(x=df.index,y=df["Close"].ewm(span=sp).mean(),
                name=nm,line=dict(color=col,width=1.2,dash="dot"),opacity=.75),row=1,col=1)
    dm={"1d":timedelta(days=5),"1wk":timedelta(weeks=3),"1mo":timedelta(days=90)}
    end=df.index[-1]+dm.get(interval,timedelta(days=5))
    for ob in obs:
        ib=ob["type"]=="BULLISH"
        fc="rgba(0,230,118,.06)" if ib else "rgba(255,68,85,.06)"
        lc="rgba(0,230,118,.35)" if ib else "rgba(255,68,85,.35)"
        tc="#00e676"             if ib else "#ff4455"
        fig.add_shape(type="rect",x0=ob["date"],x1=end,y0=ob["bottom"],y1=ob["top"],
                      fillcolor=fc,line=dict(color=lc,width=1,dash="dot"),row=1,col=1)
        fig.add_annotation(x=end,y=ob["mid"],text=f"  {ob['label']}",showarrow=False,
            font=dict(size=9,color=tc),xanchor="left",yanchor="middle",row=1,col=1)
    for fvg in [f for f in fvgs if not f["filled"]][:5]:
        ib=fvg["type"]=="BULLISH"
        fc="rgba(0,188,255,.04)" if ib else "rgba(255,160,0,.04)"
        lc="rgba(0,188,255,.18)" if ib else "rgba(255,160,0,.18)"
        fig.add_shape(type="rect",x0=fvg["date"],x1=end,y0=fvg["bottom"],y1=fvg["top"],
                      fillcolor=fc,line=dict(color=lc,width=.7,dash="dash"),row=1,col=1)
    if sh:
        fig.add_trace(go.Scatter(x=[s["date"] for s in sh[-8:]],y=[s["price"] for s in sh[-8:]],
            mode="markers+text",name="SH",marker=dict(symbol="triangle-down",size=9,color="#ff4455"),
            text=["SH"]*len(sh[-8:]),textposition="top center",
            textfont=dict(size=8,color="#ff6677"),showlegend=False),row=1,col=1)
    if sl:
        fig.add_trace(go.Scatter(x=[s["date"] for s in sl[-8:]],y=[s["price"] for s in sl[-8:]],
            mode="markers+text",name="SL",marker=dict(symbol="triangle-up",size=9,color="#00e676"),
            text=["SL"]*len(sl[-8:]),textposition="bottom center",
            textfont=dict(size=8,color="#00ee88"),showlegend=False),row=1,col=1)
    fig.add_hline(y=cp,row=1,col=1,line=dict(color="#ffd700",width=1.2,dash="dot"),
        annotation_text=f"  ${cp:,.2f}",annotation_position="right",
        annotation_font=dict(color="#ffd700",size=11))
    vc=["rgba(0,230,118,.45)" if c>=o else "rgba(255,68,85,.45)" for c,o in zip(df["Close"],df["Open"])]
    fig.add_trace(go.Bar(x=df.index,y=df["Volume"],marker_color=vc,showlegend=False),row=2,col=1)
    fig.update_layout(paper_bgcolor="#07070b",plot_bgcolor="#090810",
        font=dict(family="DM Sans",color="#b09848",size=11),
        xaxis_rangeslider_visible=False,height=640,margin=dict(l=10,r=120,t=46,b=10),
        legend=dict(bgcolor="rgba(12,10,8,.88)",bordercolor="rgba(255,215,0,.1)",
            borderwidth=1,font=dict(size=10),x=0.01,y=0.99),
        title=dict(text=f"<b>XAUUSD  ·  {tflabel}</b>  —  Smart Money Concepts",
            font=dict(color="#ffd700",size=14),x=0.01,y=0.985))
    ax=dict(gridcolor="rgba(255,215,0,.035)",zerolinecolor="rgba(255,215,0,.07)",
            tickfont=dict(color="#786850"),linecolor="rgba(255,215,0,.06)")
    fig.update_xaxes(**ax); fig.update_yaxes(**ax)
    fig.update_yaxes(tickprefix="$",row=1,col=1)
    return fig

# ═══════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════

fks   = lambda n: f"{int(round(n)):,} Ks"
fusd  = lambda n: f"${n:,.2f}"
CLR   = {"bull":("#00e676","rgba(0,230,118,.08)","rgba(0,230,118,.22)"),
         "bear":("#ff4455","rgba(255,68,85,.08)", "rgba(255,68,85,.22)"),
         "nt":  ("#ffaa00","rgba(255,170,0,.08)", "rgba(255,170,0,.22)")}
STARS = lambda n: "⭐"*n+"☆"*(5-n)
SIG_MM={"STRONG BUY":"💪  အင်မတန် ဝယ်ယူ","BUY":"🟢  ဝယ်ယူ",
        "WAIT":"⏳  စောင့်ကြည့်","SELL":"🔴  ရောင်းချ","STRONG SELL":"💨  အင်မတန် ရောင်းချ"}
TRD_MM={"BULLISH":"📈  ဈေးတက် (HH+HL)","BEARISH":"📉  ဈေးကျ (LH+LL)","RANGING":"↔️  ဦးတည်ချက်မရှိ"}
ZONE_MM={"DISCOUNT":"💚  Discount Zone <38.2% — ဝယ်ယူသင့်",
         "PREMIUM":"🔴  Premium Zone >61.8% — ရောင်းသင့်",
         "EQUILIBRIUM":"🟡  Equilibrium 38–62%","NEUTRAL":"⚪  Zone မဆုံးဖြတ်နိုင်"}

def tbadge(t):
    m={"BULLISH":'<span style="color:#00e676;background:rgba(0,230,118,.09);border:1px solid rgba(0,230,118,.22);padding:5px 16px;border-radius:8px;font-weight:800;font-size:13px">▲  BULLISH</span>',
       "BEARISH":'<span style="color:#ff4455;background:rgba(255,68,85,.09);border:1px solid rgba(255,68,85,.22);padding:5px 16px;border-radius:8px;font-weight:800;font-size:13px">▼  BEARISH</span>',
       "RANGING":'<span style="color:#ffaa00;background:rgba(255,170,0,.09);border:1px solid rgba(255,170,0,.22);padding:5px 16px;border-radius:8px;font-weight:800;font-size:13px">◆  RANGING</span>'}
    return m.get(t,m["RANGING"])

def conf_html(confs):
    h=""
    for k,txt in confs:
        c,bg,bo=CLR.get(k,CLR["nt"])
        h+=f'<div style="background:{bg};border:1px solid {bo};border-radius:7px;padding:7px 12px;margin-bottom:5px;font-size:11px;color:{c};font-weight:600">{txt}</div>'
    return h

def run_smc(df,lb):
    sh,sl=find_pivots(df,left=lb,right=lb)
    trend,evts=market_structure(df,sh,sl)
    obs=order_blocks(df,sh,sl,n=4)
    fvgs=fair_value_gaps(df)
    zone,zpct=premium_discount(df,sh,sl)
    cp=float(df["Close"].iloc[-1])
    sig,clr,str_,cf=generate_signal(trend,evts,obs,fvgs,zone,cp)
    target,stop,rr=smc_levels(cp,sig,obs,sh,sl,fvgs)
    return dict(sh=sh,sl=sl,obs=obs,fvgs=fvgs,trend=trend,evts=evts,
                zone=zone,zpct=zpct,cp=cp,sig=sig,clr=clr,str_=str_,confs=cf,
                target=target,stop=stop,rr=rr)

# ═══════════════════════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════════════════════

def main():

    # ─── PROFESSIONAL BANNER ───────────────────────────────────
    st.markdown(f"""
    <div style="
      background:linear-gradient(135deg,#0c0a05 0%,#171208 25%,#1c1609 50%,#171208 75%,#0c0a05 100%);
      border:1px solid rgba(255,215,0,.14);border-radius:22px;
      padding:28px 32px 22px;margin-bottom:22px;position:relative;overflow:hidden;
      box-shadow:0 8px 48px rgba(0,0,0,.65),inset 0 1px 0 rgba(255,215,0,.07)">
      <div style="position:absolute;top:-50px;right:-50px;width:220px;height:220px;border-radius:50%;
        background:radial-gradient(circle,rgba(255,215,0,.07) 0%,transparent 70%);pointer-events:none"></div>
      <div style="position:absolute;bottom:-70px;left:-30px;width:260px;height:260px;border-radius:50%;
        background:radial-gradient(circle,rgba(255,180,0,.04) 0%,transparent 70%);pointer-events:none"></div>
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;flex-wrap:wrap;gap:8px">
        <div style="display:flex;align-items:center;gap:8px">
          <div style="background:rgba(255,215,0,.1);border:1px solid rgba(255,215,0,.2);border-radius:6px;
               padding:3px 10px;font-size:9px;font-weight:800;color:#ffd700;letter-spacing:2px">PRO</div>
          <div style="background:rgba(0,255,136,.07);border:1px solid rgba(0,255,136,.18);border-radius:6px;
               padding:3px 10px;font-size:9px;font-weight:800;color:#00ff88;letter-spacing:1.5px">● LIVE</div>
          <div style="font-size:9px;color:#504838;font-weight:600;letter-spacing:1.5px">SMC · XAUUSD · v4.0</div>
        </div>
        <div style="font-size:10px;color:#504838;font-weight:600">
          📅 {datetime.now().strftime("%d %b %Y  ·  %H:%M")}
        </div>
      </div>
      <div style="display:flex;align-items:flex-end;gap:20px;flex-wrap:wrap">
        <div style="font-family:'Playfair Display',Georgia,serif;font-size:72px;line-height:.95;
          background:linear-gradient(160deg,#fff9d0 0%,#ffd700 30%,#e8a000 55%,#ffe066 75%,#c87800 100%);
          background-size:200% 200%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;
          filter:drop-shadow(0 0 28px rgba(255,215,0,.32));animation:bgs 6s ease infinite">Au</div>
        <div style="padding-bottom:8px">
          <div style="font-size:28px;font-weight:900;line-height:1.15;letter-spacing:-.3px;color:#f4e8c0">
            Myanmar Gold Market Price</div>
          <div style="font-size:14px;font-weight:600;color:#c0a050;letter-spacing:.5px;margin-top:5px">
            မြန်မာ ရွှေဈေးကွက်  ·  ကျပ်သား / ပဲသား  Real-time ဈေးနှုန်း</div>
          <div style="font-size:10px;font-weight:700;color:#6a5538;letter-spacing:2.5px;
               text-transform:uppercase;margin-top:7px">
            Smart Money Concepts  ·  Live XAUUSD  ·  CBM Rate  ·  Daily / Weekly / Monthly</div>
        </div>
      </div>
      <div style="margin-top:18px;padding-top:14px;border-top:1px solid rgba(255,215,0,.07);
           display:flex;gap:22px;flex-wrap:wrap">
        <span style="font-size:10px;color:#6a5538;font-weight:700;letter-spacing:1px">⚡ Binance XAUUSDT</span>
        <span style="font-size:10px;color:#6a5538;font-weight:700;letter-spacing:1px">🏦 CBM USD/MMK</span>
        <span style="font-size:10px;color:#6a5538;font-weight:700;letter-spacing:1px">📊 Gold Futures Chart</span>
        <span style="font-size:10px;color:#6a5538;font-weight:700;letter-spacing:1px">🎯 BOS · CHoCH · OB · FVG</span>
        <span style="font-size:10px;color:#6a5538;font-weight:700;letter-spacing:1px">🇲🇲 ကျပ်သား · ပဲသား · Gram</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ─── FETCH DATA ────────────────────────────────────────────
    with st.spinner(""):
        live = fetch_live()
        cbm  = fetch_cbm()

    # ─── LIVE TICKER BAR ───────────────────────────────────────
    if live:
        up   = live["pct"] >= 0
        arrow= "▲" if up else "▼"
        cc   = "#00e676" if up else "#ff4455"
        bc   = "rgba(0,230,118,.04)" if up else "rgba(255,68,85,.04)"
        bor  = "rgba(0,230,118,.14)" if up else "rgba(255,68,85,.14)"
        st.markdown(f"""
        <div style="background:{bc};border:1px solid {bor};border-radius:14px;
             padding:14px 22px;margin-bottom:20px;
             display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px">
          <div>
            <div style="font-size:9px;color:#756858;font-weight:700;letter-spacing:1.8px;margin-bottom:4px">
              <span style="background:rgba(0,255,136,.1);border:1px solid rgba(0,255,136,.2);
                border-radius:4px;padding:2px 7px;color:#00ff88">● LIVE</span>
              &nbsp; {live['src']} &nbsp;·&nbsp; Auto-refresh 30s
            </div>
            <div style="font-size:38px;font-weight:900;line-height:1.1;
                background:linear-gradient(135deg,#fff8c0,#ffd700,#e0a000);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent">
              ${live['price']:,.2f}</div>
            <div style="font-size:14px;color:{cc};font-weight:700;margin-top:2px">
              {arrow} {abs(live['pct']):.2f}%
              <span style="font-size:12px;color:#756858">
              &nbsp;({'+' if up else ''}{live['change']:,.2f})</span>
            </div>
          </div>
          <div style="display:flex;gap:28px;flex-wrap:wrap;align-items:center">
            <div><div style="font-size:9px;color:#756858;letter-spacing:1.2px;font-weight:700">24H HIGH</div>
              <div style="font-size:20px;font-weight:800;color:#ffd700">${live['high']:,.2f}</div></div>
            <div><div style="font-size:9px;color:#756858;letter-spacing:1.2px;font-weight:700">24H LOW</div>
              <div style="font-size:20px;font-weight:800;color:#ffd700">${live['low']:,.2f}</div></div>
            <div><div style="font-size:9px;color:#756858;letter-spacing:1.2px;font-weight:700">CBM RATE</div>
              <div style="font-size:20px;font-weight:800;color:#00dd77">{cbm['rate']:,.0f} Ks/$</div></div>
            <div><div style="font-size:9px;color:#756858;letter-spacing:1.2px;font-weight:700">UPDATED</div>
              <div style="font-size:13px;font-weight:700;color:#756858">
              {datetime.now().strftime('%H:%M:%S')}</div></div>
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.error("⚠️  Live price ရှာမရ — Internet စစ်ပြီး Refresh နှိပ်ပါ")
        if st.button("↻  Retry"):
            st.cache_data.clear(); st.rerun()

    # ─── TABS ──────────────────────────────────────────────────
    t1, t2, t3 = st.tabs(["📊  ဈေးတွက်ချက်မှု", "📈  Gold Chart", "🎯  SMC Analysis"])

    # ══════════════════════════════════════════════════════════
    # TAB 1  ·  Calculator
    # ══════════════════════════════════════════════════════════
    with t1:
        if not live: st.warning("Live price မရသေးပါ"); return
        p = live["price"]
        col_l, col_r = st.columns([1.1, 1.4], gap="medium")
        with col_l:
            st.markdown('<div class="cl">💵 Market Exchange Rate</div>', unsafe_allow_html=True)
            mkt = st.number_input("1 USD = ? MMK",value=float(int(cbm["rate"])),step=50.0,format="%.0f")
            st.markdown(f"""
            <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:6px">
              <div style="background:rgba(0,221,119,.05);border:1px solid rgba(0,221,119,.15);
                   border-radius:8px;padding:7px 12px;flex:1;min-width:120px">
                <div style="font-size:9px;color:#756858;letter-spacing:1px;font-weight:700">🏦 CBM OFFICIAL</div>
                <div style="font-size:18px;font-weight:800;color:#00dd77">{cbm['rate']:,.0f} Ks</div>
                <div style="font-size:9px;color:#504838">{cbm['src']}</div>
              </div>
              <div style="background:rgba(255,215,0,.04);border:1px solid rgba(255,215,0,.1);
                   border-radius:8px;padding:7px 12px;flex:1;min-width:120px">
                <div style="font-size:9px;color:#756858;letter-spacing:1px;font-weight:700">🏪 MARKET INPUT</div>
                <div style="font-size:18px;font-weight:800;color:#ffd700">{int(mkt):,} Ks</div>
              </div>
            </div>""", unsafe_allow_html=True)
        with col_r:
            st.markdown("""
            <div class="gc">
              <div class="cl">📐 Myanmar Gold Formula (Verified)</div>
              <div style="font-family:'Courier New',monospace;font-size:12px;color:#d4c090;
                line-height:2.4;background:rgba(0,0,0,.32);border:1px solid rgba(255,215,0,.06);
                border-radius:10px;padding:12px 16px;font-weight:600">
                1 ကျပ်သား&nbsp;= <b style="color:#ffd700">16.329 g</b>  ← Myanmar standard tical<br>
                1 ပဲသားa&nbsp;&nbsp;= <b style="color:#ffd700">16.329 ÷ 16 = 1.0206 g</b><br>
                ကျပ်သားMMK = (XAUUSD ÷ 31.1035) × MMK × 16.329<br>
                ပဲသားMMK&nbsp;&nbsp;= ကျပ်သားMMK ÷ 16
              </div>
            </div>""", unsafe_allow_html=True)

        mc  = calc_gold(p, mkt)
        cc2 = calc_gold(p, cbm["rate"])
        diff= mc["kyat_mmk"] - cc2["kyat_mmk"]

        st.markdown('<div class="cl" style="margin:16px 0 10px">🇲🇲 မြန်မာ ရွှေဈေး တွက်ချက်မှု</div>',
                    unsafe_allow_html=True)
        a,b,c_,d = st.columns(4,gap="small")
        with a:
            st.markdown(f"""<div class="gc gc-hl" style="text-align:center">
              <div class="cl">တစ်ကျပ်သား · Market Rate</div>
              <div class="pb">{fks(mc['kyat_mmk'])}</div>
              <div style="font-size:11px;color:#756858;margin-top:4px">≈ {fusd(p*KYAT_G/TROY_OZ)}</div>
            </div>""", unsafe_allow_html=True)
        with b:
            st.markdown(f"""<div class="gc" style="text-align:center">
              <div class="cl">တစ်ကျပ်သား · CBM Rate</div>
              <div style="font-size:28px;font-weight:900;color:#00dd77">{fks(cc2['kyat_mmk'])}</div>
            </div>""", unsafe_allow_html=True)
        with c_:
            st.markdown(f"""<div class="gc" style="text-align:center">
              <div class="cl">တစ်ပဲသား (1.02g)</div>
              <div style="font-size:22px;font-weight:800;color:#ffd700">{fks(mc['pae_mmk'])}</div>
              <div style="font-size:10px;color:#756858;margin-top:2px">≈ {fusd(p*PAE_G/TROY_OZ)}</div>
            </div>""", unsafe_allow_html=True)
        with d:
            st.markdown(f"""<div class="gc" style="text-align:center">
              <div class="cl">1 Gram</div>
              <div style="font-size:13px;font-weight:700;color:#c0a860;margin-bottom:4px">
                USD <b style="color:#ffd700;font-size:16px">{fusd(mc['usd_per_gram'])}</b></div>
              <div style="font-size:13px;font-weight:700;color:#c0a860">
                MMK <b style="color:#ffd700;font-size:15px">{fks(mc['mmk_per_gram'])}</b></div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        dc = "#ff6655" if diff>0 else "#00ff88"
        st.markdown(f"""
        <div style="display:flex;gap:10px;flex-wrap:wrap">
          <div class="gc" style="flex:1;min-width:150px;text-align:center">
            <div style="font-size:9px;color:#756858;letter-spacing:1px;font-weight:700">MARKET RATE</div>
            <div style="font-size:20px;font-weight:900;color:#ffd700">{fks(mc['kyat_mmk'])}</div>
          </div>
          <div class="gc" style="flex:1;min-width:150px;text-align:center">
            <div style="font-size:9px;color:#756858;letter-spacing:1px;font-weight:700">CBM RATE</div>
            <div style="font-size:20px;font-weight:900;color:#00dd77">{fks(cc2['kyat_mmk'])}</div>
          </div>
          <div class="gc gc-hl" style="flex:1;min-width:150px;text-align:center">
            <div style="font-size:9px;color:#756858;letter-spacing:1px;font-weight:700">ကွာဟချက်</div>
            <div style="font-size:20px;font-weight:900;color:{dc}">
              {'+' if diff>=0 else ''}{fks(diff)}</div>
            <div style="font-size:10px;color:#756858">
              {abs(diff/cc2['kyat_mmk']*100):.1f}% {'above' if diff>0 else 'below'} CBM</div>
          </div>
        </div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align:center;font-size:10px;color:#443c2a;margin-top:14px;line-height:2.2">
          ⚠️ ခန့်မှန်းတွက်ချက်ဈေးသာ ဖြစ်ပါသည် — ဆိုင်ပေါက်ဈေးနှင့် ကွဲလွဲနိုင်သည်<br>
          1 ကျပ်သား = {KYAT_G}g  ·  1 ပဲသား = {PAE_G:.4f}g  ·  1 troy oz = {TROY_OZ}g<br>
          Data: {live['src'] if live else 'N/A'}  ·  CBM: {cbm['src']}
        </div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # TAB 2  ·  Chart
    # ══════════════════════════════════════════════════════════
    with t2:
        tc1,tc2,tc3 = st.columns([2,3,1],gap="small")
        with tc1:
            tf = st.selectbox("Timeframe",
                ["Daily (3 Months)","Weekly (1 Year)","Monthly (3 Years)"],key="chart_tf")
        with tc3:
            if st.button("↻  Refresh",key="chart_ref"):
                st.cache_data.clear(); st.rerun()
        TF={"Daily (3 Months)":("3mo","1d",5,"Daily"),
            "Weekly (1 Year)": ("1y","1wk",3,"Weekly"),
            "Monthly (3 Years)":("3y","1mo",2,"Monthly")}
        period,interval,lb,tflabel=TF[tf]
        with st.spinner("📊 Chart data ရယူနေသည်..."):
            df=fetch_ohlcv(period,interval)
        if df.empty:
            st.error("⚠️ yfinance data ရှာမရ — ပြန်ကြိုးစားပါ")
        else:
            A=run_smc(df,lb)
            fig=build_chart(df,A["sh"],A["sl"],A["obs"],A["fvgs"],A["cp"],tflabel,interval)
            st.plotly_chart(fig,use_container_width=True,
                config={"displayModeBar":True,"scrollZoom":True})
            r=df.iloc[-1]; prev=df.iloc[-2] if len(df)>1 else r
            ch=(r["Close"]-prev["Close"])/prev["Close"]*100
            for col_,(lbl,val) in zip(st.columns(6,gap="small"),
                [("Open",f"${r['Open']:,.2f}"),("High",f"${r['High']:,.2f}"),
                 ("Low",f"${r['Low']:,.2f}"),("Close",f"${r['Close']:,.2f}"),
                 ("Change%",f"{ch:+.2f}%"),("Volume",f"{r['Volume']:,.0f}")]):
                col_.metric(lbl,val)

    # ══════════════════════════════════════════════════════════
    # TAB 3  ·  SMC Analysis
    # ══════════════════════════════════════════════════════════
    with t3:
        st.markdown("""
        <div style="background:rgba(255,170,0,.04);border:1px solid rgba(255,170,0,.12);
             border-radius:10px;padding:10px 16px;margin-bottom:18px;
             font-size:11px;color:#756858;line-height:1.8">
          ⚠️ <b style="color:#b09848">Disclaimer:</b>  SMC Analysis သည် Historical Price Action
          ကိုသာ အခြေခံသည်။ ရင်းနှီးမြှုပ်နှံမှု အကြံပေးချက် <b style="color:#c0a860">မဟုတ်ပါ</b>။
          Geopolitical events, Fed policy, USD index တို့ကြောင့် Technical level ကျော်နိုင်သည်။
        </div>""", unsafe_allow_html=True)
        smc_tf=st.radio("📅 Timeframe ရွေးပါ",
            ["Daily  (တနေ့)","Weekly  (တပတ်)","Monthly  (တလ)"],horizontal=True)
        SMC_TF={"Daily  (တနေ့)":("3mo","1d",5,"Daily"),
                "Weekly  (တပတ်)":("1y","1wk",3,"Weekly"),
                "Monthly  (တလ)":("3y","1mo",2,"Monthly")}
        sp,si,slb,slbl=SMC_TF[smc_tf]
        with st.spinner("🧠 SMC ခွဲခြမ်းစိတ်ဖြာနေသည်..."):
            df_s=fetch_ohlcv(sp,si)
        if df_s.empty:
            st.error("Data ရှာမရ"); return
        A=run_smc(df_s,slb); sc=CLR.get(A["clr"],CLR["nt"])

        # Signal Hero
        rgb=("0,230,118" if A["clr"]=="bull" else "255,68,85" if A["clr"]=="bear" else "255,170,0")
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,rgba(255,215,0,.03) 0%,rgba({rgb},.04) 50%,rgba(0,0,0,0) 100%);
          border:1px solid {sc[2]};border-radius:20px;padding:26px;text-align:center;margin-bottom:20px;
          box-shadow:0 4px 32px {sc[1]}">
          <div style="font-size:9px;color:#756858;letter-spacing:3px;margin-bottom:10px">
            {slbl.upper()} TIMEFRAME  ·  XAUUSD  ·  SMC SIGNAL</div>
          <div style="font-size:40px;font-weight:900;color:{sc[0]};margin-bottom:6px">
            {SIG_MM.get(A['sig'],A['sig'])}</div>
          <div style="font-size:22px;margin-bottom:14px">{STARS(A['str_'])}</div>
          <div style="margin-bottom:10px">{tbadge(A['trend'])}</div>
          <div style="font-size:13px;color:#c0a860;margin-top:10px">{TRD_MM.get(A['trend'],'')}</div>
          <div style="font-size:13px;color:#756858;margin-top:5px">
            Current Price  <b style="color:#ffd700;font-size:18px">${A['cp']:,.2f}</b></div>
        </div>""", unsafe_allow_html=True)

        c1,c2,c3=st.columns(3,gap="medium")
        with c1:
            pct_bar=A["zpct"]*100
            st.markdown(f"""
            <div class="gc" style="height:100%">
              <div class="cl">📍 Price Zone (P/D Matrix)</div>
              <div style="font-size:13px;font-weight:700;margin-bottom:12px;line-height:1.5">
                {ZONE_MM.get(A['zone'],'')}</div>
              <div style="position:relative;height:10px;background:rgba(0,0,0,.35);
                border-radius:8px;border:1px solid rgba(255,215,0,.07);overflow:hidden;margin-bottom:4px">
                <div style="height:100%;width:100%;
                  background:linear-gradient(90deg,rgba(0,230,118,.7),rgba(255,215,0,.7),rgba(255,68,85,.7));
                  border-radius:8px;opacity:.55"></div>
                <div style="position:absolute;top:0;left:{pct_bar:.1f}%;transform:translateX(-50%);
                  width:3px;height:100%;background:#ffd700;border-radius:2px;
                  box-shadow:0 0 8px rgba(255,215,0,.6)"></div>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:9px;color:#443c2a;margin-bottom:14px">
                <span>0% Discount</span><span>50%</span><span>100% Premium</span></div>
              <div style="background:rgba(255,215,0,.05);border-radius:8px;padding:10px 14px;
                border:1px solid rgba(255,215,0,.1);text-align:center">
                <div style="font-size:9px;color:#756858;letter-spacing:1px">POSITION</div>
                <div style="font-size:28px;font-weight:900;color:#ffd700">{pct_bar:.1f}%</div>
              </div>
            </div>""", unsafe_allow_html=True)

        with c2:
            tgt_p=(A["target"]-A["cp"])/A["cp"]*100
            stp_p=(A["stop"]-A["cp"])/A["cp"]*100
            rr_c=("#00e676" if A["rr"]>=2.5 else "#ffd700" if A["rr"]>=1.5 else "#ffaa00" if A["rr"]>=1.0 else "#ff4455")
            rr_l=("Excellent ✓✓" if A["rr"]>=2.5 else "Good ✓" if A["rr"]>=1.5 else "Fair" if A["rr"]>=1.0 else "Poor — Wait")
            st.markdown(f"""
            <div class="gc" style="height:100%">
              <div class="cl">🎯 Key Trading Levels</div>
              <div style="background:rgba(0,230,118,.04);border:1px solid rgba(0,230,118,.15);
                border-radius:10px;padding:12px 14px;margin-bottom:10px">
                <div style="font-size:9px;color:#00e676;letter-spacing:1.5px;font-weight:800;margin-bottom:4px">🎯 TARGET</div>
                <div style="font-size:26px;font-weight:900;color:#00e676">${A['target']:,.2f}</div>
                <div style="font-size:11px;color:#756858;margin-top:2px">{tgt_p:+.2f}%  from current</div>
              </div>
              <div style="background:rgba(255,68,85,.04);border:1px solid rgba(255,68,85,.15);
                border-radius:10px;padding:12px 14px;margin-bottom:10px">
                <div style="font-size:9px;color:#ff4455;letter-spacing:1.5px;font-weight:800;margin-bottom:4px">🛡️ STOP LOSS</div>
                <div style="font-size:26px;font-weight:900;color:#ff4455">${A['stop']:,.2f}</div>
                <div style="font-size:11px;color:#756858;margin-top:2px">{stp_p:+.2f}%  from current</div>
              </div>
              <div style="background:rgba(255,215,0,.04);border:1px solid rgba(255,215,0,.12);
                border-radius:10px;padding:12px 14px;text-align:center">
                <div style="font-size:9px;color:#756858;letter-spacing:1px">RISK : REWARD</div>
                <div style="font-size:28px;font-weight:900;color:{rr_c}">1 : {A['rr']:.2f}</div>
                <div style="font-size:10px;color:{rr_c};font-weight:700">{rr_l}</div>
              </div>
            </div>""", unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="gc" style="height:100%">
              <div class="cl">🔗 Confluences ({len(A['confs'])})</div>
              {conf_html(A['confs'])}
            </div>""", unsafe_allow_html=True)

        st.markdown("---")

        # OBs + FVGs
        ob1,ob2=st.columns(2,gap="medium")
        with ob1:
            st.markdown('<div class="cl" style="margin-bottom:10px">📦 Active Order Blocks</div>', unsafe_allow_html=True)
            if A["obs"]:
                for ob in A["obs"][:4]:
                    ib=ob["type"]=="BULLISH"
                    dist=(A["cp"]-ob["mid"])/ob["mid"]*100
                    tc2="#00e676" if ib else "#ff4455"
                    bdc="rgba(0,230,118,.18)" if ib else "rgba(255,68,85,.18)"
                    dc2="#0a1108" if ib else "#110808"
                    st.markdown(f"""
                    <div style="background:{dc2};border:1px solid {bdc};border-radius:10px;
                      padding:10px 14px;margin-bottom:7px;
                      display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">
                      <div>
                        <div style="font-size:10px;font-weight:800;color:{tc2};margin-bottom:3px">
                          {'▲ BULLISH OB (Demand)' if ib else '▼ BEARISH OB (Supply)'}</div>
                        <div style="font-size:11px;color:#c0a860">
                          ${ob['bottom']:,.2f} ↔ ${ob['top']:,.2f}
                          <span style="color:#756858"> mid ${ob['mid']:,.2f}</span></div>
                        <div style="font-size:9px;color:#443c2a">{ob['date'].strftime('%Y-%m-%d')}</div>
                      </div>
                      <div style="background:rgba(255,215,0,.06);border:1px solid rgba(255,215,0,.1);
                        border-radius:6px;padding:5px 10px;text-align:center">
                        <div style="font-size:9px;color:#756858">Dist</div>
                        <div style="font-size:14px;font-weight:800;color:{tc2}">{dist:+.2f}%</div>
                      </div>
                    </div>""", unsafe_allow_html=True)
            else: st.info("Active Order Blocks မတွေ့ပါ")

        with ob2:
            st.markdown('<div class="cl" style="margin-bottom:10px">⚡ Open Fair Value Gaps</div>', unsafe_allow_html=True)
            ofvgs=[f for f in A["fvgs"] if not f["filled"]]
            if ofvgs:
                for fvg in ofvgs[:4]:
                    ib=fvg["type"]=="BULLISH"
                    tc3="#00c8ff" if ib else "#ffa500"
                    bdc3="rgba(0,200,255,.18)" if ib else "rgba(255,165,0,.18)"
                    dc3="#080c13" if ib else "#130d08"
                    dist=(A["cp"]-fvg["mid"])/fvg["mid"]*100
                    st.markdown(f"""
                    <div style="background:{dc3};border:1px solid {bdc3};border-radius:10px;
                      padding:10px 14px;margin-bottom:7px;
                      display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">
                      <div>
                        <div style="font-size:10px;font-weight:800;color:{tc3};margin-bottom:3px">
                          {'⬆ BULLISH FVG' if ib else '⬇ BEARISH FVG'}</div>
                        <div style="font-size:11px;color:#c0a860">
                          ${fvg['bottom']:,.2f} ↔ ${fvg['top']:,.2f}
                          <span style="color:#756858"> size ${fvg['size']:,.2f}</span></div>
                        <div style="font-size:9px;color:#443c2a">{fvg['date'].strftime('%Y-%m-%d')}</div>
                      </div>
                      <div style="background:rgba(255,215,0,.06);border:1px solid rgba(255,215,0,.1);
                        border-radius:6px;padding:5px 10px;text-align:center">
                        <div style="font-size:9px;color:#756858">Dist</div>
                        <div style="font-size:14px;font-weight:800;color:{tc3}">{dist:+.2f}%</div>
                      </div>
                    </div>""", unsafe_allow_html=True)
            else: st.info("Open FVGs မတွေ့ပါ")

        # Structure Events
        if A["evts"]:
            st.markdown('<div class="cl" style="margin-top:6px;margin-bottom:8px">🏗️ Structure Events</div>',
                        unsafe_allow_html=True)
            for ev in A["evts"]:
                iu=ev["dir"]=="UP"
                bc_="rgba(0,230,118,.05)" if iu else "rgba(255,68,85,.05)"
                bo_="rgba(0,230,118,.18)" if iu else "rgba(255,68,85,.18)"
                tc_="#00e676"             if iu else "#ff4455"
                st.markdown(f"""
                <div style="background:{bc_};border:1px solid {bo_};border-radius:8px;
                  padding:9px 16px;margin-bottom:6px;
                  display:flex;justify-content:space-between;align-items:center">
                  <b style="color:{tc_};font-size:12px">{ev['label']}</b>
                  <span style="color:#756858;font-size:11px">
                    Level: <b style="color:#ffd700">${ev['level']:,.2f}</b></span>
                </div>""", unsafe_allow_html=True)

        # Myanmar Summary
        st.markdown("---")
        sc2=CLR.get(A["clr"],CLR["nt"])
        tp2=(A["target"]-A["cp"])/A["cp"]*100
        sp2=(A["stop"]-A["cp"])/A["cp"]*100
        st.markdown(f"""
        <div class="gc gc-hl">
          <div class="cl">🇲🇲 ခွဲခြမ်းစိတ်ဖြာချက် ကျဉ်းချုပ် — {slbl} Timeframe</div>
          <div style="font-size:13px;line-height:2.6;color:#c0a860">
            <div>📅 Timeframe: <b style="color:#ffd700">{slbl}</b></div>
            <div>📍 Trend: <b style="color:#ffd700">{TRD_MM.get(A['trend'],'')}</b></div>
            <div>💹 Zone: <b style="color:#ffd700">{ZONE_MM.get(A['zone'],'')}</b></div>
            <div>🎯 Signal: <b style="color:{sc2[0]};font-size:16px">{SIG_MM.get(A['sig'],'')} &nbsp;{STARS(A['str_'])}</b></div>
            <div>💰 Current: <b style="color:#ffd700">${A['cp']:,.2f}</b></div>
            <div>🎯 Target: <b style="color:#00e676">${A['target']:,.2f} ({tp2:+.2f}%)</b></div>
            <div>🛡️ Stop: <b style="color:#ff4455">${A['stop']:,.2f} ({sp2:+.2f}%)</b></div>
            <div>⚖️ R:R = <b style="color:#ffd700">1 : {A['rr']:.2f}</b></div>
          </div>
          <div style="margin-top:12px;padding:12px 14px;background:rgba(255,170,0,.04);
            border-radius:8px;border:1px solid rgba(255,170,0,.1);
            font-size:11px;color:#756858;line-height:1.8">
            ⚠️ ဤ Analysis သည် Historical Price Action ကိုသာ အခြေခံသည်။
            Geopolitical events, Fed policy, Dollar index ဆိုသည့် အချက်များကြောင့်
            Technical level များကို ကျော်ဝင်နိုင်သည်။<br>
            <b style="color:#c0a860">Past performance does not guarantee future results.</b>
          </div>
        </div>""", unsafe_allow_html=True)

        # Multi-TF
        st.markdown("---")
        st.markdown('<div class="cl" style="margin-bottom:14px">📊 Multi-Timeframe Quick Summary</div>',
                    unsafe_allow_html=True)
        mt_cols=st.columns(3,gap="medium")
        for col_,(lbl2,per2,iv2,lb3) in zip(mt_cols,[("DAILY","3mo","1d",5),("WEEKLY","1y","1wk",3),("MONTHLY","3y","1mo",2)]):
            with col_:
                with st.spinner(""):
                    df_mt=fetch_ohlcv(per2,iv2)
                if not df_mt.empty:
                    Am=run_smc(df_mt,lb3); sc3=CLR.get(Am["clr"],CLR["nt"])
                    tp3=(Am["target"]-Am["cp"])/Am["cp"]*100
                    st.markdown(f"""
                    <div class="gc" style="text-align:center;border-color:{sc3[2]}">
                      <div style="font-size:10px;color:#756858;letter-spacing:2px;font-weight:800;margin-bottom:8px">{lbl2}</div>
                      <div style="font-size:22px;font-weight:900;color:{sc3[0]};margin-bottom:4px">
                        {SIG_MM.get(Am['sig'],Am['sig'])}</div>
                      <div style="font-size:16px;margin:4px 0">{STARS(Am['str_'])}</div>
                      <div style="margin:8px 0">{tbadge(Am['trend'])}</div>
                      <div style="font-size:10px;color:#756858;margin-top:8px">
                        Zone: <b style="color:#b09848">{Am['zone']}</b></div>
                      <div style="font-size:10px;color:{sc3[0]};margin-top:4px;font-weight:700">
                        Target {tp3:+.1f}%  ·  R:R 1:{Am['rr']:.1f}</div>
                      <div style="font-size:11px;color:#443c2a;margin-top:5px">${Am['cp']:,.2f}</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div class="gc" style="text-align:center">
                      <div class="cl">{lbl2}</div>
                      <div style="color:#443c2a">Data N/A</div></div>""",
                      unsafe_allow_html=True)


if __name__ == "__main__":
    main()
