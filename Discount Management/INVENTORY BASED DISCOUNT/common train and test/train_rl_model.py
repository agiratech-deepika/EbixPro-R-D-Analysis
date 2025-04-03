# import gym
# import numpy as np
# from stable_baselines3 import PPO

# # Define Custom Gym Environment
# class InventoryDiscountEnv(gym.Env):
#     def __init__(self):
#         super(InventoryDiscountEnv, self).__init__()

#         # Define state space (features)
#         self.observation_space = gym.spaces.Box(low=0, high=1, shape=(10,), dtype=np.float32)

#         # Define action space (discounts in percentage)
#         self.action_space = gym.spaces.Discrete(7)  # 0%, 5%, 10%, 15%, 20%, 25%, 30%

#     def reset(self):
#         """Reset environment state"""
#         self.state = np.random.rand(10)  # Initialize a random state
#         return self.state

#     def step(self, action):
#         """Apply the selected discount and compute reward"""
#         discount = action * 5  # Convert action index to discount percentage

#         # Simulated sales increase based on discount
#         sales_increase = np.random.uniform(0, 1) * (discount / 30)  

#         # Reward function: Increase sales while minimizing discount loss
#         reward = (sales_increase * 200) - (discount * 1.5)   

#         # Update environment state
#         self.state = np.random.rand(10)
        
#         return self.state, reward, False, {}  # (next_state, reward, done, info)

# # Create Environment
# env = InventoryDiscountEnv()

# # Initialize PPO Model
# model = PPO("MlpPolicy", env, verbose=1)

# # Train the Model
# print("Training PPO Model...")
# model.learn(total_timesteps=10000)
# print("Training Complete!")

# # Save the Trained Model
# model.save("discount_rl_model")
# print("Model Saved!")


from stable_baselines3 import PPO
import gym
import numpy as np

# Define Custom Gym Environment
class InventoryDiscountEnv(gym.Env):
    def __init__(self):
        super(InventoryDiscountEnv, self).__init__()

        # State Space: 10 features
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(10,), dtype=np.float32)

        # Action Space: Discount levels (0% to 30%)
        self.action_space = gym.spaces.Discrete(7)  

    def reset(self):
        """Reset environment"""
        self.state = np.random.rand(10)  
        return self.state

    def step(self, action):
        """Apply discount and compute reward"""
        discount = action * 5  
        sales_increase = np.random.uniform(0, 1) * (discount / 30)  

        # Improved Reward Function
        # reward = (sales_increase * 200) - (discount * 1.5)  # Higher reward scaling
        # reward = (sales_increase * 150) - (discount ** 1.2) * 2.5
        reward = (sales_increase * 200) - (discount ** 1.1) * 1.8


        self.state = np.random.rand(10)
        return self.state, reward, False, {}

# Create Environment
env = InventoryDiscountEnv()

# 🔹 Optimized PPO Model
# model = PPO(
#     "MlpPolicy", env,
#     learning_rate=0.0005,  # Adjusted for better convergence
#     gamma=0.98,  # Slightly lower discount factor for shorter-term rewards
#     batch_size=128,  # Larger batch size for stable training
#     n_steps=2048,  # Rollout steps
#     ent_coef=0.01,  # Small entropy coefficient to encourage exploration
#     verbose=1
# )
# model = PPO(
#     "MlpPolicy", env,
#     learning_rate=0.0003,  
#     gamma=0.98,  
#     batch_size=128,  
#     n_steps=2048,  
#     ent_coef=0.05,  # 🔥 Increase entropy coefficient to encourage exploration
#     verbose=1
# )
model = PPO(
    "MlpPolicy", env,
    learning_rate=0.0003,  
    gamma=0.99,  
    batch_size=128,  
    n_steps=4096,  # 🔥 Increase steps for better learning
    ent_coef=0.1,  # 🔥 Higher entropy to force more exploration
    verbose=1
)



# Train the Model
print("Training Optimized PPO Model...")
# model.learn(total_timesteps=100000)  # Increased from 10,000 to 50,000
model.learn(total_timesteps=150000)  # 🔥 Train longer to avoid bias
print("Training Complete!")

# Save the Model
model.save("discount_rl_model_optimized_2")
print("Optimized Model Saved!")
