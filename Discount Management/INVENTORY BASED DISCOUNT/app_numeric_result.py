# Description: Streamlit app to get discount recommendation for a product based on inventory data.
# The app loads the preprocessed dataset and the trained RL model to provide discount suggestions.
# The user can select a Seller ID and Product to get a discount recommendation.
# The app displays the recommended discount percentage for the selected product.
# The app uses the trained RL model to predict the optimal discount based on the product features.
# Trained with store admin id and product name, Product_Category and Product_ID. getting result with converting categorical data to numerical data.
# streamlit will provide the selected items with numerical data and the model will predict the discount percentage.


# Import necessary libraries
import streamlit as st
import gym
import numpy as np
import pandas as pd
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
import os

# Load Dataset
DATASET_PATH = r"C:\Projects\EbixPro_AI_bot\Analysis\Discount Management\INVENTORY BASED DISCOUNT\Data\inventory_based_discount_dataset.csv"
MODEL_PATH = "discount_rl_model"

# Load and preprocess dataset
@st.cache_data
def load_data():
    df = pd.read_csv(DATASET_PATH)
    
    FEATURES = ["Product_ID", "Store_Admin_ID", "Product_Category", "Product_Name", 
                "Product_Price", "Discount_Offered", "Stock_Availability", "Reorder_Threshold", 
                "Average_Daily_Sales", "Days_of_Stock_Left", "Competitor_Price", 
                "Customer_Interest_Score", "Historical_Discount_Impact", "Seasonality_Flag", 
                "Day_of_Week", "Festive_Season"]
    df = df[FEATURES]

    def normalize_data(data):
        numeric_cols = data.select_dtypes(include=['number']).columns
        data[numeric_cols] = (data[numeric_cols] - data[numeric_cols].min()) / (data[numeric_cols].max() - data[numeric_cols].min())
        return data

    def preprocess_data(data):
        for col in data.select_dtypes(include=['object']).columns:
            data[col] = data[col].astype('category').cat.codes
        return data

    df = normalize_data(df)
    df = preprocess_data(df)
    return df

df = load_data()

# Define Custom Gym Environment
class InventoryDiscountEnv(gym.Env):
    def __init__(self, data):
        super(InventoryDiscountEnv, self).__init__()
        self.data = data.values
        self.current_step = 0
        self.action_space = gym.spaces.Box(low=0, high=30, shape=(1,), dtype=np.float32)
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(len(df.columns) - 2,), dtype=np.float32)

    def reset(self):
        self.current_step = 0
        return self.data[self.current_step, 2:]

    def step(self, action):
        discount = np.clip(action[0], 0, 30)
        reward = self.calculate_reward(self.current_step, discount)
        self.current_step += 1
        done = self.current_step >= len(self.data)
        obs = self.data[self.current_step, 2:] if not done else np.zeros(len(df.columns) - 2)
        return obs, reward, done, {}

    def calculate_reward(self, step, discount):
        row = self.data[step]
        sales = row[5]
        demand_score = row[8]
        revenue = sales * (1 - (discount / 100))
        stock_left = row[6]
        reward = (revenue * demand_score) - (stock_left * 0.1)
        if discount > 0:
            reward += 0.05 * discount
        return reward

# Train Model
def train_model():
    env = DummyVecEnv([lambda: InventoryDiscountEnv(df)])
    
    ppo_params = {
        "learning_rate": 0.0005,
        "n_steps": 4096,
        "batch_size": 128,
        "n_epochs": 15,
        "gamma": 0.98,
        "gae_lambda": 0.90,
        "clip_range": 0.15,
        "ent_coef": 0.05
    }

    model = PPO("MlpPolicy", env, verbose=1, **ppo_params)
    model.learn(total_timesteps=150000)
    model.save(MODEL_PATH)
    return model

# Load or Train Model
if os.path.exists(MODEL_PATH + ".zip"):
    model = PPO.load(MODEL_PATH)
else:
    model = train_model()

# Streamlit UI
st.title("🛒 Dynamic Discount Optimization")
st.write("Select a **Seller ID** and **Product** to get inventory based suggestion.")

# Dropdowns
seller_ids = df["Store_Admin_ID"].unique()
selected_seller = st.selectbox("Select Seller ID", seller_ids)

products = df[df["Store_Admin_ID"] == selected_seller]["Product_Name"].unique()
selected_product = st.selectbox("Select Product", products)

# Get Product Features
if st.button("Get Discount Recommendation"):
    product_data = df[(df["Store_Admin_ID"] == selected_seller) & (df["Product_Name"] == selected_product)]
    
    if not product_data.empty:
        obs = product_data.iloc[:, 2:].values[0]
        action, _ = model.predict(obs)
        discount_suggestion = round(action[0], 2)
        st.success(f"🔖 Recommended Discount: **{discount_suggestion}%** for '{selected_product}'")
    else:
        st.warning("⚠️ Product data not found!")