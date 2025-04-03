# from stable_baselines3 import PPO
# import numpy as np
# from train_rl_model import InventoryDiscountEnv
# import pandas as pd


# # Load the trained model
# model = PPO.load("discount_rl_model")

# # Create a new instance of the environment
# env = InventoryDiscountEnv()

# # Test the model on new data
# obs = env.reset()
# print("Testing the RL Model...")

# for i in range(10):
#     obs = env.reset()  # Reset environment for fresh conditions
#     action, _ = model.predict(obs)  # Get best action
#     obs, reward, done, _ = env.step(action)  # Apply action
#     print(f"Test {i+1}: Discount: {action * 5}%, Reward: {reward}") 

from stable_baselines3 import PPO
import numpy as np
from train_rl_model import InventoryDiscountEnv

# Load the trained model
model = PPO.load("discount_rl_model_optimized_1")

# Create Environment
env = InventoryDiscountEnv()

# Test with Multiple Resets
print("Testing Optimized RL Model...")
for i in range(10):
    obs = env.reset()
    action, _ = model.predict(obs)  
    obs, reward, done, _ = env.step(action)  
    print(f"Test {i+1}: Discount: {action * 5}%, Reward: {reward}") 
