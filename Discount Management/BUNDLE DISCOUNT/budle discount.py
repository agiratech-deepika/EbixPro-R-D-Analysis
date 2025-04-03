# import pandas as pd
# import numpy as np
# import gym
# from stable_baselines3 import PPO
# from stable_baselines3.common.vec_env import DummyVecEnv
# from gym import spaces
# import random

# # Load dataset
# df = pd.read_csv(r"C:\\Projects\\EbixPro_AI_bot\\Analysis\\Discount Management\\BUNDLE DISCOUNT\\Dataset\\final_bundle_discount_dataset.csv")

# # Check dataset structure
# print(df.head())

# # Encode categorical columns (Product Name, Category, Bundle Type)
# from sklearn.preprocessing import LabelEncoder

# label_encoders = {}
# categorical_cols = ["product_name", "category", "bundle_type"]

# for col in categorical_cols:
#     label_encoders[col] = LabelEncoder()
#     df[col] = label_encoders[col].fit_transform(df[col])

# # Define state & action spaces
# class BundleDiscountEnv(gym.Env):
#     def __init__(self, data):
#         super(BundleDiscountEnv, self).__init__()
        
#         self.data = data
#         self.current_index = 0
        
#         # State space (features used for discount prediction)
#         self.observation_space = spaces.Box(
#             low=0, high=1, shape=(len(data.columns) - 1,), dtype=np.float32
#         )
        
#         # Action space (discount range 0% to 50%)
#         self.action_space = spaces.Discrete(51)  # 0% to 50% in steps of 1%

#     def reset(self):
#         self.preprocess_data()  # Ensure encoding before use
#         return self.data.iloc[self.current_index, :-1].values.astype(np.float32)

#     def step(self, action):
#         # Get current row
#         row = self.data.iloc[self.current_index]
        
#         # Reward mechanism: Encourage reasonable discounts
#         actual_discount = row["suggested_discount"]
#         reward = -abs(action - actual_discount)  # Closer to true discount = higher reward
        
#         self.current_index += 1
#         done = self.current_index >= len(self.data)
        
#         next_state = (
#             self.data.iloc[self.current_index, :-1].values.astype(np.float32)
#             if not done
#             else np.zeros(self.observation_space.shape)
#         )
        
#         return next_state, reward, done, {}

# # Create environment
# env = DummyVecEnv([lambda: BundleDiscountEnv(df)])

# # Train PPO Model
# model = PPO("MlpPolicy", env, verbose=1)
# model.learn(total_timesteps=10000)  # Train for 10,000 steps

# # Save model
# model.save("ppo_bundle_discount")

# # Load trained model
# model = PPO.load("ppo_bundle_discount")

# # Test prediction on new data
# test_sample = df.sample(1).drop(columns=["suggested_discount"]).values.astype(np.float32)
# predicted_discount = model.predict(test_sample)[0]
# print("Predicted Discount:", predicted_discount, "%")


# import pandas as pd
# import numpy as np
# import gym
# from stable_baselines3 import PPO
# from stable_baselines3.common.vec_env import DummyVecEnv
# from gym import spaces
# from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# # Load dataset
# df = pd.read_csv(r"C:\\Projects\\EbixPro_AI_bot\\Analysis\\Discount Management\\BUNDLE DISCOUNT\\Dataset\\final_bundle_discount_dataset.csv")

# # Debug: Check available columns
# print("Columns in dataset:", df.columns)

# # Ensure column names are lowercase (optional, if needed)
# df.columns = df.columns.str.lower()

# # Identify categorical columns
# categorical_cols = ["product_name", "category", "bundle_type"]

# # Encode categorical columns
# label_encoders = {}
# for col in categorical_cols:
#     if col in df.columns and df[col].dtype == "object":  # Ensure column exists
#         label_encoders[col] = LabelEncoder()
#         df[col] = label_encoders[col].fit_transform(df[col])

# # Ensure "suggested_discount" is present
# if "suggested_discount" not in df.columns:
#     raise KeyError("Column 'suggested_discount' is missing. Check dataset.")

# # Identify numeric columns excluding 'suggested_discount'
# num_cols = [col for col in df.select_dtypes(include=[np.number]).columns if col != "suggested_discount"]

# # Apply MinMaxScaler to numeric columns
# scaler = MinMaxScaler()
# df[num_cols] = scaler.fit_transform(df[num_cols])

# class BundleDiscountEnv(gym.Env):
#     def __init__(self, data):
#         super(BundleDiscountEnv, self).__init__()

#         self.data = data
#         self.current_index = 0

#         # Define state space
#         self.observation_space = spaces.Box(
#             low=0, high=1, shape=(len(num_cols),), dtype=np.float32
#         )

#         # Define action space (discount from 0% to 50%)
#         self.action_space = spaces.Discrete(51)  

#     def reset(self):
#         """Resets the environment and returns the first observation"""
#         self.current_index = 0
#         return self.data.iloc[self.current_index][num_cols].values.astype(np.float32)

#     def step(self, action):
#         """Takes an action and returns (next_state, reward, done, info)"""
#         row = self.data.iloc[self.current_index]

#         # Reward mechanism: Encourage discounts close to actual suggestion
#         actual_discount = row["suggested_discount"]
#         reward = -abs(action - actual_discount)  

#         self.current_index += 1
#         done = self.current_index >= len(self.data)

#         next_state = (
#             self.data.iloc[self.current_index][num_cols].values.astype(np.float32)
#             if not done
#             else np.zeros(self.observation_space.shape)
#         )

#         return next_state, reward, done, {}

# # Create and wrap environment
# env = DummyVecEnv([lambda: BundleDiscountEnv(df)])

# # Train PPO Model
# model = PPO("MlpPolicy", env, verbose=1)
# model.learn(total_timesteps=10000)

# # Save model
# model.save("ppo_bundle_discount")

# # Load trained model
# model = PPO.load("ppo_bundle_discount")

# # Test prediction on new data
# test_sample = df.sample(1)[num_cols].values.astype(np.float32)
# predicted_discount = model.predict(test_sample.reshape(1, -1))[0]  # Reshaped for model input
# print("Predicted Discount:", predicted_discount, "%")


import pandas as pd
import numpy as np
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from gymnasium import spaces
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# Load dataset
df = pd.read_csv(r"C:\\Projects\\EbixPro_AI_bot\\Analysis\\Discount Management\\BUNDLE DISCOUNT\\Dataset\\final_bundle_discount_dataset.csv")

# Normalize column names (remove spaces & lowercase)
df.columns = df.columns.str.strip().str.lower()

# Check if 'suggested_discount' exists, else compute it
if "suggested_discount" not in df.columns:
    if "historical_discount" in df.columns:
        df["suggested_discount"] = df["historical_discount"] * 0.9  # Example logic
    else:
        raise KeyError("❌ 'historical_discount' is missing! Cannot compute 'suggested_discount'.")

# Identify categorical columns that need encoding
categorical_cols = ["seller_id", "product_id", "bundle_id", "seasonality", "product_name", "category", "bundle_type"]
label_encoders = {}

for col in categorical_cols:
    if df[col].dtype == "object" or df[col].nunique() < 50:  # Encode non-numeric categorical features
        label_encoders[col] = LabelEncoder()
        df[col] = label_encoders[col].fit_transform(df[col])

# Ensure all columns are numeric
non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
if non_numeric_cols:
    raise ValueError(f"❌ Non-numeric columns detected even after encoding: {non_numeric_cols}")

# Identify numerical columns
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
num_cols.remove("suggested_discount")  # Exclude target column

# Scale numerical columns
scaler = MinMaxScaler()
df[num_cols] = scaler.fit_transform(df[num_cols])

# Debugging
print("✅ Data ready for training!\n", df.dtypes)
print("🔢 First few rows:\n", df.head())

# Define Custom Gym Environment
class BundleDiscountEnv(gym.Env):
    def __init__(self, data):
        super(BundleDiscountEnv, self).__init__()
        self.data = data
        self.current_index = 0

        # Define State Space (excluding suggested_discount)
        self.observation_space = spaces.Box(low=0, high=1, shape=(len(data.columns) - 1,), dtype=np.float32)

        # Define Action Space (discount range 0% to 50%)
        self.action_space = spaces.Discrete(51)

    def reset(self, seed=None, options=None):
        self.current_index = 0
        return self.data.iloc[self.current_index, :-1].values.astype(np.float32), {}

    def step(self, action):
        row = self.data.iloc[self.current_index]
        actual_discount = row["suggested_discount"]
        reward = -abs(action - actual_discount)  # Lower error → higher reward

        self.current_index += 1
        done = self.current_index >= len(self.data)

        next_state = self.data.iloc[self.current_index, :-1].values.astype(np.float32) if not done else np.zeros(self.observation_space.shape)

        return next_state, reward, done, {}, {}

# Create environment
env = DummyVecEnv([lambda: BundleDiscountEnv(df)])

# Train PPO Model
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

# Save trained model
model.save("ppo_bundle_discount")

# # Test prediction
# test_sample = df.sample(1).drop(columns=["suggested_discount"]).values.astype(np.float32)
# predicted_discount = model.predict(test_sample)[0]
# print("🎯 Predicted Discount:", predicted_discount, "%")

test_samples = df.sample(10).drop(columns=["suggested_discount"]).values.astype(np.float32)
predicted_discounts = model.predict(test_samples)[0]
print("✅ Predicted Discounts:", predicted_discounts)
