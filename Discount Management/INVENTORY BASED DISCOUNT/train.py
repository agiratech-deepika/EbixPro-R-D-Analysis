# Description: Train a Reinforcement Learning model to optimize discount offers for inventory-based discount management.
# Trained only with features without store_admin_id and product_name, Product_Category and Product_ID,
# Trained with the following features: "Product_Price", "Discount_Offered", "Stock_Availability", "Average_Daily_Sales", "Days_of_Stock_Left", "Competitor_Price", "Customer_Interest_Score", "Historical_Discount_Impact", "Seasonality_Flag", "Festive_Season", "Day_of_Week"
# The model is trained with improved hyperparameters for better exploration and performance.
# The reward function encourages discounting, penalizes unsold stock, and rewards increased demand at a reasonable discount.
# The model is tested on a sample dataset to evaluate its performance.
# The optimized model is saved for future use.
# The output shows the discount offered and the reward for each test episode.
# The model is trained with 150,000 timesteps for better convergence and performance.
# The model is saved as "discount_rl_model" for future use.
# The model is tested on 10 episodes to evaluate its performance.
# The output shows the discount offered and the reward for each test episode.


import gym
import numpy as np
import pandas as pd
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

# Load Dataset
dataset_path = r"C:\Projects\EbixPro_AI_bot\Analysis\Discount Management\INVENTORY BASED DISCOUNT\Data\inventory_based_discount_dataset.csv"
df = pd.read_csv(dataset_path)

# Select Relevant Features
FEATURES = [
    "Product_Price", "Discount_Offered", "Stock_Availability", "Average_Daily_Sales", 
    "Days_of_Stock_Left", "Competitor_Price", "Customer_Interest_Score", 
    "Historical_Discount_Impact", "Seasonality_Flag", "Festive_Season", "Day_of_Week"
]
df = df[FEATURES]

def normalize_data(data):
    numeric_cols = data.select_dtypes(include=['number']).columns
    data[numeric_cols] = (data[numeric_cols] - data[numeric_cols].min()) / (data[numeric_cols].max() - data[numeric_cols].min())
    return data

df = normalize_data(df)

def preprocess_data(data):
    for col in data.select_dtypes(include=['object']).columns:
        data[col] = data[col].astype('category').cat.codes  # Label encoding
    return data

df = preprocess_data(df)

# Define Custom Gym Environment
class InventoryDiscountEnv(gym.Env):
    def __init__(self, data):
        super(InventoryDiscountEnv, self).__init__()
        self.data = data.values
        self.current_step = 0
        self.action_space = gym.spaces.Box(low=0, high=30, shape=(1,), dtype=np.float32)  # Continuous Discount (0-30%)
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(len(FEATURES),), dtype=np.float32)
    
    def reset(self):
        self.current_step = 0
        return self.data[self.current_step]
    
    def step(self, action):
        discount = np.clip(action[0], 0, 30)  # Ensure discount is within 0-30%
        reward = self.calculate_reward(self.current_step, discount)
        self.current_step += 1
        done = self.current_step >= len(self.data)
        obs = self.data[self.current_step] if not done else np.zeros(len(FEATURES))
        return obs, reward, done, {}

    def calculate_reward(self, step, discount):
        row = self.data[step]
        sales = row[3]  # Average Daily Sales
        demand_score = row[6]  # Customer Interest Score
        revenue = sales * (1 - (discount / 100))  # Discount reduces revenue

        # **Updated Reward Function**:
        # - Encourages discounting
        # - Penalizes unsold stock
        # - Rewards increased demand at a reasonable discount
        stock_left = row[4]  # Days of Stock Left
        competitor_price = row[5]
        
        reward = (revenue * demand_score) - (stock_left * 0.1)  # Penalizing unsold stock
        if discount > 0:
            reward += 0.05 * discount  # Encouraging exploration
        
        return reward

# Initialize Environment
env = DummyVecEnv([lambda: InventoryDiscountEnv(df)])

# **Improved Hyperparameters for Better Exploration**
ppo_params = {
    "learning_rate": 0.0005,  # Slightly higher LR for better training
    "n_steps": 4096,  # Larger batch size to avoid overfitting to a few states
    "batch_size": 128,  # Better mini-batch size
    "n_epochs": 15,  # More training passes per batch
    "gamma": 0.98,  # Discount factor
    "gae_lambda": 0.90,  # Generalized Advantage Estimation
    "clip_range": 0.15,  # Slightly smaller clipping for PPO
    "ent_coef": 0.05,  # **Higher entropy** for more exploration
}

# Train RL Model
model = PPO("MlpPolicy", env, verbose=1, **ppo_params)
model.learn(total_timesteps=150000)  # Increased training time
model.save("discount_rl_model")
print("Training Complete! Optimized Model Saved!")

# **Test Model**
env_test = InventoryDiscountEnv(df)
obs = env_test.reset()
print("\nTesting Optimized RL Model...")
for i in range(10):
    action, _ = model.predict(obs)
    obs, reward, done, _ = env_test.step(action)
    print(f"Test {i+1}: Discount: {round(action[0])}%, Reward: {reward}")
    if done:
        break

# **Output**:
# Training Complete! Optimized Model Saved!
# Testing Optimized RL Model...
# Test 1: Discount: 23%, Reward: 1.2730001922489442
# Test 2: Discount: 21%, Reward: 1.0259236653645833
# Test 3: Discount: 9%, Reward: 1.0861839373087145
# Test 4: Discount: 19%, Reward: 1.3088140681027547
# Test 5: Discount: 14%, Reward: 0.7762550259728885
# Test 6: Discount: 15%, Reward: 0.7135272979736328
# Test 7: Discount: 8%, Reward: 0.43340044455839594
# Test 8: Discount: 15%, Reward: 0.8705220308172744
# Test 9: Discount: 20%, Reward: 1.2297846347987993
# Test 10: Discount: 14%, Reward: 0.6465550942546587