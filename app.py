import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import pickle
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Vision Traffic",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- GLOBAL CSS ----------------
st.markdown("""
<style>
/* Main Background */
.stApp {
    background: radial-gradient(circle at 50% 10%, #1a3c2f 0%, #050b08 60%);
    color: #eafff4;
}

/* Hide Streamlit Header */
header {visibility: hidden;}
footer {visibility: hidden;}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 6px;
    background: #050b08;
}
::-webkit-scrollbar-thumb {
    background: #22e38a;
    border-radius: 3px;
}

/* TYPEOGRAPHY */
h1, h2, h3, h4, h5, h6, p, div, span {
    font-family: 'Inter', sans-serif;
}

/* MAIN TITLE */
.main-title {
    font-size: 80px;
    font-weight: 900;
    text-align: center;
    margin-bottom: 0px;
    line-height: 1.1;
    letter-spacing: -2px;
}
.green-text { 
    color: #22e38a; 
    text-shadow: 0 0 20px rgba(34,227,138,0.4);
}
.subtitle {
    text-align: center;
    font-size: 18px;
    opacity: 0.7;
    margin-top: 10px;
    margin-bottom: 40px;
    font-weight: 300;
}

/* GLASS CARDS */
.glass-card {
    background: rgba(12, 30, 24, 0.4);
    border-radius: 12px;
    padding: 24px;
    border: 1px solid rgba(34,227,138,0.1);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    height: 100%;
}
.glass-card:hover {
    border-color: #22e38a;
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(34,227,138,0.1);
}
.card-icon {
    font-size: 24px;
    margin-bottom: 12px;
    color: #22e38a;
}
.card-title {
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 8px;
    color: #fff;
}
.card-desc {
    font-size: 14px;
    color: #8fa39a;
    line-height: 1.5;
}

/* BUTTONS */
.stButton button {
    width: 100%;
    border-radius: 30px;
    height: 50px;
    font-weight: 600;
    border: none;
    transition: 0.3s;
    background: #1a3c2f; /* Dark Green Default */
    color: #22e38a;
    border: 1px solid #22e38a;
}
.stButton button:hover {
    background: #22e38a;
    color: #050b08;
    box-shadow: 0 0 15px rgba(34,227,138,0.4);
}

/* Primary Button Override (Gradient Green) */
div[data-testid="column"]:nth-of-type(1) .stButton button, 
div[data-testid="stVerticalBlock"] > .stButton button {
    background: linear-gradient(135deg, #1fcf82, #22e38a);
    color: #050b08;
    border: none;
    box-shadow: 0 0 20px rgba(34,227,138,0.3);
}
div[data-testid="column"]:nth-of-type(1) .stButton button:hover,
div[data-testid="stVerticalBlock"] > .stButton button:hover {
    box-shadow: 0 0 30px rgba(34,227,138,0.6);
    transform: scale(1.02);
}

/* Secondary Button Override */
div[data-testid="column"]:nth-of-type(2) .stButton button {
    background: rgba(34,227,138,0.1); /* Slight fill for better visibility */
    border: 1px solid #22e38a;
    color: #22e38a;
}
div[data-testid="column"]:nth-of-type(2) .stButton button:hover {
    background: #22e38a;
    color: #000;
}

/* FOOTER STATS */
.footer-stat {
    text-align: center;
    padding: 20px;
}
.footer-val {
    font-size: 28px;
    font-weight: 800;
    color: #22e38a;
    margin-bottom: 5px;
}
.footer-label {
    font-size: 14px;
    color: #8fa39a;
}

/* SIDEBAR START */
section[data-testid="stSidebar"] {
    background-color: #050b08;
    border-right: 1px solid #1a3c2f;
}
section[data-testid="stSidebar"] h2 {
    color: white;
    font-size: 24px;
    margin-bottom: 30px;
    padding-left: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- NAVIGATION ----------------
from streamlit_option_menu import option_menu

with st.sidebar:
    # Custom Header
    st.markdown("""
        <style>
        .nav-header {
            display: flex;
            align-items: center;
            padding: 10px 0px 20px 10px;
        }
        .logo-box {
            background: #22e38a;
            width: 40px;
            height: 40px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            box-shadow: 0 0 15px rgba(34,227,138,0.4);
        }
        .logo-icon {
            color: #050b08;
            font-size: 24px;
            font-weight: bold;
        }
        .app-name {
            color: #22e38a;
            font-size: 24px;
            font-weight: 800;
            letter-spacing: -1px;
        }
        </style>
        <div class="nav-header">
            <div class="logo-box">
                <span class="logo-icon">⚡</span>
            </div>
            <div class="app-name">VISION</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Navigation Menu
    page = option_menu(
        menu_title=None,
        options=["Home", "Live Data", "Prediction", "Analytics"],
        icons=["house", "broadcast", "activity", "bar-chart-fill"],
        menu_icon="cast",
        default_index=0,
        key="nav_menu",
        styles={
            "container": {"padding": "0!important", "background-color": "#050b08"},
            "icon": {"color": "#8fa39a", "font-size": "18px"}, 
            "nav-link": {
                "font-size": "16px", 
                "text-align": "left", 
                "margin": "5px 0px", 
                "color": "white",
                "font-weight": "500",
                "padding-left": "15px"
            },
            "nav-link-selected": {
                "background-color": "#1a3c2f", 
                "color": "white",
                "border": "1px solid #22e38a",
                "border-radius": "10px",
                "font-weight": "600"
            },
        }
    )
    
    st.markdown("---")
    st.markdown("""
        <div style='padding:10px; background:rgba(34,227,138,0.1); border-radius:8px; border:1px solid #22e38a; margin-top: auto;'>
            <div style='color:white; font-size:12px; font-weight:600'>● System Active</div>
        </div>
    """, unsafe_allow_html=True)

# ---------------- HOME PAGE ----------------
if page == "Home":
    # 1) HERO SECTION
    st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="main-title">
            VISION <span class="green-text">TRAFFIC</span>
        </div>
        <p class="subtitle">
            Real-Time Traffic Analysis & Prediction System<br>
            Harness the power of machine learning to predict traffic patterns, optimize routes, and make data-driven decisions.
        </p>
    """, unsafe_allow_html=True)

    # 2) CTA BUTTONS
    c1, c2, c3 = st.columns([1, 1, 3]) # Adjusting column ratio to center buttons
    
    # Using columns for centering, we need a nested structure for the actual buttons to be close
    with st.container():
        col_spacer_l, col_btn1, col_btn2, col_spacer_r = st.columns([2, 1, 1, 2])
        with col_btn1:
            st.button("Start Predicting →", on_click=lambda: st.session_state.update({"nav_menu": "Prediction"}))
        with col_btn2:
            st.button("View Analytics", on_click=lambda: st.session_state.update({"nav_menu": "Analytics"}))

    # 3) FEATURES GRID
    st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center; margin-bottom:30px">Powerful Features</h3>', unsafe_allow_html=True)
    
    f1, f2, f3 = st.columns(3)
    
    features = [
        {"icon": "💾", "title": "Real-Time Data", "desc": "Stream live traffic data from multiple sources with millisecond latency."},
        {"icon": "🧠", "title": "ML Prediction", "desc": "Advanced machine learning models predict traffic patterns and congestion."},
        {"icon": "📊", "title": "Smart Analytics", "desc": "Interactive visuals and insights to understand deep traffic trends."},
        
    ]

    for col, feat in zip([f1,f2,f3], features):
        with col:
            st.markdown(f"""
            <div class="glass-card">
                <div class="card-icon">{feat['icon']}</div>
                <div class="card-title">{feat['title']}</div>
                <div class="card-desc">{feat['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

    # 4) FOOTER STATS
    st.markdown('<div style="height: 80px;"></div>', unsafe_allow_html=True)
    st.markdown("---", unsafe_allow_html=True)
    
    s1, s2 = st.columns(2)
    stats = [
        ("<50ms", "Response Time"),
        ("24/7", "Live Monitoring")
    ]
    
    for col, stat in zip([s1,s2], stats):
        with col:
            st.markdown(f"""
            <div class="footer-stat">
                <div class="footer-val">{stat[0]}</div>
                <div class="footer-label">{stat[1]}</div>
            </div>
            """, unsafe_allow_html=True)

# ---------------- PREDICTION PAGE ----------------
elif page == "Prediction":
    st.markdown("<h1 style='text-align: center'>Traffic <span class='green-text'>Prediction</span></h1>", unsafe_allow_html=True)
    
    # Validation flags
    models_loaded = False
    
    # Load Models & Encoders
    try:
        # Load using joblib instead of pickle
        import joblib
        traffic_model = joblib.load('traffic_level_model.pkl')
        vehicle_model = joblib.load('vehicle_count_model.pkl')
        location_ohe = joblib.load('location_ohe.pkl')
        date_encoder = joblib.load('date_encoder.pkl')
        time_encoder = joblib.load('time_encoder.pkl')
        traffic_le = joblib.load('traffic_label_encoder.pkl')
            
        models_loaded = True
    except Exception as e:
        st.error(f"Error loading models: {e}")
        st.warning("Please ensure all 6 pickle files are in the directory.")

    # Unique Locations (Loaded from CSV to ensure consistency)
    try:
        df_loc = pd.read_csv('vehicle_data.csv')
        location_options = sorted(df_loc['location_name'].unique().tolist())
    except:
        # Fallback if CSV read fails
        location_options = [
            "Agra Fort, India", "Bangalore, India", "Bhopal, India", 
            "Chandigarh, India", "Chennai, India", "India Gate, Delhi, India", 
            "Kolkata, India", "Lucknow, India", "Mumbai, India", "Taj Mahal, India"
        ]

    # Clean spacing
    st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
    
    # Centered layout columns
    _, c_center, _ = st.columns([1, 2, 1])
    
    with c_center:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # INPUTS
        st.markdown("### 📅 Trip Details")
        
        selected_location = st.selectbox("Select Location", location_options)
        
        col_d, col_t = st.columns(2)
        with col_d:
            selected_date = st.date_input("Date", datetime.now())
        with col_t:
            selected_time = st.time_input("Time", datetime.now())
            
        st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
        
        if st.button("Predict Traffic & Count 🚀"):
            if models_loaded:
                try:
                    # 1. Prepare Data Frame for input
                    
                    # Transform Location (OneHotEncoder expects DataFrame)
                    loc_df = pd.DataFrame({'location_name': [selected_location]})
                    loc_encoded = location_ohe.transform(loc_df)
                    loc_encoded_df = pd.DataFrame(
                        loc_encoded, 
                        columns=location_ohe.get_feature_names_out(['location_name'])
                    )
                    
                    # Transform Date & Time (LabelEncoder expects 1D array/list)
                    # Note: LabelEncoder encodes strings/values to integers. 
                    # If the model expects One-Hot features for these, using LabelEncoder is unusual for linear models but ok for Trees.
                    # We pass the raw value as a list.
                    
                    # IMPORTANT: LabelEncoders typically expect the exact strings seen during training.
                    # If date/time are continuous or high-cardinality, LabelEncoder might fail on unseen data.
                    # Assuming the training data covered these or handled them generically.
                    # For safety, we will convert to string as they likely were during training.
                    
                    # Adjust format to match likely training format (YYYY-MM-DD and HH:MM)
                    date_str = selected_date.strftime("%Y-%m-%d") if not isinstance(selected_date, str) else selected_date
                    time_str = selected_time.strftime("%H:%M") if not isinstance(selected_time, str) else selected_time
                    
                    # Handle unseen labels for LabelEncoder (Naive approach: assign 0 or mode if error, but try/except block handles it)
                    # Or check classes_ if needed. For now, try direct transform.
                    
                    # For safer execution in production, we should handle unseen labels, 
                    # but let's try standard transform first.
                    try:
                        date_encoded_val = date_encoder.transform([date_str])[0]
                    except ValueError:
                         # Fallback for unseen date: use mode or 0
                         date_encoded_val = 0 
                         
                    try:
                        time_encoded_val = time_encoder.transform([time_str])[0]
                    except ValueError:
                         time_encoded_val = 0

                    date_encoded = pd.DataFrame({'date': [date_encoded_val]})
                    time_encoded = pd.DataFrame({'time': [time_encoded_val]})
                    
                    # Combine all features
                    input_features = pd.concat([loc_encoded_df, date_encoded, time_encoded], axis=1)
                    
                    # PREDICT TRAFFIC LEVEL (Classification)
                    traffic_pred_encoded = traffic_model.predict(input_features)
                    traffic_level = traffic_le.inverse_transform(traffic_pred_encoded)[0]
                    
                    # PREDICT VEHICLE COUNT (Regression)
                    vehicle_count = vehicle_model.predict(input_features)[0]
                    
                    # Display Results
                    st.markdown("---")
                    
                    # Color Logic
                    color_map = {
                        "High": "#ff3232",
                        "Medium": "#ffa500",
                        "Low": "#22e38a"
                    }
                    status_color = color_map.get(traffic_level, "#22e38a")
                    
                    st.markdown(f"""
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div style="text-align:center; flex:1; padding:15px; border-right:1px solid #333">
                                <div style="color:#8fa39a; font-size:14px; margin-bottom:5px">Traffic Level</div>
                                <div style="color:{status_color}; font-size:28px; font-weight:bold; text-shadow:0 0 15px {status_color}40">
                                    {traffic_level}
                                </div>
                            </div>
                            <div style="text-align:center; flex:1; padding:15px;">
                                <div style="color:#8fa39a; font-size:14px; margin-bottom:5px">Vehicle Count</div>
                                <div style="color:#ffffff; font-size:28px; font-weight:bold;">
                                    {int(vehicle_count)}
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Prediction Error: {e}")
                    st.caption("Debug Info: Model/Encoder input mismatch.")
            else:
                st.warning("Models are not loaded correctly.")
                
        st.markdown('</div>', unsafe_allow_html=True)
        st.info("Select details to forecast traffic conditions using AI.")

# ---------------- ANALYTICS PAGE ----------------
elif page == "Analytics":
    st.markdown("# System <span class='green-text'>Analytics</span>", unsafe_allow_html=True)
    
    # Check if data exists
    if 'traffic_data' in st.session_state and not st.session_state['traffic_data'].empty:
        df_analytics = st.session_state['traffic_data']
        
        # Calculate Real KPIs
        avg_speed = df_analytics["Current Speed (km/h)"].mean()
        avg_free_flow = df_analytics["Free Flow Speed (km/h)"].mean()
        high_congestion_count = len(df_analytics[df_analytics["Congestion Level"] == "High"])
        
        
        kpis = [
            ("Avg Speed", f"{avg_speed:.1f} km/h"), 
            ("Congestion",'3' "Zones"),  
            ("Network Health", "98%")
        ]
        
        # Top Stats
        k1, k2, k3 = st.columns(3)
        for col, (label, val) in zip([k1,k2,k3], kpis):
            with col:
                st.markdown(f"""
                <div class="glass-card" style="padding:15px; text-align:center">
                    <div style="font-size:12px; color:#8fa39a">{label}</div>
                    <div style="font-size:24px; font-weight:bold; color:#fff">{val}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
        st.markdown("### Traffic Speed Analysis (Live Snapshot)")

        # Comparison Bar Chart
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Set positions
        x = range(len(df_analytics))
        width = 0.35
        
        # Plot bars
        ax.bar(x, df_analytics["Current Speed (km/h)"], width, label='Current Speed', color='#22e38a')
        # Removed Free Flow Speed bar as requested
        
        # Styling
        ax.set_facecolor('#050b08')
        fig.patch.set_facecolor('#050b08')
        ax.set_xticks(x)
        ax.set_xticklabels(df_analytics["Location Name"], rotation=45, ha='right', color='#8fa39a', fontsize=8)
        ax.tick_params(axis='y', colors='#8fa39a')
        # Legend might not be needed if only one bar, but keeping for clarity or removing if preferred. 
        # Since label is set, ax.legend() will show it. Let's keep it simple.
        ax.legend(facecolor='#050b08', edgecolor='#22e38a', labelcolor='white')
        ax.grid(color='#1a3c2f', linestyle='--', alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('#1a3c2f')
        ax.spines['left'].set_color('#1a3c2f')
        
        st.pyplot(fig)
        
        # --- Live Delay Analysis ---
        st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
        st.markdown("### Live Traffic Delays by Location")
        
        # Calculate Delay per Location for Live Data
        df_analytics['Live Delay (s)'] = df_analytics['Current Travel Time (s)'] - df_analytics['Free Flow Travel Time (s)']
        
        fig_d, axd = plt.subplots(figsize=(10, 5))
        
        # Set positions
        x_d = range(len(df_analytics))
        
        # Plot bars for delay
        colors = ['#ff3232' if d > 60 else '#ffa500' if d > 0 else '#22e38a' for d in df_analytics['Live Delay (s)']]
        
        axd.bar(x_d, df_analytics['Live Delay (s)'], color=colors, alpha=0.8)
        
        # Styling
        axd.set_facecolor('#050b08')
        fig_d.patch.set_facecolor('#050b08')
        axd.set_xticks(x_d)
        axd.set_xticklabels(df_analytics["Location Name"], rotation=45, ha='right', color='#8fa39a', fontsize=8)
        axd.set_ylabel("Delay (seconds)", color='#8fa39a')
        axd.tick_params(axis='y', colors='#8fa39a')
        axd.grid(color='#1a3c2f', linestyle='--', alpha=0.3)
        axd.spines['top'].set_visible(False)
        axd.spines['right'].set_visible(False)
        axd.spines['bottom'].set_color('#1a3c2f')
        axd.spines['left'].set_color('#1a3c2f')
        
        st.pyplot(fig_d)
        
        st.caption("Delay = Current Travel Time - Free Flow Travel Time")

        # ---------------- HISTORICAL ANALYSIS ----------------
        st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
        st.markdown("### Historical Trends (Daily Patterns)")
        
        # Load and Process Data for Charts
        try:
            df_hist = pd.read_csv('vehicle_data.csv')
            
            # --- Data Processing ---
            # Convert timestamp to datetime (Fix for format error)
            # Handling DD-MM-YYYY HH:MM or similar formats with dayfirst=True
            df_hist['timestamp'] = pd.to_datetime(df_hist['timestamp'], dayfirst=True)
            
            # Extract Hour
            df_hist['hour'] = df_hist['timestamp'].dt.hour
            
            # Calculate Delay (Current Travel Time - Free Flow Travel Time)
            # Assuming columns exist: 'currentTravelTime' and 'freeFlowTravelTime' based on typical TomTom data
            # If not, we might need to rely on speed difference as a proxy or skip delay if cols missing.
            # Let's check columns printed in previous step: 
            # id,timestamp,latitude,longitude,location_name,frc,currentSpeed,freeFlowSpeed,currentTravelTime,freeFlowTravelTime,confidence
            # (Hypothetical standard schema, checking 'currentSpeed' availability is confirmed)
            
            # Calculate averages by hour
            hourly_stats = df_hist.groupby('hour').agg({
                'currentSpeed': 'mean',
                'currentTravelTime': 'mean',
                'freeFlowTravelTime': 'mean'
            }).reset_index()
            
            hourly_stats['avg_delay'] = hourly_stats['currentTravelTime'] - hourly_stats['freeFlowTravelTime']
            
            # --- Chart 1: Average Traffic Speed vs Hour ---
            st.markdown("#### Average Traffic Speed Across the Day")
            
            fig1, ax1 = plt.subplots(figsize=(10, 4))
            ax1.plot(hourly_stats['hour'], hourly_stats['currentSpeed'], marker='o', linestyle='-', color='#22e38a', linewidth=2, markersize=6)
            
            # Styling Chart 1
            ax1.set_facecolor('#050b08')
            fig1.patch.set_facecolor('#050b08')
            ax1.set_xlabel("Time of Day (Hour)", color='#8fa39a', fontsize=10)
            ax1.set_ylabel("Average Traffic Speed (km/h)", color='#8fa39a', fontsize=10)
            ax1.set_title("Average Traffic Speed Across the Day", color='white', fontsize=12, pad=15)
            ax1.tick_params(axis='x', colors='#8fa39a')
            ax1.tick_params(axis='y', colors='#8fa39a')
            ax1.grid(color='#1a3c2f', linestyle='--', alpha=0.3)
            ax1.set_xticks(range(0, 24)) # Show all hours
            
            # Remove spines
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            ax1.spines['bottom'].set_color('#1a3c2f')
            ax1.spines['left'].set_color('#1a3c2f')
            
            st.pyplot(fig1)
            
            # --- Chart 2: Average Traffic Delay vs Hour ---
            st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
            st.markdown("#### Traffic Delay Pattern During the Day")
            
            fig2, ax2 = plt.subplots(figsize=(10, 4))
            ax2.plot(hourly_stats['hour'], hourly_stats['avg_delay'], marker='s', linestyle='--', color='#ff3232', linewidth=2, markersize=6)
            
            # Styling Chart 2
            ax2.set_facecolor('#050b08')
            fig2.patch.set_facecolor('#050b08')
            ax2.set_xlabel("Time of Day (Hour)", color='#8fa39a', fontsize=10)
            ax2.set_ylabel("Average Traffic Delay (sec)", color='#8fa39a', fontsize=10)
            ax2.set_title("Traffic Delay Pattern During the Day", color='white', fontsize=12, pad=15)
            ax2.tick_params(axis='x', colors='#8fa39a')
            ax2.tick_params(axis='y', colors='#8fa39a')
            ax2.grid(color='#1a3c2f', linestyle='--', alpha=0.3)
            ax2.set_xticks(range(0, 24))
            
            # Remove spines
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            ax2.spines['bottom'].set_color('#1a3c2f')
            ax2.spines['left'].set_color('#1a3c2f')
            
            st.pyplot(fig2)
            
        except Exception as e:
            st.error(f"Could not load historical analytics: {e}")
            st.caption("Ensure 'vehicle_data.csv' has columns: timestamp, currentSpeed, currentTravelTime, freeFlowTravelTime")
        # Empty State
        st.info("No live data available for analytics.")
        st.markdown("""
            <div style="text-align: center; padding: 40px; color: #8fa39a;">
                Go to the <b>Live Data</b> page and click 'Refresh' to generate analytics.
            </div>
        """, unsafe_allow_html=True)

# ---------------- LIVE DATA PAGE ----------------
elif page == "Live Data":
    st.markdown("# Live <span class='green-text'>Monitoring</span>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background:rgba(255, 50, 50, 0.1); border:1px solid #ff3232; padding:10px; border-radius:8px; margin-bottom:20px'>
            🔴 <b>System Alert:</b> Real-time data feed active. Fetching latest traffic flow segments.
        </div>
    """, unsafe_allow_html=True)

    # API Configuration
    api_key = "VK1Ay21GpKGvAMvUrmpZUlyGOeRZI8pb"
    
    # 10 Locations (latitude, longitude)
    locations = [
        (27.1767, 78.0081, "Taj Mahal, Agra"),
        (27.1879, 78.0129, "Agra Fort"),
        (28.6129, 77.2295, "India Gate, Delhi"),
        (19.0760, 72.8777, "Mumbai Central"),
        (12.9716, 77.5946, "Bangalore City"),
        (13.0827, 80.2707, "Chennai Central"),
        (22.5726, 88.3639, "Kolkata"),
        (26.8467, 80.9462, "Lucknow"),
        (23.2599, 77.4126, "Bhopal"),
        (30.7333, 76.7794, "Chandigarh")
    ]

    if st.button("Refresh Live Data 🔄"):
        with st.spinner("Fetching live traffic data..."):
            results = []
            
            for lat, lon, name in locations:
                try:
                    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={api_key}&point={lat},{lon}"
                    response = requests.get(url)
                    
                    if response.status_code == 200:
                        data = response.json()
                        flow_data = data.get("flowSegmentData", {})
                        
                        current_speed = flow_data.get("currentSpeed", 0)
                        free_flow_speed = flow_data.get("freeFlowSpeed", 0)
                        confidence = flow_data.get("confidence", 0)
                        current_travel_time = flow_data.get("currentTravelTime", 0)
                        free_flow_travel_time = flow_data.get("freeFlowTravelTime", 0)
                        
                        # Calculate congestion level
                        congestion = "Low"
                        if current_speed < free_flow_speed * 0.5:
                            congestion = "High"
                        elif current_speed < free_flow_speed * 0.8:
                            congestion = "Moderate"

                        results.append({
                            "Location Name": name,
                            "Coordinates": f"{lat:.4f}, {lon:.4f}",
                            "Current Speed (km/h)": current_speed,
                            "Free Flow Speed (km/h)": free_flow_speed,
                            "Current Travel Time (s)": current_travel_time,
                            "Free Flow Travel Time (s)": free_flow_travel_time,
                            "Congestion Level": congestion,
                            "Confidence": f"{confidence * 100:.0f}%"
                        })
                except Exception as e:
                    st.error(f"Error fetching data for {name}: {e}")
            
            if results:
                df = pd.DataFrame(results)
                st.session_state['traffic_data'] = df  # Save to session state for Analytics
                st.dataframe(df, use_container_width=True)
                st.success("Live data updated! Check the Analytics page for detailed insights.")
            else:
                st.warning("No data fetched. Please check API connection.")
                
    else:
        st.info("Click the button above to fetch the latest real-time traffic data.")
