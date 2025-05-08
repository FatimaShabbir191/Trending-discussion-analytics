import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Define a list of topics that might be trending
TOPICS = [
    "Artificial Intelligence", 
    "Sustainability", 
    "Cryptocurrency", 
    "Space Exploration", 
    "Health Tech",
    "Remote Work", 
    "Climate Change", 
    "Electric Vehicles", 
    "Quantum Computing", 
    "Robotics",
    "Augmented Reality", 
    "Cybersecurity", 
    "Blockchain", 
    "5G Technology", 
    "Renewable Energy"
]

# Define words commonly used in discussions about these topics
TOPIC_WORDS = {
    "Artificial Intelligence": ["machine learning", "neural networks", "deep learning", "algorithms", "data", "models", "automation", "predictive", "intelligence", "GPT", "AI ethics"],
    "Sustainability": ["environment", "green", "recycling", "carbon footprint", "renewable", "eco-friendly", "conservation", "biodegradable", "sustainable", "climate"],
    "Cryptocurrency": ["bitcoin", "ethereum", "blockchain", "wallet", "mining", "token", "decentralized", "exchange", "investment", "defi", "nft"],
    "Space Exploration": ["mars", "rocket", "nasa", "spacecraft", "galaxy", "orbit", "astronaut", "satellite", "mission", "lunar", "spacex", "telescope"],
    "Health Tech": ["telehealth", "wearables", "medical devices", "healthcare", "patient", "diagnosis", "monitoring", "wellness", "digital health", "biotechnology"],
    "Remote Work": ["virtual", "zoom", "wfh", "productivity", "collaboration", "distributed", "flexible", "home office", "hybrid", "teams", "communication"],
    "Climate Change": ["global warming", "emissions", "temperature", "sea level", "greenhouse gas", "carbon", "pollution", "weather", "environmental", "fossil fuels"],
    "Electric Vehicles": ["tesla", "charging", "battery", "range", "ev", "autonomous", "sustainable", "emissions", "motors", "clean energy", "transportation"],
    "Quantum Computing": ["qubit", "quantum", "superposition", "computation", "encryption", "simulator", "physics", "algorithm", "processor", "entanglement"],
    "Robotics": ["automation", "robot", "ai", "mechanical", "sensors", "programming", "engineering", "motion", "manufacturing", "drones", "precision"],
    "Augmented Reality": ["ar", "vr", "mixed reality", "immersive", "headset", "visualization", "experience", "overlay", "virtual", "3d", "interactive"],
    "Cybersecurity": ["hacking", "firewall", "encryption", "threat", "security", "data breach", "protection", "vulnerability", "malware", "authentication", "privacy"],
    "Blockchain": ["ledger", "decentralized", "cryptocurrency", "bitcoin", "smart contracts", "transactions", "secure", "distributed", "tokens", "validation"],
    "5G Technology": ["bandwidth", "network", "wireless", "connectivity", "speed", "latency", "telecommunications", "mobile", "infrastructure", "data", "iot"],
    "Renewable Energy": ["solar", "wind", "sustainable", "grid", "power", "green", "carbon", "clean energy", "battery", "climate", "efficiency"]
}

def generate_content(topic):
    """Generate random content for a post based on the topic"""
    # Get words relevant to the topic
    topic_related_words = TOPIC_WORDS.get(topic, ["discussion", "trending", "topic"])
    
    # Generate a random sentence length
    sentence_length = random.randint(8, 20)
    
    # Create a sentence with some topic-related words and some common words
    common_words = ["the", "and", "is", "of", "in", "to", "a", "with", "for", "on", "that", "this", "are", "as", "by"]
    
    # Choose words for the sentence
    words = []
    for _ in range(sentence_length):
        if random.random() < 0.4:  # 40% chance to pick a topic-related word
            words.append(random.choice(topic_related_words))
        else:
            words.append(random.choice(common_words))
    
    # Ensure at least one topic word is included
    if not any(word in topic_related_words for word in words):
        words[random.randint(0, len(words)-1)] = random.choice(topic_related_words)
    
    # Create the sentence with first letter capitalized and a period at the end
    sentence = " ".join(words)
    sentence = sentence[0].upper() + sentence[1:] + "."
    
    return sentence

def generate_timestamp(start_date, end_date):
    """Generate a random timestamp between start_date and end_date"""
    time_diff = end_date - start_date
    random_seconds = random.randint(0, int(time_diff.total_seconds()))
    return start_date + timedelta(seconds=random_seconds)

def generate_engagement():
    """Generate random engagement metrics (likes, shares, comments)"""
    # Using a right-skewed distribution to simulate reality where most posts get low engagement
    return np.random.lognormal(mean=2, sigma=1.2)

def generate_mock_data(num_posts=1000, start_date=None, end_date=None):
    """
    Generate mock data for trending topics discussions
    
    Parameters:
    num_posts (int): Number of posts to generate
    start_date (datetime): Start date for the time range (default: 30 days ago)
    end_date (datetime): End date for the time range (default: now)
    
    Returns:
    pandas.DataFrame: DataFrame with the generated data
    """
    if start_date is None:
        start_date = datetime.now() - timedelta(days=30)
    if end_date is None:
        end_date = datetime.now()
    
    # Initialize empty lists to store the data
    timestamps = []
    topics = []
    contents = []
    engagements = []
    
    # Generate data for each post
    for _ in range(num_posts):
        # Randomly select a topic (with weighted probabilities for some trending topics)
        topic_weights = [1.5 if i < 3 else 1.0 for i in range(len(TOPICS))]  # First 3 topics are more trending
        topic = random.choices(TOPICS, weights=topic_weights, k=1)[0]
        
        # Generate a timestamp, content, and engagement metrics
        timestamp = generate_timestamp(start_date, end_date)
        content = generate_content(topic)
        engagement = generate_engagement()
        
        # Append to lists
        timestamps.append(timestamp)
        topics.append(topic)
        contents.append(content)
        engagements.append(round(engagement, 2))  # Round to 2 decimal places
    
    # Create DataFrame
    data = {
        'timestamp': timestamps,
        'topic': topics,
        'content': contents,
        'engagement': engagements
    }
    
    df = pd.DataFrame(data)
    
    # Sort by timestamp
    df = df.sort_values('timestamp').reset_index(drop=True)
    
    return df