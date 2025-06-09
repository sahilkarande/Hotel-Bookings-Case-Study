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
# Custom CSS for Sidebar and Global Styling
# ----------------------------
st.markdown("""
<style>
    /* Global text and background */
    body, .stApp, .main {
        background-color: #121212;
        color: #E0E0E0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #FFFFFF !important;
        font-weight: 700;
        text-shadow: none !important;
    }

    /* Sidebar */
    .css-1d391kg, .st-bc {
        background-color: #1E1E1E;
        border-radius: 12px;
        padding: 20px;
        box-shadow: none !important;
        color: #CCCCCC !important;
    }

    /* Buttons */
    .stButton > button, .stDownloadButton > button {
        background-color: #000000 !important;
        border: 2px solid #1E90FF !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        padding: 0.5em 1.2em !important;
        font-weight: 600 !important;
        transition: background-color 0.3s ease, color 0.3s ease;
        box-shadow: none !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background-color: #1E90FF !important;
        color: #000000 !important;
        cursor: pointer;
        box-shadow: none !important;
    }

    /* Inputs, sliders, selects: less round, compact height */
    .stRadio > div, .stMultiSelect > div, .stSlider > div, .stTextInput > div, .stSelectbox > div {
        background-color: #2A2A2A;
        border-radius: 4px;          /* reduced from 8px */
        padding: 4px 8px !important; /* reduced vertical padding */
        color: #DDDDDD !important;
        box-shadow: none !important;
        min-height: 32px !important; /* reduce height */
        font-size: 14px !important;
    }

    /* Scrollbar style */
    .stDataFrame > div > div {
        scrollbar-width: thin;
        scrollbar-color: #555555 #1E1E1E;
    }
    .stDataFrame > div > div::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    .stDataFrame > div > div::-webkit-scrollbar-track {
        background: #1E1E1E;
    }
    .stDataFrame > div > div::-webkit-scrollbar-thumb {
        background-color: #555555;
        border-radius: 4px;
    }

    /* Container padding & max width */
    .block-container {
        padding: 2rem !important;
        max-width: 1200px !important;
        margin-left: auto !important;
        margin-right: auto !important;
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
# Sidebar Filters
# ----------------------------
st.sidebar.header("🔎 Filter Options")

# Reset filters button
if st.sidebar.button("🔄 Reset Filters"):
    st.session_state.clear()  # Clear session state variables if any
    st.experimental_rerun()

# Hotel Type Filter (multiselect)
with st.sidebar.expander("🏨 Hotel Type", expanded=True):
    hotel_type = st.multiselect(
        "Select hotel type(s):",
        options=df['hotel'].unique().tolist(),
        default=df['hotel'].unique().tolist(),
        help="Filter bookings by hotel type"
    )

# Guest Country Filter (top 20, searchable)
with st.sidebar.expander("🌍 Guest Country (Top 20)", expanded=True):
    countries = st.multiselect(
        "Select countries:",
        options=df['country'].value_counts().index[:20].tolist(),
        default=df['country'].value_counts().index[:10].tolist(),
        help="Top 20 guest countries by bookings"
    )

# Cancellation Status Radio
with st.sidebar.expander("❌ Cancellation Status", expanded=True):
    cancel_option = st.radio(
        "Show bookings:",
        options=['All', 'Canceled', 'Not Canceled'],
        index=0,
        help="Filter bookings by cancellation status"
    )

# Customer Type Filter
with st.sidebar.expander("👤 Customer Type", expanded=True):
    customer_types = st.multiselect(
        "Choose customer types:",
        options=df['customer_type'].unique().tolist(),
        default=df['customer_type'].unique().tolist(),
        help="Filter by customer type"
    )

# Market Segment Filter
with st.sidebar.expander("📦 Market Segment", expanded=False):
    segment_options = st.multiselect(
        "Select market segments:",
        options=df['market_segment'].unique().tolist(),
        default=df['market_segment'].unique().tolist(),
        help="Filter by market segment"
    )

# Average Daily Rate Slider
with st.sidebar.expander("💰 Average Daily Rate (ADR)", expanded=True):
    min_adr = float(df['adr'].min())
    max_adr = float(df['adr'].max())
    min_adr_selected, max_adr_selected = st.slider(
        "Select ADR range:",
        min_value=round(min_adr, 2),
        max_value=round(max_adr, 2),
        value=(round(min_adr, 2), round(max_adr, 2)),
        step=1.0,
        help="Filter bookings by ADR (₹)"
    )

    # Lead Time Range Slider
    min_lt = int(df['lead_time'].min())
    max_lt = int(df['lead_time'].max())
    lead_time_range = st.slider(
        "Lead Time (days):",
        min_value=min_lt,
        max_value=max_lt,
        value=(min_lt, max_lt),
        step=1,
        help="Days between booking and arrival"
    )

    # Room Change Filter
    room_change_filter = st.selectbox(
        "Room Changed?",
        options=["All", "Yes", "No"],
        index=0,
        help="Filter if assigned room differs from reserved room"
    )


# ----------------------------
# Apply Filters
# ----------------------------
filtered_df = df[
    (df['hotel'].isin(hotel_type)) &
    (df['country'].isin(countries)) &
    (df['customer_type'].isin(customer_types)) &
    (df['market_segment'].isin(segment_options)) &
    (df['adr'] >= min_adr_selected) &
    (df['adr'] <= max_adr_selected) &
    (df['lead_time'] >= lead_time_range[0]) &
    (df['lead_time'] <= lead_time_range[1])
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
st.title("🏨 Hotel Booking Analysis Dashboard")
st.markdown("""
This interactive dashboard provides insights into hotel booking trends, guest behavior,
cancellation patterns, revenue generation, and other key performance metrics. Use the filters on the left
to customize the visualizations and gain targeted insights.
""")

# ----------------------------
# Key Metrics
# ----------------------------
st.subheader("📌 Business Metrics Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Bookings", len(filtered_df))
col2.metric("Average ADR", f"₹{filtered_df['adr'].mean():.2f}")
col3.metric("Avg. Stay (Nights)", f"{filtered_df['total_stay_nights'].mean():.2f}")
col4.metric("Revenue Generated", f"₹{filtered_df['revenue_generated'].sum():,.0f}")

col5, col6, col7 = st.columns(3)
col5.metric("Total Guests", int(filtered_df['total_members'].sum()))
col6.metric("Cancellation Rate", f"{filtered_df['is_canceled'].mean() * 100:.1f}%")
col7.metric("Room Reassignments", f"{filtered_df['room_change'].mean() * 100:.1f}%")

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
# Data Preview
# ----------------------------
st.subheader("🗃️ Filtered Data Preview")
st.dataframe(filtered_df.head(100), use_container_width=True)

# ----------------------------
# Visual Insights
# ----------------------------
st.subheader("📊 Visual Insights")

with st.container():
    st.markdown("#### 🏨 Bookings by Hotel Type")
    hotel_counts = filtered_df['hotel'].value_counts().reset_index()
    hotel_counts.columns = ['Hotel Type', 'Bookings']
    st.bar_chart(hotel_counts.set_index('Hotel Type'))

    st.markdown("#### 🌍 Top 10 Countries by Booking Count")
    top_countries = filtered_df['country'].value_counts().head(10).reset_index()
    top_countries.columns = ['Country', 'Bookings']
    st.bar_chart(top_countries.set_index('Country'))

with st.container():
    st.markdown("#### 📅 Arrival Day Distribution")
    day_distribution = filtered_df['arrival_day_name'].value_counts().reset_index()
    day_distribution.columns = ['Day', 'Bookings']
    st.bar_chart(day_distribution.set_index('Day'))

    st.markdown("#### 💰 ADR (Average Daily Rate) Distribution")
    adr_data = filtered_df['adr'].value_counts().sort_index().reset_index()
    adr_data.columns = ['ADR', 'Frequency']
    st.area_chart(adr_data.set_index('ADR'))

with st.container():
    st.markdown("#### 🧾 Revenue Trend by Stay Duration")
    stay_revenue = filtered_df.groupby('total_stay_nights')[['revenue_generated']].sum().reset_index()
    st.line_chart(stay_revenue.set_index('total_stay_nights'))

    st.markdown("#### 🔄 Lead Time vs Booking Changes")
    lead_changes = filtered_df.groupby('lead_time')['booking_changes'].mean().reset_index()
    st.line_chart(lead_changes.set_index('lead_time'))

with st.container():
    st.markdown("#### 📈 ADR by Customer Type")
    adr_customer = filtered_df.groupby('customer_type')[['adr']].mean().reset_index()
    st.bar_chart(adr_customer.set_index('customer_type'))

    st.markdown("#### 📈 Cancellation Rate by Customer Type")
    cancel_rate = filtered_df.groupby('customer_type')['is_canceled'].mean().reset_index()
    cancel_rate.columns = ['customer_type', 'Cancellation Rate']
    st.bar_chart(cancel_rate.set_index('customer_type'))

    st.markdown("#### ⏱️ Average Lead Time by Market Segment")
    lead_market = filtered_df.groupby('market_segment')['lead_time'].mean().reset_index()
    lead_market.columns = ['market_segment', 'Avg Lead Time']
    st.bar_chart(lead_market.set_index('market_segment'))

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
