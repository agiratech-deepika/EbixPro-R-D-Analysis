# Description: This script trains a PPO model to predict bundle discounts based on historical data.
# The model is trained using the Stable Baselines library and the custom Gym environment.
# The trained model is saved and used to predict discounts on new data. 
"""
🚀 Bundle Discount Enhancement using Reinforcement Learning (PPO)

🔹 This script optimizes bundle discount predictions for products using 
   reinforcement learning (PPO) from Stable-Baselines3.

🛠 Steps:
1️⃣ Load & preprocess dataset (normalize, encode categorical features, scale numeric data).
2️⃣ Define a Custom Gym Environment for training AI in a discount simulation.
3️⃣ Train a PPO (Proximal Policy Optimization) model to predict optimal discounts.
4️⃣ Test the trained model with a random sample.

🎯 Output: The model suggests an optimized discount percentage.
"""

"""
📌 Sample Data Columns (for reference):

| seller_id | product_id | product_name | category   | bundle_id | bundle_type  | quantity_threshold | price_per_unit | stock_availability | seasonality | competitor_price | customer_demand | historical_discount |
|-----------|-----------|--------------|------------|-----------|--------------|---------------------|----------------|--------------------|-------------|-----------------|----------------|---------------------|
| S10       | P001      | Laptop       | Electronics| B41       | Office Setup | 3                   | 839.8          | 15                 | Medium      | 885.48          | 266            | 5                   |

🔹 This dataset is used for bundle discount predictions.
🔹 Numerical values are scaled between 0 and 1 for Reinforcement Learning.
🔹 Categorical values (like seller_id, bundle_type) are encoded as numbers.

"""
# The main reinforcement learning algorithm used for training is PPO (Proximal Policy Optimization) from Stable-Baselines3.

# The other algorithms are only used for preprocessing the dataset, ensuring it's suitable for training.

# Preprocessing (Before Training the Model)

# Label Encoding (LabelEncoder) → Converts categorical columns (seller_id, product_id, etc.) into numerical format.

# Min-Max Scaling (MinMaxScaler) → Normalizes numerical columns to a range between 0 and 1 for better training stability.


import pandas as pd
import numpy as np
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from gymnasium import spaces
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# Load dataset
df = pd.read_csv(r"C:\\Projects\\EbixPro_AI_bot\\Analysis\\Discount Management\\BUNDLE DISCOUNT\\Dataset\\final_bundle_discount_dataset.csv")

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# Ensure necessary columns exist
required_cols = {"seller_id", "product_id", "bundle_id", "seasonality", "product_name", "category", "bundle_type", "historical_discount"}
missing_cols = required_cols - set(df.columns)
if missing_cols:
    raise KeyError(f"❌ Missing columns in dataset: {missing_cols}")

# Compute 'suggested_discount' if missing
if "suggested_discount" not in df.columns:
    df["suggested_discount"] = df["historical_discount"] * 0.9  # Example logic

# Encode categorical features
categorical_cols = ["seller_id", "product_id", "bundle_id", "seasonality", "product_name", "category", "bundle_type"]
label_encoders = {col: LabelEncoder().fit(df[col]) for col in categorical_cols}
for col, encoder in label_encoders.items():
    df[col] = encoder.transform(df[col])

# Ensure all columns are numeric
non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
if non_numeric_cols:
    raise ValueError(f"❌ Non-numeric columns detected even after encoding: {non_numeric_cols}")

# Identify numerical columns & scale
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
num_cols.remove("suggested_discount")  # Exclude target column
scaler = MinMaxScaler()
df[num_cols] = scaler.fit_transform(df[num_cols])

# Drop NaN and infinite values
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)

# Define Custom Gym Environment
class BundleDiscountEnv(gym.Env):
    def __init__(self, data):
        super(BundleDiscountEnv, self).__init__()
        self.data = data
        self.current_index = 0
        self.observation_space = spaces.Box(low=0, high=1, shape=(len(data.columns) - 1,), dtype=np.float32)
        self.action_space = spaces.Box(low=0, high=50, shape=(1,), dtype=np.float32)

    def reset(self, seed=None, options=None):
        self.current_index = 0
        return self.data.iloc[self.current_index, :-1].values.astype(np.float32), {}

    def step(self, action):
        row = self.data.iloc[self.current_index]
        actual_discount = row["suggested_discount"]
        
        if actual_discount == 0 or np.isnan(actual_discount):
            reward = -np.abs(action[0])
        else:
            reward = -np.abs(action[0] - actual_discount) / (actual_discount + 1e-5)

        self.current_index += 1
        done = self.current_index >= len(self.data)
        next_state = self.data.iloc[self.current_index, :-1].values.astype(np.float32) if not done else np.zeros(self.observation_space.shape)

        return next_state, reward, done, {}, {}

# Create environment
env = DummyVecEnv([lambda: BundleDiscountEnv(df)])

# Define PPO Hyperparameters
ppo_params = {
    "learning_rate": 0.0003,  
    "n_steps": 2048,
    "batch_size": 64,
    "n_epochs": 10,
    "gamma": 0.99,
    "gae_lambda": 0.95,
    "clip_range": 0.2,
    "ent_coef": 0.01,
    "vf_coef": 0.5,
    "max_grad_norm": 0.5
}

# Train PPO Model
model = PPO("MlpPolicy", env, verbose=1, **ppo_params)
model.learn(total_timesteps=50000)

# Save trained model
model.save("ppo_bundle_discount_enhancement")
print("🎯 Model training completed and saved!")

# Test prediction
test_sample = df.sample(1).drop(columns=["suggested_discount"]).values.astype(np.float32)
predicted_discount, _ = model.predict(test_sample, deterministic=True)
print(f"🎯 Predicted Discount: {float(predicted_discount[0][0]):.2f}%")

