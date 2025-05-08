import pandas as pd
import numpy as np
from collections import Counter
import re

def analyze_topic_trends(data):
    """
    Analyze topic trends over time
    
    Parameters:
    data (pandas.DataFrame): DataFrame containing timestamp and topic columns
    
    Returns:
    pandas.DataFrame: DataFrame with topic counts grouped by date
    """
    # Convert timestamp to date
    data_copy = data.copy()
    data_copy['date'] = data_copy['timestamp'].dt.date
    
    # Group by date and topic, count occurrences
    topic_counts = data_copy.groupby(['date', 'topic']).size().reset_index(name='count')
    
    return topic_counts

def analyze_engagement_metrics(data):
    """
    Calculate engagement metrics by topic
    
    Parameters:
    data (pandas.DataFrame): DataFrame containing topic and engagement columns
    
    Returns:
    pandas.DataFrame: DataFrame with engagement metrics by topic
    """
    # Group by topic and calculate metrics
    topic_engagement = data.groupby('topic').agg(
        total_engagement=('engagement', 'sum'),
        avg_engagement=('engagement', 'mean'),
        max_engagement=('engagement', 'max'),
        post_count=('engagement', 'count')
    ).reset_index()
    
    # Round values for readability
    topic_engagement['avg_engagement'] = topic_engagement['avg_engagement'].round(2)
    topic_engagement['total_engagement'] = topic_engagement['total_engagement'].round(2)
    
    return topic_engagement

def get_most_frequent_terms(data, n=20):
    """
    Extract the most frequently used terms in post content
    
    Parameters:
    data (pandas.DataFrame): DataFrame containing content column
    n (int): Number of top terms to return
    
    Returns:
    pandas.DataFrame: DataFrame with term frequencies
    """
    # Combine all content
    all_content = ' '.join(data['content'].tolist()).lower()
    
    # Remove punctuation and split into words
    words = re.findall(r'\b\w+\b', all_content)
    
    # Filter out common stop words
    stop_words = set([
        'the', 'and', 'is', 'of', 'in', 'to', 'a', 'with', 'for', 'on', 
        'that', 'this', 'are', 'as', 'by', 'an', 'be', 'it', 'was', 'not',
        'but', 'or', 'at', 'from', 'they', 'we', 'you', 'i', 'have', 'has',
        'had', 'been', 'would', 'could', 'should', 'will', 'can', 'may'
    ])
    
    filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
    
    # Count word frequencies
    word_counts = Counter(filtered_words)
    
    # Get the most common words
    most_common = word_counts.most_common(n)
    
    # Convert to DataFrame
    terms_df = pd.DataFrame(most_common, columns=['term', 'frequency'])
    
    return terms_df