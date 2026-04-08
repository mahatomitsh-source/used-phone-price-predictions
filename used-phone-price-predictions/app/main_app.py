import streamlit as st
import pandas as pd
import pickle
import numpy as np
import os

from login import login_page
from logout import logout

# -----------------------
# Page Config
# -----------------------
st.set_page_config(
    page_title="Phone Price Predictor",
    page_icon="",
    layout="wide"
)
# -----------------------
# BRAND MAPPING
# -----------------------
brand_map = {
    0: "Apple",
    1: "Samsung",
    2: "Xiaomi",
    3: "OnePlus",
    4: "Realme",
    5: "Oppo",
    6: "Vivo",
    7: "Nokia",
    8: "Motorola",
    9: "Google",
    10: "Huawei",
    11: "Sony",
    12: "LG",
    13: "Asus",
    14: "Lenovo",
    15: "Micromax",
    16: "Infinix",
    17: "Tecno",
    18: "Honor",
    19: "Nothing"
}
# -----------------------
# Base Directory
# -----------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# -----------------------
# Session State
# -----------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# -----------------------
# DASHBOARD (PREMIUM)
# -----------------------
def dashboard():

    import plotly.express as px

    # ---------- DARK MODE ----------
    dark_mode = st.sidebar.toggle("🌙 Dark Mode")

    if dark_mode:
        bg_color = "#111827"
        text_color = "white"
        card_bg = "#1f2937"
    else:
        bg_color = "#f9fafb"
        text_color = "black"
        card_bg = "white"

    # ---------- STYLE ----------
    st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}

    .header-box {{
        padding: 25px;
        border-radius: 15px;
        background: linear-gradient(90deg, #2563eb, #3b82f6);
        color: white;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 25px;
    }}

    .card {{
        padding: 20px;
        border-radius: 15px;
        background: {card_bg};
        box-shadow: 0px 6px 15px rgba(0,0,0,0.08);
        text-align: center;
    }}

    .card-title {{
        font-size: 14px;
        color: gray;
    }}

    .card-value {{
        font-size: 24px;
        font-weight: bold;
        color: #2563eb;
    }}

    .section-box {{
        padding: 20px;
        border-radius: 15px;
        background: {card_bg};
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="header-box"> Phone Price Dashboard</div>', unsafe_allow_html=True)

    # ---------- LOAD DATA ----------
    data_path = os.path.join(BASE_DIR, "data", "used_phone-1.csv.xlsx")

    if not os.path.exists(data_path):
        st.error("Dataset not found!")
        return

    df = pd.read_excel(data_path)

    # ---------- FILTERS ----------
    st.sidebar.subheader(" Filters")

    ram_filter = st.sidebar.multiselect(
        "RAM",
        sorted(df["ram_gb"].unique()),
        default=sorted(df["ram_gb"].unique())
    )

    storage_filter = st.sidebar.multiselect(
        "Storage",
        sorted(df["storage_gb"].unique()),
        default=sorted(df["storage_gb"].unique())
    )

    price_range = st.sidebar.slider(
        "Price Range",
        int(df["resale_price"].min()),
        int(df["resale_price"].max()),
        (int(df["resale_price"].min()), int(df["resale_price"].max()))
    )

    filtered_df = df[
        (df["ram_gb"].isin(ram_filter)) &
        (df["storage_gb"].isin(storage_filter)) &
        (df["resale_price"].between(price_range[0], price_range[1]))
    ]

    # ---------- DOWNLOAD ----------
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Filtered Data", csv, "filtered_data.csv")

    # ---------- METRICS ----------
    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(f"<div class='card'><div class='card-title'>Total Phones</div><div class='card-value'>{len(filtered_df)}</div></div>", unsafe_allow_html=True)

    col2.markdown(f"<div class='card'><div class='card-title'>Average Price</div><div class='card-value'>₹{round(filtered_df['resale_price'].mean(),2)}</div></div>", unsafe_allow_html=True)

    col3.markdown(f"<div class='card'><div class='card-title'>Max Price</div><div class='card-value'>₹{filtered_df['resale_price'].max()}</div></div>", unsafe_allow_html=True)

    col4.markdown(f"<div class='card'><div class='card-title'>Min Price</div><div class='card-value'>₹{filtered_df['resale_price'].min()}</div></div>", unsafe_allow_html=True)

    # ---------- CHARTS ----------
    st.markdown('<div class="section-box">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(filtered_df, x="resale_price")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.scatter(filtered_df, x="ram_gb", y="resale_price")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- BOX ----------
    st.markdown('<div class="section-box">', unsafe_allow_html=True)

    fig = px.box(filtered_df, x="storage_gb", y="resale_price")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- AI INSIGHTS ----------
    st.markdown('<div class="section-box">', unsafe_allow_html=True)

    st.subheader("🤖 Insights")
    st.write(f"💡 Avg Price: ₹{round(filtered_df['resale_price'].mean(),2)}")

    best_ram = filtered_df.groupby("ram_gb")["resale_price"].mean().idxmax()
    st.write(f" Best performing RAM: {best_ram} GB")

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- TABLE ----------
    st.markdown('<div class="section-box">', unsafe_allow_html=True)

    st.dataframe(filtered_df, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------
# PREDICTION
# -----------------------
def prediction():

    import base64
    import plotly.express as px

    img1 = os.path.join(BASE_DIR, "images", "phone1.jpg")

    if os.path.exists(img1):
        with open(img1, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()

        st.markdown(f"""
        <style>

        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
        }}

        .glass {{
            backdrop-filter: blur(15px);
            background: rgba(255,255,255,0.85);
            padding: 30px;
            border-radius: 20px;
        }}

        .result-box {{
            padding: 20px;
            border-radius: 15px;
            background: linear-gradient(90deg, #16a34a, #22c55e);
            color: white;
            text-align: center;
            font-size: 22px;
            font-weight: bold;
        }}

        @keyframes gradientMove {{
            0% {{ background-position: 0% }}
            100% {{ background-position: 100% }}
        }}

        .animated-title {{
            font-size: 42px;
            font-weight: bold;
            text-align: center;
            background: linear-gradient(90deg, #2563eb, #9333ea, #06b6d4);
            background-size: 200%;
            -webkit-background-clip: text;
            color: transparent;
            animation: gradientMove 3s linear infinite;
        }}

        </style>
        """, unsafe_allow_html=True)
    # ---------- CENTER ----------
    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.markdown('<div class="glass">', unsafe_allow_html=True)

        st.markdown("""
        <h1 class="animated-title">
        📱 Smart Phone Price Predictor
        </h1>
        """, unsafe_allow_html=True)

        # ---------- LOAD MODEL ----------
        model_path = os.path.join(BASE_DIR, "models", "used_phone.pkl")
        scaler_path = os.path.join(BASE_DIR, "models", "scaler.pkl")
        data_path = os.path.join(BASE_DIR, "data", "used_phone-1.csv.xlsx")

        if not os.path.exists(model_path):
            st.error("Model not found!")
            return

        model = pickle.load(open(model_path, "rb"))
        scaler = pickle.load(open(scaler_path, "rb"))
        df = pd.read_excel(data_path)

        # ---------- INPUTS ----------
        colA, colB = st.columns(2)

        with colA:
            brand_name = st.selectbox("Select Brand", list(brand_map.values()))

        # convert name → ID
            brand = list(brand_map.keys())[list(brand_map.values()).index(brand_name)]
            model_name = st.number_input("Model ID", 0)
            ram = st.selectbox("RAM", [2,4,6,8,12,16])
            storage = st.selectbox("Storage", [32,64,128,256,512])

        with colB:
            condition = st.slider("Condition", 0, 10, 5)
            battery = st.slider("Battery Health", 50, 100, 80)
            age = st.slider("Age", 0, 5, 1)
            original_price = st.number_input("Original Price", 1000)

        # ---------- BUTTON ----------
        if st.button(" Predict Price"):

            features = np.array([[brand, model_name, ram, storage, condition, battery, age, original_price]])
            features = scaler.transform(features)
            pred = model.predict(features)[0]

            # ---------- RESULT ----------
            st.markdown(f"""
            <div class="result-box">
                 Predicted Price: ₹ {pred:.2f}
            </div>
            """, unsafe_allow_html=True)

            # ---------- AI INSIGHT ----------
            avg_price = df["resale_price"].mean()

            if pred > avg_price:
                st.success(" High-value phone (Above average)")
            else:
                st.info(" Budget-friendly phone")

            # ---------- RECOMMENDATION ----------
            best_ram = df.groupby("ram_gb")["resale_price"].mean().idxmax()
            best_storage = df.groupby("storage_gb")["resale_price"].mean().idxmax()

            st.subheader("🤖 AI Recommendation")
            st.write(f" Best RAM for value: **{best_ram} GB**")
            st.write(f" Best Storage for value: **{best_storage} GB**")

            # ---------- COMPARISON GRAPH ----------
            st.subheader(" Price Comparison")

            sample_df = df.sample(100)

            fig = px.scatter(
                sample_df,
                x="ram_gb",
                y="resale_price",
                title="Market Price Distribution"
            )

            # highlight predicted point
            fig.add_scatter(
                x=[ram],
                y=[pred],
                mode='markers',
                marker=dict(size=12),
                name="Your Phone"
            )

            st.plotly_chart(fig, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)


# -----------------------
# MAIN ROUTING
# -----------------------

if not st.session_state.logged_in:
    login_page()

else:
    st.sidebar.title(" Navigation")

    # Menu (only pages, no logout here)
    page = st.sidebar.radio(
        "Menu",
        ["Dashboard", "Prediction"]
    )

    st.sidebar.markdown("---")

    #  Logout Button
    if st.sidebar.button(" Logout", use_container_width=True):
        logout()

    # -----------------------
    # PAGE ROUTING
    # -----------------------
    if page == "Dashboard":
        dashboard()

    elif page == "Prediction":
        prediction()