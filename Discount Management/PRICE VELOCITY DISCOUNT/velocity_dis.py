
# import gym
# import numpy as np
# import pandas as pd
# from stable_baselines3 import PPO
# from stable_baselines3.common.vec_env import DummyVecEnv
# import os

# # Correct dataset path
# data_path = r"C:\\Projects\\EbixPro_AI_bot\\Analysis\\Discount Management\\PRICE VELOCITY DISCOUNT\\Dataset\\price_velocity_discount.csv"

# if not os.path.exists(data_path):
#     raise FileNotFoundError(f"Dataset not found at: {data_path}")

# class PricingEnv(gym.Env):
#     def __init__(self, data_path):
#         super(PricingEnv, self).__init__()
        
#         # Load dataset
#         self.data = pd.read_csv(data_path)
#         self.current_step = 0
        
#         # Define action and observation space
#         self.action_space = gym.spaces.Discrete(3)  # 0: Decrease, 1: No Change, 2: Increase
#         self.observation_space = gym.spaces.Box(low=0, high=np.inf, shape=(5,), dtype=np.float32)

#     def reset(self):
#         self.current_step = 0
#         return self._get_obs()
    
#     def _get_obs(self):
#         row = self.data.iloc[self.current_step]
#         return np.array([
#             row['Sales_Velocity'], row['Stock_Level'], row['Competitor_Pricing'],
#             row['Discounted_Price'], row['Customer_Demand_Index']
#         ]).astype(np.float32)
    
#     def step(self, action):
#         row = self.data.iloc[self.current_step]
        
#         # Action Impact on Discounted Price
#         if action == 0:  # Increase Discount (Lower Price)
#             new_discount = row['Current_Discount'] + 5
#         elif action == 2:  # Reduce Discount (Increase Price)
#             new_discount = max(row['Current_Discount'] - 5, 0)  # Ensure discount doesn't go negative
#         else:  # Maintain Discount
#             new_discount = row['Current_Discount']
        
#         # Compute Reward (Profit Maximization)
#         new_price = row['Base_Price'] * (1 - new_discount / 100)
#         revenue = row['Units_Sold'] * new_price
#         cost = row['Units_Sold'] * row['Base_Price'] * 0.6  # Assuming 60% cost
#         profit = revenue - cost
#         reward = profit / max(row['Stock_Level'], 1)  # Avoid division by zero
        
#         self.current_step += 1
#         done = self.current_step >= len(self.data) - 1
        
#         return self._get_obs(), reward, done, {"Suggested_Discount": new_discount}
    
#     def render(self, mode='human'):
#         pass

# # Function to create environment
# def create_env():
#     return PricingEnv(data_path)

# # Train PPO Agent
# env = DummyVecEnv([create_env])
# model = PPO("MlpPolicy", env, verbose=1)
# model.learn(total_timesteps=10000)

# # Save and Load Model
# model.save("ppo_pricing_model")
# model = PPO.load("ppo_pricing_model")

# # Suggest Discount Based on Model Prediction
# def suggest_discount(model, env, steps=10):
#     obs = env.reset()
#     suggestions = []
    
#     for _ in range(steps):
#         action, _ = model.predict(obs)
#         obs, reward, done, info = env.step(action)
        
#         suggestion = "Increase Discount" if action == 0 else "Maintain Price" if action == 1 else "Reduce Discount"
#         discount_percentage = info[0]["Suggested_Discount"]  # Extract from wrapped env
        
#         suggestions.append((suggestion, discount_percentage))
#         print(f"Action: {action}, Suggested Discount Strategy: {suggestion}, Recommended Discount: {discount_percentage}%, Reward: {reward}")
        
#         if done:
#             break
#     return suggestions

# # Get discount suggestions
# suggest_discount(model, env)

import gym
import numpy as np
import pandas as pd
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
import os

# Define the correct dataset path
data_path = r"C:/Projects/Analysis/Discount Management/PRICE VELOCITY DISCOUNT/Dataset/price_velocity_discount.csv"

# Ensure dataset exists
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Dataset not found at: {data_path}")

class PricingEnv(gym.Env):
    def __init__(self, data_path):
        super(PricingEnv, self).__init__()
        
        # Load dataset
        self.data = pd.read_csv(data_path)
        self.current_step = 0
        
        # Define action and observation space
        self.action_space = gym.spaces.Discrete(3)  # 0: Decrease, 1: No Change, 2: Increase
        self.observation_space = gym.spaces.Box(low=0, high=np.inf, shape=(5,), dtype=np.float32)

        # Mapping for categorical values
        self.category_mapping = {
            "Low": 0,
            "Medium": 1,
            "High": 2
        }

    def reset(self):
        """Reset the environment and return the initial observation."""
        self.current_step = 0
        return self._get_obs()

    def _get_obs(self):
        """Retrieve the current observation state."""
        row = self.data.iloc[self.current_step]

        return np.array([
            self.category_mapping.get(row['Sales_Velocity'], row['Sales_Velocity']),
            row['Stock_Level'],
            row['Competitor_Pricing'],
            row['Discounted_Price'],
            self.category_mapping.get(row['Customer_Demand_Index'], row['Customer_Demand_Index'])
        ]).astype(np.float32)

    def step(self, action):
        """Apply action and compute the reward."""
        row = self.data.iloc[self.current_step]

        # Determine the new discount based on action
        if action == 0:  # Increase Discount (Lower Price)
            # new_discount = row['Current_Discount'] + 5
            new_discount = row['Discount_Percentage'] + 5
        elif action == 2:  # Reduce Discount (Increase Price)
            new_discount = max(row['Discount_Percentage'] - 5, 0)  # Ensure discount doesn't go negative
        else:  # Maintain Discount
            new_discount = row['Discount_Percentage']

        # Compute new price
        new_price = row['Base_Price'] * (1 - new_discount / 100)
        revenue = row['Units_Sold'] * new_price
        cost = row['Units_Sold'] * row['Base_Price'] * 0.6  # Assuming 60% cost
        profit = revenue - cost
        reward = profit / (row['Stock_Level'] + 1)  # Avoid division by zero

        self.current_step += 1
        done = self.current_step >= len(self.data) - 1

        return self._get_obs(), reward, done, {"Suggested_Discount": new_discount}

    def render(self, mode='human'):
        pass


# Train PPO Agent
env = DummyVecEnv([lambda: PricingEnv(data_path)])
model = PPO("MlpPolicy", env, verbose=1)

# Train the model
model.learn(total_timesteps=10000)

# Save and Load Model
model.save("ppo_pricing_model5")
model = PPO.load("ppo_pricing_model5")

# Suggest Discount Based on Model Prediction
def suggest_discount(model, env, steps=10):
    obs = env.reset()
    if isinstance(obs, tuple):  # Ensure proper format
        obs = obs[0]

    suggestions = []
    for _ in range(steps):
        action, _ = model.predict(obs)
        obs, reward, done, info = env.step(action)
        
        if isinstance(obs, tuple):  # Ensure obs is in the right format
            obs = obs[0]

        suggestion = "Increase Discount" if action == 0 else "Maintain Price" if action == 1 else "Reduce Discount"
        discount_percentage = info[0]["Suggested_Discount"]  # Ensure correct extraction

        suggestions.append((suggestion, discount_percentage))
        print(f"Action: {action}, Suggested Discount Strategy: {suggestion}, Recommended Discount: {discount_percentage}%, Reward: {reward}")

        if done:
            break
    return suggestions

# Get discount suggestions
suggest_discount(model, env)

# import gym
# import numpy as np
# import pandas as pd
# from stable_baselines3 import PPO
# from stable_baselines3.common.vec_env import DummyVecEnv
# import os

# # Define the correct dataset path
# data_path = r"C:/Projects/Analysis/Discount Management/PRICE VELOCITY DISCOUNT/Dataset/price_velocity_discount.csv"

# # Ensure dataset exists
# if not os.path.exists(data_path):
#     raise FileNotFoundError(f"Dataset not found at: {data_path}")

# class PricingEnv(gym.Env):
#     def __init__(self, data_path):
#         super(PricingEnv, self).__init__()
        
#         # Load dataset
#         self.data = pd.read_csv(data_path)
#         self.current_step = 0
        
#         # Define action and observation space
#         self.action_space = gym.spaces.Discrete(3)  # 0: Increase Discount, 1: Maintain, 2: Reduce Discount
#         self.observation_space = gym.spaces.Box(low=0, high=np.inf, shape=(5,), dtype=np.float32)

#         # Mapping for categorical values
#         self.category_mapping = {"Low": 0, "Medium": 1, "High": 2}

#     def reset(self):
#         self.current_step = 0
#         return self._get_obs()

#     def _get_obs(self):
#         row = self.data.iloc[self.current_step]
#         return np.array([
#             self.category_mapping.get(row['Sales_Velocity'], row['Sales_Velocity']),
#             row['Stock_Level'],
#             row['Competitor_Pricing'],
#             row['Discount_Percentage'],  # Ensure using correct column
#             self.category_mapping.get(row['Customer_Demand_Index'], row['Customer_Demand_Index'])
#         ]).astype(np.float32)

#     def step(self, action):
#         row = self.data.iloc[self.current_step]
        
#         # Determine new discount based on action
#         if action == 0:
#             new_discount = row['Discount_Percentage'] + 5
#         elif action == 2:
#             new_discount = max(row['Discount_Percentage'] - 5, 0)
#         else:
#             new_discount = row['Discount_Percentage']

#         # Compute new price
#         new_price = row['Base_Price'] * (1 - new_discount / 100)
#         revenue = row['Units_Sold'] * new_price
#         cost = row['Units_Sold'] * row['Base_Price'] * 0.6
#         profit = revenue - cost
#         reward = profit / (row['Stock_Level'] + 1)  # Avoid division by zero

#         self.current_step += 1
#         done = self.current_step >= len(self.data) - 1

#         return self._get_obs(), reward, done, {"Suggested_Discount": new_discount}

#     def render(self, mode='human'):
#         pass

# # Train PPO Agent
# env = DummyVecEnv([lambda: PricingEnv(data_path)])
# model = PPO("MlpPolicy", env, verbose=1)

# # Train the model
# model.learn(total_timesteps=10000)

# # Save and Load Model
# model.save("ppo_pricing_model")
# model = PPO.load("ppo_pricing_model")

# # Suggest Discount Based on Model Prediction
# def suggest_discount(model, env, steps=10):
#     obs = env.reset()
#     if isinstance(obs, tuple):
#         obs = obs[0]
    
#     suggestions = []
#     for _ in range(steps):
#         action, _ = model.predict(obs)
#         obs, reward, done, info = env.step(action)
        
#         if isinstance(obs, tuple):
#             obs = obs[0]

#         suggestion = "Increase Discount" if action == 0 else "Maintain Price" if action == 1 else "Reduce Discount"
#         discount_percentage = info[0]["Suggested_Discount"]

#         suggestions.append((suggestion, discount_percentage))
#         print(f"Action: {action}, Suggested Discount Strategy: {suggestion}, Recommended Discount: {discount_percentage}%, Reward: {reward}")

#         if done:
#             break
#     return suggestions

# # Get discount suggestions
# suggest_discount(model, env)


