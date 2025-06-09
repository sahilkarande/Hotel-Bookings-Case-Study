import streamlit as st
import pandas as pd
import numpy as np

# ----------------------------
# Streamlit Page Config
# ----------------------------
st.set_page_config(
    page_title="🏨 Hotel Booking Dashboard",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/sahilkarande/HotelBookingDashboard',
        'Report a bug': 'mailto:sahilkarande@example.com',
        'About': "Hotel Booking Analysis Dashboard by Sahil Karande"
    }
)

# ----------------------------
# Custom CSS for Dark Theme & Sidebar
# ----------------------------
st.markdown("""
<style>
    body, .stApp, .main {
        background-color: #121212;
        color: #E0E0E0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #FFFFFF !important;
        font-weight: 700;
        text-shadow: none !important;
    }

    .css-1d391kg, .st-bc {
        background-color: #1E1E1E;
        border-radius: 12px;
        padding: 20px;
        color: #CCCCCC !important;
    }

    .stButton > button, .stDownloadButton > button {
        background-color: #000000 !important;
        border: 2px solid #1E90FF !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        padding: 0.5em 1.2em !important;
        font-weight: 600 !important;
    }

    .stButton > button:hover, .stDownloadButton > button:hover {
        background-color: #1E90FF !important;
        color: #000000 !important;
        cursor: pointer;
    }

    .stRadio > div, .stMultiSelect > div, .stSlider > div, .stTextInput > div, .stSelectbox > div {
        background-color: #2A2A2A;
        border-radius: 4px;
        padding: 4px 8px !important;
        color: #DDDDDD !important;
        font-size: 14px !important;
    }

    .stDataFrame > div > div {
        scrollbar-width: thin;
        scrollbar-color: #555555 #1E1E1E;
    }

    .stDataFrame > div > div::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    .stDataFrame > div > div::-webkit-scrollbar-thumb {
        background-color: #555555;
        border-radius: 4px;
    }

    .block-container {
        padding: 2rem !important;
        max-width: 1200px !important;
        margin: auto;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Load and Preprocess Dataset
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Assets/hotel_bookings.csv")
    df['agent'] = df['agent'].fillna(0).astype(int)
    df['children'] = df['children'].fillna(0)
    df['country'] = df['country'].fillna(df['country'].mode()[0])
    df.drop(['company'], axis=1, inplace=True, errors='ignore')

    df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])
    df['arrival_date'] = pd.to_datetime(
        df['arrival_date_year'].astype(str) + '-' +
        df['arrival_date_month'].astype(str) + '-' +
        df['arrival_date_day_of_month'].astype(str),
        format='%Y-%B-%d', errors='coerce')
    df['arrival_day_name'] = df['arrival_date'].dt.day_name()
    df['total_stay_nights'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    df['departure_date'] = df['arrival_date'] + pd.to_timedelta(df['total_stay_nights'], unit='D')
    df['total_members'] = df['adults'] + df['children'] + df['babies']
    df['revenue_generated'] = df['adr'] * df['total_stay_nights']
    df['room_change'] = df['reserved_room_type'].astype(str) != df['assigned_room_type'].astype(str)
    df['stay_duration'] = df['total_stay_nights']
    df.drop_duplicates(inplace=True)

    return df

df = load_data()

# ----------------------------
# Sidebar Filters (Collapsed by Default)
# ----------------------------
st.sidebar.header("🔎 Filter Options")

with st.sidebar.expander("🏨 Hotel Type", expanded=False):
    hotel_type = st.multiselect("Select hotel type(s):", options=df['hotel'].unique(), default=df['hotel'].unique())

with st.sidebar.expander("🌍 Guest Country (Top 20)", expanded=False):
    countries = st.multiselect("Select countries:", options=df['country'].value_counts().index[:20], default=df['country'].value_counts().index[:10])

with st.sidebar.expander("❌ Cancellation Status", expanded=False):
    cancel_option = st.radio("Show bookings:", ['All', 'Canceled', 'Not Canceled'], index=0)

with st.sidebar.expander("👤 Customer Type", expanded=False):
    customer_types = st.multiselect("Choose customer types:", options=df['customer_type'].unique(), default=df['customer_type'].unique())

with st.sidebar.expander("📦 Market Segment", expanded=False):
    segment_options = st.multiselect("Select market segments:", options=df['market_segment'].unique(), default=df['market_segment'].unique())

with st.sidebar.expander("💰 Advanced Filters", expanded=False):
    min_adr, max_adr = float(df['adr'].min()), float(df['adr'].max())
    min_adr_selected, max_adr_selected = st.slider("Select ADR range (₹):", min_value=round(min_adr, 2), max_value=round(max_adr, 2), value=(round(min_adr, 2), round(max_adr, 2)), step=1.0)

    min_lt, max_lt = int(df['lead_time'].min()), int(df['lead_time'].max())
    lead_time_range = st.slider("Lead Time (days):", min_value=min_lt, max_value=max_lt, value=(min_lt, max_lt), step=1)

    room_change_filter = st.selectbox("Room Changed?", options=["All", "Yes", "No"], index=0)

# ----------------------------
# Apply Filters
# ----------------------------
filtered_df = df[
    (df['hotel'].isin(hotel_type)) &
    (df['country'].isin(countries)) &
    (df['customer_type'].isin(customer_types)) &
    (df['market_segment'].isin(segment_options)) &
    (df['adr'] >= min_adr_selected) & (df['adr'] <= max_adr_selected) &
    (df['lead_time'] >= lead_time_range[0]) & (df['lead_time'] <= lead_time_range[1])
]

if cancel_option == 'Canceled':
    filtered_df = filtered_df[filtered_df['is_canceled'] == 1]
elif cancel_option == 'Not Canceled':
    filtered_df = filtered_df[filtered_df['is_canceled'] == 0]

if room_change_filter == 'Yes':
    filtered_df = filtered_df[filtered_df['room_change'] == True]
elif room_change_filter == 'No':
    filtered_df = filtered_df[filtered_df['room_change'] == False]

# ----------------------------
# Dashboard Header
# ----------------------------
# ----------------------------
# Business Metrics (Blue-White Theme)
# ----------------------------
st.subheader("📌 Business Metrics Overview")

metric_style = """
    <div style="background-color:#1e1e1e; padding:1rem; border-radius:12px; 
                text-align:center; border:1px solid #2e2e2e;">
        <h5 style="color:white;">{label}</h5>
        <p style="font-size:24px; color:#1f77b4; font-weight:bold;">{value}</p>
    </div>
"""

# First Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(metric_style.format(label="Total Bookings", value=f"{len(filtered_df):,}"), unsafe_allow_html=True)
with col2:
    st.markdown(metric_style.format(label="Average ADR", value=f"₹{filtered_df['adr'].mean():.2f}"), unsafe_allow_html=True)
with col3:
    st.markdown(metric_style.format(label="Avg. Stay (Nights)", value=f"{filtered_df['total_stay_nights'].mean():.2f}"), unsafe_allow_html=True)
with col4:
    st.markdown(metric_style.format(label="Revenue Generated", value=f"₹{filtered_df['revenue_generated'].sum():,.0f}"), unsafe_allow_html=True)
st.markdown("---")  # Separator line for clarity
# Second Row
col5, col6, col7 = st.columns(3)
with col5:
    st.markdown(metric_style.format(label="Total Guests", value=f"{int(filtered_df['total_members'].sum()):,}"), unsafe_allow_html=True)
with col6:
    st.markdown(metric_style.format(label="Cancellation Rate", value=f"{filtered_df['is_canceled'].mean() * 100:.1f}%"), unsafe_allow_html=True)
with col7:
    st.markdown(metric_style.format(label="Room Reassignments", value=f"{filtered_df['room_change'].mean() * 100:.1f}%"), unsafe_allow_html=True)

# ----------------------------
# Date Range Display
# ----------------------------
# ----------------------------
# Booking Date Range Metric (Custom Styled)
# ----------------------------
min_date = filtered_df['arrival_date'].min().date()
max_date = filtered_df['arrival_date'].max().date()

with st.container():
    st.markdown("""
    <div style='
        background-color: #1e1e1e;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin-top: 1.5rem;
        border: 1px solid #444;
        '>
        <h4 style='color:#ffffff;'>📅 Booking Date Range</h4>
        <p style='font-size: 20px; font-weight: 600; color: #00BFFF;'>{} <span style='color:#888;'>to</span> {}</p>
    </div>
    """.format(min_date.strftime("%d %b %Y"), max_date.strftime("%d %b %Y")),
    unsafe_allow_html=True)

# ----------------------------
# Statistical Summary
# ----------------------------
st.subheader("📊 Statistical Testing Insights")
st.markdown("""
- **ADR Comparison** (Online TA vs Direct): No significant difference *(p > 0.05)*  
- **Room Upgrade vs Lead Time**: Significant association *(Chi², p < 0.05)*  
- **Stay Duration by Customer Type**: Varies significantly *(ANOVA, p < 0.05)*  
- **Lead Time vs Booking Changes**: Weak positive relationship *(ρ ≈ 0.08)*  
""")

# ----------------------------
# Filtered Data Preview
# ----------------------------
st.subheader("🗃️ Filtered Data Preview")
st.dataframe(filtered_df.head(100), use_container_width=True)

# ----------------------------
# Visual Insights
# ----------------------------
st.subheader("📊 Visual Insights")

with st.container():
    st.markdown("#### 🏨 Bookings by Hotel Type")
    st.bar_chart(filtered_df['hotel'].value_counts())

    st.markdown("#### 🌍 Top 10 Countries by Booking Count")
    st.bar_chart(filtered_df['country'].value_counts().head(10))

with st.container():
    st.markdown("#### 📅 Arrival Day Distribution")
    st.bar_chart(filtered_df['arrival_day_name'].value_counts())

    st.markdown("#### 💰 ADR (Average Daily Rate) Distribution")
    st.area_chart(filtered_df['adr'].value_counts().sort_index())

with st.container():
    st.markdown("#### 🧾 Revenue Trend by Stay Duration")
    stay_revenue = filtered_df.groupby('total_stay_nights')['revenue_generated'].sum()
    st.line_chart(stay_revenue)

    st.markdown("#### 🔄 Lead Time vs Booking Changes")
    lead_changes = filtered_df.groupby('lead_time')['booking_changes'].mean()
    st.line_chart(lead_changes)

with st.container():
    st.markdown("#### 📈 ADR by Customer Type")
    adr_customer = filtered_df.groupby('customer_type')['adr'].mean()
    st.bar_chart(adr_customer)

    st.markdown("#### 📈 Cancellation Rate by Customer Type")
    cancel_rate = filtered_df.groupby('customer_type')['is_canceled'].mean()
    st.bar_chart(cancel_rate)

    st.markdown("#### ⏱️ Average Lead Time by Market Segment")
    lead_market = filtered_df.groupby('market_segment')['lead_time'].mean()
    st.bar_chart(lead_market)

# ----------------------------
# Download Option
# ----------------------------
st.subheader("📤 Export Filtered Dataset")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📄 Download Filtered Data as CSV",
    data=csv,
    file_name='filtered_hotel_bookings.csv',
    mime='text/csv',
    use_container_width=True
)

# ----------------------------
# Footer
# ----------------------------
st.markdown("""
---
<p style='text-align:center; color: #F0F8FF;'>Made with ❤️ by <b>Sahil Karande</b></p>
""", unsafe_allow_html=True)
