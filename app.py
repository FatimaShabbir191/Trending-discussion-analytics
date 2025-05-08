import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import time

from data_generator import generate_mock_data
from data_analyzer import analyze_topic_trends, analyze_engagement_metrics, get_most_frequent_terms

# Set page config
st.set_page_config(
    page_title="Trending Topics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Initialize session state for data generation
if 'data' not in st.session_state:
    st.session_state.data = generate_mock_data(
        num_posts=1000,
        start_date=datetime.now() - timedelta(days=30),
        end_date=datetime.now()
    )
    st.session_state.last_update = datetime.now()

# Function to update data periodically (every 60 seconds)
def update_data():
    if datetime.now() - st.session_state.last_update > timedelta(seconds=60):
        # Add some new data (simulate new posts)
        new_data = generate_mock_data(
            num_posts=50,  
            start_date=datetime.now() - timedelta(days=3),
            end_date=datetime.now()
        )
        st.session_state.data = pd.concat([st.session_state.data, new_data]).reset_index(drop=True)
        st.session_state.last_update = datetime.now()
        return True
    return False

# Dashboard title and description
st.title("Trending Topics Analytics Dashboard")
st.markdown("This dashboard tracks and visualizes trending topics based on generated data.")

# Data update indicator
with st.sidebar:
    st.subheader("Dashboard Controls")
    st.write(f"Last data update: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if st.button("Update Data Now"):
        new_data = generate_mock_data(
            num_posts=100,
            start_date=datetime.now() - timedelta(days=3),
            end_date=datetime.now()
        )
        st.session_state.data = pd.concat([st.session_state.data, new_data]).reset_index(drop=True)
        st.session_state.last_update = datetime.now()
        st.success("Data updated!")
    
    # Time period filter
    st.subheader("Filter Data")
    time_period = st.selectbox(
        "Select Time Period",
        ["Last 24 hours", "Last 7 days", "Last 30 days", "All data"]
    )
    
    # Filter by topic
    all_topics = st.session_state.data['topic'].unique().tolist()
    selected_topics = st.multiselect(
        "Filter by Topics",
        options=all_topics,
        default=all_topics[:5] if len(all_topics) > 5 else all_topics
    )

# Filter data based on selected criteria
filtered_data = st.session_state.data.copy()

# Apply time filter
now = datetime.now()
if time_period == "Last 24 hours":
    filtered_data = filtered_data[filtered_data['timestamp'] >= now - timedelta(days=1)]
elif time_period == "Last 7 days":
    filtered_data = filtered_data[filtered_data['timestamp'] >= now - timedelta(days=7)]
elif time_period == "Last 30 days":
    filtered_data = filtered_data[filtered_data['timestamp'] >= now - timedelta(days=30)]

# Apply topic filter
if selected_topics:
    filtered_data = filtered_data[filtered_data['topic'].isin(selected_topics)]

# Display some stats in metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Posts", len(filtered_data))
with col2:
    st.metric("Unique Topics", filtered_data['topic'].nunique())
with col3:
    st.metric("Avg. Engagement", round(filtered_data['engagement'].mean(), 2))

# Analyze and visualize the data
if not filtered_data.empty:
    # 1. Topic Trends Over Time visualization
    st.subheader("Topic Trends Over Time")
    topic_trends = analyze_topic_trends(filtered_data)
    
    fig = px.line(
        topic_trends, 
        x='date', 
        y='count', 
        color='topic',
        title="Post Frequency by Topic Over Time",
        labels={'date': 'Date', 'count': 'Number of Posts', 'topic': 'Topic'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 2. Engagement Metrics by Topic
    st.subheader("Engagement Metrics by Topic")
    
    # Split into two columns for visualizations
    col1, col2 = st.columns(2)
    
    engagement_metrics = analyze_engagement_metrics(filtered_data)
    
    with col1:
        # Bar chart for average engagement
        fig_bar = px.bar(
            engagement_metrics.sort_values('avg_engagement', ascending=False), 
            x='topic', 
            y='avg_engagement',
            title="Average Engagement by Topic",
            labels={'topic': 'Topic', 'avg_engagement': 'Average Engagement'},
            color='avg_engagement',
            color_continuous_scale=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Top topics by total engagement
        fig_pie = px.pie(
            engagement_metrics.sort_values('total_engagement', ascending=False).head(8), 
            values='total_engagement', 
            names='topic',
            title="Total Engagement Distribution (Top 8)",
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # 3. Most Frequent Terms
    st.subheader("Most Frequent Terms in Discussions")
    frequent_terms = get_most_frequent_terms(filtered_data)
    
    if not frequent_terms.empty:
        fig_terms = px.bar(
            frequent_terms.sort_values('frequency', ascending=True).tail(15), 
            y='term', 
            x='frequency',
            title="Most Frequently Used Terms",
            labels={'term': 'Term', 'frequency': 'Frequency'},
            orientation='h',
            color='frequency',
            color_continuous_scale=px.colors.sequential.Plasma
        )
        st.plotly_chart(fig_terms, use_container_width=True)
    
    # 4. Raw Data Table (with pagination)
    st.subheader("Raw Data Sample")
    st.dataframe(
        filtered_data.sort_values('timestamp', ascending=False)
        .head(100)[['timestamp', 'topic', 'content', 'engagement']]
    )
else:
    st.warning("No data available for the selected filters. Please adjust your filter criteria.")

# Check for data updates in the background
if update_data():
    st.rerun()

# Footer
st.markdown("---")
st.caption("Analytics Dashboard - Data updates automatically every minute")