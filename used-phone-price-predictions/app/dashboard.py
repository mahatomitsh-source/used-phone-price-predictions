import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import base64

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def dashboard():

    st.success("🔥 Dashboard Loaded Successfully")

    # ---------- IMAGE PATHS ----------
    banner = os.path.join(BASE_DIR, "images", "phone1.png")
    side_img = os.path.join(BASE_DIR, "images", "phone2.png")
    bg = os.path.join(BASE_DIR, "images", "phone3.png")

    # ---------- BACKGROUND ----------
    if os.path.exists(bg):
        with open(bg, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
                        url("data:image/png;base64,{encoded}");
            background-size: cover;
        }}

        .glass {{
            backdrop-filter: blur(15px);
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 20px;
            color: white;
        }}

        .card {{
            padding: 20px;
            border-radius: 15px;
            background: rgba(255,255,255,0.1);
            text-align: center;
            transition: 0.3s;
        }}

        .card:hover {{
            transform: scale(1.05);
        }}

        .value {{
            font-size: 24px;
            font-weight: bold;
            color: #60a5fa;
        }}
        </style>
        """, unsafe_allow_html=True)

    # ---------- BANNER ----------
    if os.path.exists(banner):
        st.image(banner, width="stretch")

    # ---------- LOAD DATA ----------
    data_path = os.path.join(BASE_DIR, "data", "used_phone-1.csv.xlsx")

    if not os.path.exists(data_path):
        st.error("Dataset not found!")
        return

    df = pd.read_excel(data_path)

    # ---------- FILTERS ----------
    st.sidebar.header("🎛️ Filters")

    ram = st.sidebar.multiselect("RAM", df["ram_gb"].unique())
    storage = st.sidebar.multiselect("Storage", df["storage_gb"].unique())

    if ram:
        df = df[df["ram_gb"].isin(ram)]

    if storage:
        df = df[df["storage_gb"].isin(storage)]

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.title("📊 Premium Dashboard")

    # ---------- METRICS ----------
    c1, c2, c3, c4 = st.columns(4)

    c1.markdown(f"<div class='card'>Total<div class='value'>{len(df)}</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='card'>Avg Price<div class='value'>₹{round(df['resale_price'].mean(),2)}</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='card'>Max<div class='value'>₹{df['resale_price'].max()}</div></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='card'>Min<div class='value'>₹{df['resale_price'].min()}</div></div>", unsafe_allow_html=True)

    st.markdown("---")

    # ---------- CHARTS ----------
    col1, col2 = st.columns([2,1])

    with col1:
        fig, ax = plt.subplots()
        sns.histplot(df["resale_price"], bins=20, kde=True, ax=ax)
        st.pyplot(fig)

    with col2:
        if os.path.exists(side_img):
            st.image(side_img, width="stretch")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        sns.scatterplot(x=df["ram_gb"], y=df["resale_price"], ax=ax)
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()
        sns.boxplot(x=df["storage_gb"], y=df["resale_price"], ax=ax)
        st.pyplot(fig)

    st.markdown('</div>', unsafe_allow_html=True)