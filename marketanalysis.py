import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from prophet import Prophet
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import networkx as nx
from io import BytesIO
from fpdf import FPDF
import numpy as np
from sklearn.linear_model import LinearRegression

# Set page config with favicon
st.set_page_config(
    page_title="Cloud Architect Job Market Analysis",
    page_icon="https://cdn-icons-png.flaticon.com/512/1828/1828961.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional UI 
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    .stApp { 
        background: linear-gradient(to bottom right, #d9e2ec, #b0c4de); /* Slightly darker gradient for better contrast */
        font-family: 'Roboto', sans-serif; 
    }
    h1, h2, h3 { 
        color: #1a3c5e; 
        font-weight: 700; 
    }
    h1 { font-size: 32px; margin-bottom: 0; }
    h2 { font-size: 24px; }
    p, .stMarkdown, .stMetric, .stPlotlyChart { 
        color: #2f4f4f; /* Darker text for better readability */
        padding: 10px 0; /* Add padding to elements for spacing */
    }
    .header {
        position: fixed;
        top: 0;
        width: 100%;
        background: #1a3c5e;
        color: white;
        padding: 15px 20px;
        z-index: 1000;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .header img { vertical-align: middle; margin-right: 10px; }
    .main-content {
        padding-top: 70px; /* Adjust this value based on the header height */
    }
    .stButton>button {
        background: linear-gradient(90deg, #4CAF50, #66BB6A);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #45a049, #5cb85c);
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    [data-testid='stSidebar'] { 
        background: #f8fafc; 
        border-right: 1px solid #e0e7ff; 
    }
    .dark-mode .stApp { 
        background: linear-gradient(to bottom right, #1e293b, #334155); 
        color: #e2e8f0; 
    }
    .dark-mode h1, .dark-mode h2, .dark-mode h3 { color: #dbeafe; }
    .dark-mode p, .dark-mode .stMarkdown, .dark-mode .stMetric, .dark-mode .stPlotlyChart { 
        color: #e2e8f0; 
    }
    .dark-mode [data-testid='stSidebar'] { background: #1e293b; }
    @media (max-width: 600px) {
        h1 { font-size: 24px; }
        .main-content { padding-top: 60px; }
        p, .stMarkdown, .stMetric, .stPlotlyChart { padding: 5px 0; }
    }
    </style>
""", unsafe_allow_html=True)

# Dark Mode Toggle
dark_mode = st.sidebar.checkbox("🌙 Dark Mode", value=False)
if dark_mode:
    st.markdown('<body class="dark-mode">', unsafe_allow_html=True)

# Custom Header
st.markdown("""
    <div class="header">
        <img src="https://cdn-icons-png.flaticon.com/512/1828/1828961.png" width="30">
        <span>Cloud Architect Job Market Analysis</span>
    </div>
""", unsafe_allow_html=True)

# Wrap all content in a div with padding to avoid overlap with the fixed header
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Load dataset
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    df['Date_Posted'] = pd.to_datetime(df['Date_Posted'], errors='coerce')
    # Standardize Skills column for consistent splitting
    df['Skills'] = df['Skills'].str.replace(', ', ',').str.replace(',', ', ')
    return df

file_path = r"C:\\Users\\bhima\\Downloads\\expanded_cloud_architect_jobs.csv"
df = load_data(file_path)

# Sidebar Navigation with Icons
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", [
    "🏠 Home", 
    "📊 Salary Analysis", 
    "📌 Skill Analysis", 
    "📅 Trends Analysis", 
    "🚀 Career Simulator", 
    "ℹ️ About"
])

# Home Page
if page == "🏠 Home":
    st.markdown("<h2>Charting the Cloud: Job Market Mastery</h2>", unsafe_allow_html=True,)
    st.markdown("<p style='text-align:center; color:#64748b;'>Explore trends and insights for Cloud Architect careers.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Jobs", df.shape[0])
    with col2:
        st.metric("Avg Salary (USD)", f"${df['Salary_USD'].mean():,.2f}")
    with col3:
        st.metric("Top Location", df['Location'].mode()[0])
    
    exp_counts = df["Experience_Level"].value_counts().reset_index()
    exp_counts.columns = ["Experience", "Count"]  # Rename for clarity
    fig = px.pie(exp_counts, values="Count", names="Experience", 
                 title="Jobs by Experience Level", 
                 color_discrete_sequence=["#4CAF50", "#66BB6A", "#A5D6A7"])
    st.plotly_chart(fig, use_container_width=True)

# Salary Analysis Page
elif page == "📊 Salary Analysis":
    st.markdown("<h2>Salary Analysis</h2>", unsafe_allow_html=True)
    
    with st.expander("🔍 Filter Options", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            location_filter = st.multiselect("🌍 Locations", df["Location"].unique(), default=[df["Location"].mode()[0]], help="Select one or more locations")
        with col2:
            experience_filter = st.multiselect("🔹 Experience", df["Experience_Level"].unique(), default=[df["Experience_Level"].mode()[0]], help="Filter by experience level")
        with col3:
            salary_range = st.slider("💰 Salary Range (USD)", int(df["Salary_USD"].min()), int(df["Salary_USD"].max()), 
                                    (int(df["Salary_USD"].min()), int(df["Salary_USD"].max())), help="Set salary range")
    
    filtered_df = df[df["Location"].isin(location_filter) & 
                     df["Experience_Level"].isin(experience_filter) & 
                     (df["Salary_USD"] >= salary_range[0]) & (df["Salary_USD"] <= salary_range[1])]
    
    st.write(f"Showing {len(filtered_df)} jobs matching your filters:")
    with st.expander("View Filtered Data"):
        st.dataframe(filtered_df)
    csv = filtered_df.to_csv(index=False)
    st.download_button("📥 Download CSV", csv, "cloud_architect_data.csv", "text/csv")
    
    st.markdown("### 🌍 Average Salary by Location")
    salary_by_location = filtered_df.groupby("Location")["Salary_USD"].mean().reset_index()
    fig = px.bar(salary_by_location, x="Location", y="Salary_USD", 
                 title="Average Salary by Location", 
                 color="Salary_USD", color_continuous_scale="Blues",
                 labels={"Salary_USD": "Average Salary (USD)"})
    fig.update_layout(xaxis={'tickangle': 45})
    st.plotly_chart(fig, use_container_width=True)

# Skill Analysis Page
elif page == "📌 Skill Analysis":
    st.markdown("<h2>Skill Analysis</h2>", unsafe_allow_html=True)
    skills = df["Skills"].str.split(", ").explode()
    
    st.markdown("### 🔥 Top 10 Most In-Demand Skills")
    skill_counts = skills.value_counts().head(10)
    fig2 = px.bar(skill_counts, x=skill_counts.index, y=skill_counts.values, 
                  title="Most Required Skills", color=skill_counts.values, 
                  labels={"x": "Skills", "y": "Count"}, color_continuous_scale="Greens")
    fig2.update_traces(marker=dict(color="#4CAF50"))
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("### 🌐 Skills Word Cloud")
    wordcloud = WordCloud(width=800, height=400, background_color="white", colormap="Greens").generate(" ".join(skills))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)

# Trends Analysis Page
elif page == "📅 Trends Analysis":
    st.markdown("<h2>Trends Analysis</h2>", unsafe_allow_html=True)
    
    date_range = st.slider("📅 Select Date Range", min_value=df['Date_Posted'].min().date(), 
                           max_value=df['Date_Posted'].max().date(), 
                           value=(df['Date_Posted'].min().date(), df['Date_Posted'].max().date()))
    filtered_trends = df[(df['Date_Posted'].dt.date >= date_range[0]) & 
                         (df['Date_Posted'].dt.date <= date_range[1])].sort_values("Date_Posted")
    filtered_trends["Rolling_Avg"] = filtered_trends["Salary_USD"].rolling(window=7).mean()
    
    if st.checkbox("🔮 Show Salary Forecast"):
        prophet_df = filtered_trends[["Date_Posted", "Salary_USD"]].rename(columns={"Date_Posted": "ds", "Salary_USD": "y"}).dropna()
        model = Prophet(yearly_seasonality=True)
        model.fit(prophet_df)
        future = model.make_future_dataframe(periods=90)
        forecast = model.predict(future)
        fig = px.line(forecast, x="ds", y="yhat", title="Salary Forecast", 
                      labels={"ds": "Date", "yhat": "Predicted Salary (USD)"}, 
                      color_discrete_sequence=["#FF5733"])
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = px.line(filtered_trends, x="Date_Posted", y="Rolling_Avg", 
                      title="Smoothed Salary Trends", markers=True,
                      labels={"Date_Posted": "Date", "Rolling_Avg": "Avg Salary (USD)"}, 
                      color_discrete_sequence=["#4CAF50"])
        st.plotly_chart(fig, use_container_width=True)

# Career Simulator Page
elif page == "🚀 Career Simulator":
    st.markdown("<h2>Career Simulator</h2>", unsafe_allow_html=True)
    
    user_skills = st.multiselect("🛠️ Select Your Skills", df["Skills"].str.split(", ").explode().unique(), help="Choose your current skills")
    user_experience = st.selectbox("🔹 Experience Level", df["Experience_Level"].unique())
    user_location = st.selectbox("🌍 Location", df["Location"].unique())
    
    sim_df = df[(df["Experience_Level"] == user_experience) & (df["Location"] == user_location)]
    avg_salary = sim_df["Salary_USD"].mean()
    missing_skills = set(df["Skills"].str.split(", ").explode().value_counts().index[:5]) - set(user_skills)
    
    st.write(f"Estimated Salary: **${avg_salary:,.2f} USD**")
    if missing_skills:
        st.write("Skills to Learn for Higher Pay:", ", ".join(missing_skills))

# About Page
elif page == "ℹ️ About":
    st.markdown("<h2>About This Project</h2>", unsafe_allow_html=True)
    st.write("""
        **Cloud Architect Job Market Analysis** is a professional dashboard for exploring job trends, salaries, and skills.
        Built with Streamlit, Plotly, and advanced analytics tools.
        Developed by Bhargav Ram Buska.
    """)

# Close the main-content div
st.markdown('</div>', unsafe_allow_html=True)