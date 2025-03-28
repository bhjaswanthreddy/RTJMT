import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Cloud Architect Job Market Analysis",
    page_icon="📊",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    h1, h2, h3 { color: #333; text-align: center; }
    .stButton>button { background-color: #4CAF50; color: red; border-radius: 10px; font-size: 16px; padding: 10px; }
    .stButton>button:hover { background-color: #45a049; }
    </style>
""", unsafe_allow_html=True)

# Load dataset function
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

file_path = r"C:\\Users\\bhima\\Downloads\\expanded_cloud_architect_jobs.csv"
df = load_data(file_path)

# Convert 'Date_Posted' to datetime
df['Date_Posted'] = pd.to_datetime(df['Date_Posted'])

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📊 Salary Analysis", "📌 Skill Analysis", "📅 Trends Analysis", "ℹ️ About"])

# Home Page
if page == "🏠 Home":
    st.markdown("<h1>🌟 Cloud Architect Job Market Analysis</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Jobs", df.shape[0])
    col2.metric("Avg Salary (USD)", f"${df['Salary_USD'].mean():,.2f}")
    col3.metric("Top Location", df['Location'].mode()[0])

# Salary Analysis Page
elif page == "📊 Salary Analysis":
    st.markdown("<h1>📊 Salary Analysis</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        location_filter = st.selectbox("🌍 Select Location", df["Location"].unique())
    with col2:
        experience_filter = st.selectbox("🔹 Select Experience Level", df["Experience_Level"].unique())
    
    filtered_df = df[(df["Location"] == location_filter) & (df["Experience_Level"] == experience_filter)]
    st.write(f"Showing results for **{location_filter}** and **{experience_filter}**:")
    st.dataframe(filtered_df)

    # Salary Distribution Chart
    st.markdown("### 📍 Average Salary by Location")
    salary_by_location = df.groupby("Location")["Salary_USD"].mean().sort_values(ascending=False).head(10)
    fig = px.bar(salary_by_location, x=salary_by_location.index, y=salary_by_location.values, 
                 title="Top 10 Locations by Salary", color=salary_by_location.values, 
                 labels={"x": "Location", "y": "Average Salary (USD)"}, color_continuous_scale="blues")
    st.plotly_chart(fig, use_container_width=True)

# Skill Analysis Page
elif page == "📌 Skill Analysis":
    st.markdown("<h1>📌 Skill Analysis</h1>", unsafe_allow_html=True)
    st.markdown("### 🔥 Top 10 Most In-Demand Skills")
    skills = df["Skills"].str.split(", ").explode()
    skill_counts = skills.value_counts().head(10)
    
    fig2 = px.bar(skill_counts, x=skill_counts.index, y=skill_counts.values, 
                  title="Most Required Skills", color=skill_counts.values, 
                  labels={"x": "Skills", "y": "Count"}, color_continuous_scale="viridis")
    st.plotly_chart(fig2, use_container_width=True)

# Trends Analysis Page
elif page == "📅 Trends Analysis":
    st.markdown("<h1>📅 Trends Analysis</h1>", unsafe_allow_html=True)

    # Date Range Selector
    date_range = st.slider("Select Date Range", 
                           min_value=df['Date_Posted'].min().date(), 
                           max_value=df['Date_Posted'].max().date(), 
                           value=(df['Date_Posted'].min().date(), df['Date_Posted'].max().date()))

    # Filter Data by Selected Date Range
    filtered_trends = df[(df['Date_Posted'].dt.date >= date_range[0]) & (df['Date_Posted'].dt.date <= date_range[1])]

    # Ensure Data is Sorted by Date for Rolling Average
    filtered_trends = filtered_trends.sort_values(by="Date_Posted")

    # Calculate 7-Day Moving Average for Salary
    filtered_trends["Rolling_Avg"] = filtered_trends["Salary_USD"].rolling(window=7).mean().dropna()

    # Plot Smoothed Salary Trends
    fig = px.line(filtered_trends, x="Date_Posted", y="Rolling_Avg",
                  title="Smoothed Salary Trends (7-Day Moving Avg)", markers=True,
                  labels={"Date_Posted": "Date", "Rolling_Avg": "7-Day Avg Salary (USD)"},
                  color_discrete_sequence=["#FF5733"])
    
    st.plotly_chart(fig, use_container_width=True)


# About Page
elif page == "ℹ️ About":
    st.markdown("<h1>ℹ️ About This Project</h1>", unsafe_allow_html=True)
    st.write("""
        **Cloud Architect Job Market Analysis** is an interactive dashboard that helps users explore job market trends,  
        salary expectations, and skill demands for Cloud Architect roles globally.

        **🔹 Built With:**  
        - 🏗️ **Streamlit** for front-end  
        - 📊 **Plotly** for interactive visualizations  
        - 🗃 **Pandas** for data handling  
    """)

    st.markdown("""
        ---
        **💡 Developed by:** Bhargav Ram Buska  
        📂 [GitHub Repository](#) | 🔗 [LinkedIn](#)
    """)