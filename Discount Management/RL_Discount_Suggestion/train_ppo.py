# import gym
# from stable_baselines3 import PPO
# from train_env import InventoryDiscountEnv

# # Initialize custom environment
# # env = InventoryDiscountEnv(csv_file="C:\Projects\EbixPro_AI_bot\Analysis\Discount Management\RL_Discount_Suggestion\Data\ecommerce dataset.csv")
# env = InventoryDiscountEnv(csv_file=r"C:\Projects\EbixPro_AI_bot\Analysis\Discount Management\RL_Discount_Suggestion\Data\ecommerce dataset.csv")


# # Train PPO Model
# model = PPO("MlpPolicy", env, verbose=1)
# model.learn(total_timesteps=10000)

# # Save trained model
# model.save("ppo_discount_model")
# print("✅ Model saved successfully!")

import gym
from stable_baselines3 import PPO
from train_env import InventoryDiscountEnv

# Initialize custom environment
env = InventoryDiscountEnv(csv_file=r"C:\Projects\EbixPro_AI_bot\Analysis\Discount Management\RL_Discount_Suggestion\Data\ecommerce dataset.csv")

# Train PPO Model
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

# Save trained model
model.save("ppo_discount_model")
print("✅ Model saved successfully!")

