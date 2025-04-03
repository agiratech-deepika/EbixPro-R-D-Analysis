import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)

# Define the features
features = [
    'Post Time',
    'Day of the Week',
    'Hour of the Day',
    'Platform',
    'Post Type',
    'Text',
    'Hashtags',
    'Likes',
    'Comments',
    'Shares',
    'Views'
]

# Define the possible values for each feature
platforms = ['Instagram', 'Facebook', 'YouTube']
post_types = ['Photo', 'Video', 'Story']

# List of possible words for the text
words = [
    'I', 'love', 'to', 'travel', 'and', 'explore', 'new', 'places',
    'The', 'beauty', 'of', 'nature', 'is', 'breathtaking',
    'I', 'enjoy', 'taking', 'photos', 'and', 'vlogging', 'my', 'adventures',
    'Fashion', 'is', 'my', 'passion', 'I', 'love', 'to', 'stay', 'on', 'top',
    'of', 'the', 'latest', 'trends', 'and', 'styles'
]

# List of possible product names
product_names = [
    'iPhone 13',
    'Samsung Galaxy S22',
    'Google Pixel 6',
    'Apple Watch',
    'Nike Air Max',
    'Adidas Superstar',
    'Loreal Makeup',
    'Maybelline Cosmetics',
    'Dior Fragrance',
    'Hermes Handbag',
    'Gucci Shoes'
]

# Generate synthetic data
data = []
start_date = datetime(2020, 1, 1)
end_date = datetime(2024, 12, 31)

for i in range(10000):
    post_time = start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days))
    day_of_week = post_time.strftime('%A')
    hour_of_day = post_time.hour
    platform = random.choice(platforms)
    post_type = random.choice(post_types)
    
    # Generate text
    num_sentences = np.random.randint(1, 3)
    text = ''
    for _ in range(num_sentences):
        num_words = np.random.randint(10, 20)
        sentence = ' '.join(random.choice(words) for _ in range(num_words))
        text += sentence + '. '
    
    # Add a product name to the text
    if np.random.random() < 0.5:
        text += 'I recently bought ' + random.choice(product_names) + ' and I\'m loving it!'
    
    # Generate hashtags
    num_hashtags = np.random.randint(1, 5)
    hashtags = []
    for _ in range(num_hashtags):
        hashtag = '#' + random.choice(words).lower()
        hashtags.append(hashtag)
    hashtags = ', '.join(hashtags)
    
    likes = np.random.randint(0, 1000)
    comments = np.random.randint(0, 100)
    shares = np.random.randint(0, 50)
    views = np.random.randint(0, 5000)
    
    data.append([
        post_time,
        day_of_week,
        hour_of_day,
        platform,
        post_type,
        text,
        hashtags,
        likes,
        comments,
        shares,
        views
    ])

# Create a pandas DataFrame
df = pd.DataFrame(data, columns=features)

# Print the first few rows of the DataFrame
print(df.head())

# Save the DataFrame to a CSV file
df.to_csv('synthetic_data.csv', index=False)

import re

def extract_hashtags(text):
    hashtags = re.findall(r'#\w+', text)
    return hashtags

df['Extracted Hashtags'] = df['Text'].apply(extract_hashtags)