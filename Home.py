import streamlit as st

st.markdown("""
<div style="text-align:center; margin-top:60px">
    <div class="h-title">VISION <span class="green">TRAFFIC</span></div>
    <p style="opacity:0.7">Real-Time Traffic Analysis & Prediction System</p>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns([1,1])
with c1:
    st.button("Start Predicting ⚡")
with c2:
    st.button("View Analytics")

st.markdown("## Powerful Features")

cols = st.columns(4)
features = [
    ("Real-Time Data Ingestion", "Live traffic data streaming"),
    ("ML Traffic Prediction", "AI based congestion forecast"),
    ("Smart Analytics", "Interactive dashboards"),
    ("Power BI Integration", "Enterprise BI support")
]

for col, feat in zip(cols, features):
    with col:
        st.markdown(f"""
        <div class="glass">
            <h4>{feat[0]}</h4>
            <p style="opacity:0.7">{feat[1]}</p>
        </div>
        """, unsafe_allow_html=True)
