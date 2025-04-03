import pandas as pd
from faker import Faker
import random

# Initialize Faker to generate synthetic data
fake = Faker()

# Define the number of rows to generate
num_rows = 10

# Create synthetic data
data = {
    "Text": [fake.sentence() for _ in range(num_rows)],
    "Sentiment": random.choices(["Positive", "Neutral", "Negative"], k=num_rows),
    "Timestamp": [fake.date_time_this_decade().strftime("%m/%d/%Y %H:%M") for _ in range(num_rows)],
    "User": [fake.user_name() for _ in range(num_rows)],
    "Platform": random.choices(["Twitter", "Instagram", "Facebook", "YouTube"], k=num_rows),
    "Hashtags": [f"#{fake.word()} #{fake.word()}" for _ in range(num_rows)],
    "Retweets": [random.randint(0, 100) for _ in range(num_rows)],
    "Likes": [random.randint(0, 500) for _ in range(num_rows)],
    "Country": [fake.country_code() for _ in range(num_rows)],
    "Year": [random.randint(2000, 2025) for _ in range(num_rows)],
    "Month": [random.randint(1, 12) for _ in range(num_rows)],
    "Day": [random.randint(1, 28) for _ in range(num_rows)],
    "Hour": [random.randint(0, 23) for _ in range(num_rows)]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("synthetic_social_media_data.csv", index=False)

print(df.head())
