# # import gym
# # from gym import spaces
# # import numpy as np
# # import pandas as pd

# # class InventoryDiscountEnv(gym.Env):
# #     def __init__(self, csv_file):
# #         super(InventoryDiscountEnv, self).__init__()
        
# #         # Load dataset
# #         self.data = pd.read_csv(csv_file)
# #         self.current_idx = 0  # Track the current product row
        
# #         # Action space: Discount range (0% to 50%)
# #         self.action_space = spaces.Box(low=0, high=50, shape=(1,), dtype=np.float32)
        
# #         # Observation space: stock_quantity, price, trend_score, days_in_inventory
# #         self.observation_space = spaces.Box(
# #             low=np.array([0, 0, 0, 0]), 
# #             high=np.array([10000, 10000, 1, 365]), 
# #             dtype=np.float32
# #         )
    
# #     def reset(self):
# #         """ Reset environment and return first observation """
# #         self.current_idx = np.random.randint(0, len(self.data))  # Select a random product
# #         return self._get_observation()
    
# #     def _get_observation(self):
# #         """ Extract relevant features for RL """
# #         row = self.data.iloc[self.current_idx]
# #         return np.array([row['stock_quantity'], row['price'], row['trend_score'], row['days_in_inventory']], dtype=np.float32)
    
# #     def step(self, action):
# #         """ Apply discount and compute reward """
# #         discount = action[0]  # Extract action (discount %)
# #         row = self.data.iloc[self.current_idx]
        
# #         # Simulate sales boost: More discount → More sales
# #         sales_boost = np.exp(-discount / 20) * row['quantity_sold']
        
# #         # Reward: Higher sales + Avoid excessive discount
# #         reward = sales_boost - (discount * 5)  # Penalize high discounts
        
# #         # Move to the next product (simulate batch processing)
# #         self.current_idx = (self.current_idx + 1) % len(self.data)
        
# #         return self._get_observation(), reward, False, {}
# import gym
# from gym import spaces
# import numpy as np
# import pandas as pd

# class InventoryDiscountEnv(gym.Env):
#     """Custom environment for optimizing discount strategy."""
    
#     def __init__(self, csv_file):
#         super(InventoryDiscountEnv, self).__init__()

#         # Load dataset
#         self.data = pd.read_csv(csv_file)
#         self.data.fillna(0, inplace=True)  # Handle missing values
#         self.current_idx = 0  # Track the current product row

#         # Action space: Discount range (5% to 50%)
#         self.action_space = spaces.Box(low=5, high=50, shape=(1,), dtype=np.float32)

#         # Observation space: stock_quantity, price, trend_score, days_in_inventory
#         self.observation_space = spaces.Box(
#             low=np.array([0, 0, 0, 0]), 
#             high=np.array([10000, 10000, 1, 365]), 
#             dtype=np.float32
#         )

#     def reset(self):
#         """Reset environment and return first observation."""
#         self.current_idx = np.random.randint(0, len(self.data))  # Select a random product
#         return self._get_observation()

#     def _get_observation(self):
#         """Extract relevant features for RL."""
#         row = self.data.iloc[self.current_idx]
#         return np.array([
#             row['stock_quantity'], 
#             row['price'], 
#             row['trend_score'], 
#             row['days_in_inventory']
#         ], dtype=np.float32)

#     # def step(self, action):
#     #     """Apply discount and compute reward."""
#     #     discount = np.clip(action[0], 0, 50)  # Ensure action is within range
#     #     row = self.data.iloc[self.current_idx]

#     #     # Simulate sales boost: More discount → More sales
#     #     sales_boost = np.exp(-discount / 20) * row.get('quantity_sold', 1)

#     #     # Reward function: Encourage higher sales but penalize excessive discount
#     #     reward = sales_boost - (discount * 5)

#     #     # Move to the next product (simulate batch processing)
#     #     self.current_idx = (self.current_idx + 1) % len(self.data)

#     #     return self._get_observation(), reward, False, {}
#     def step(self, action):
#         discount = np.clip(action[0], 5, 50)  # Minimum discount is now 5%
#         row = self.data.iloc[self.current_idx]

#         sales_boost = np.exp(-discount / 20) * row.get('quantity_sold', 1)

#         # Penalize discounts below 5% more heavily
#         if discount < 5:
#             reward = -10
#         else:
#             reward = sales_boost - (discount * 5)  # Encourage sales but prevent over-discounting

#         self.current_idx = (self.current_idx + 1) % len(self.data)
#         return self._get_observation(), reward, False, {}

import gym
from gym import spaces
import numpy as np
import pandas as pd

class InventoryDiscountEnv(gym.Env):
    """Custom environment for optimizing discount strategy using RL."""

    def __init__(self, csv_file):
        super(InventoryDiscountEnv, self).__init__()

        # Load dataset
        self.data = pd.read_csv(csv_file)
        self.data.fillna(0, inplace=True)  # Handle missing values
        self.current_idx = 0  # Track the current product row

        # Action space: Discount range (5% to 50%)
        self.action_space = spaces.Box(low=5, high=50, shape=(1,), dtype=np.float32)

        # Observation space: Define state with additional features
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0, 0, 0, 0, 0]),  # Min values
            high=np.array([10000, 10000, 1, 365, 500, 10000, 1, 100]),  # Max values
            dtype=np.float32
        )

    def reset(self):
        """Reset environment and return first observation."""
        self.current_idx = np.random.randint(0, len(self.data))  # Select a random product
        return self._get_observation()

    def _get_observation(self):
        """Extract relevant features for RL."""
        row = self.data.iloc[self.current_idx]
        return np.array([
            row['stock_quantity'], 
            row['price'], 
            row['trend_score'], 
            row['days_in_inventory'],
            row['reorder_threshold'],
            row['competitor_price'],
            row['profit_margin'],
            row['customer_purchase_frequency']
        ], dtype=np.float32)

    def step(self, action):
        """Apply discount and compute reward based on optimized strategy."""
        discount = np.clip(action[0], 5, 50)  # Ensure discount is within range
        row = self.data.iloc[self.current_idx]

        # Factors affecting discount efficiency
        stock_excess_ratio = row['stock_quantity'] / (row['reorder_threshold'] + 1)
        competitor_price_gap = row['competitor_price'] - row['price']
        aging_factor = row['days_in_inventory'] / 365
        profit_margin_penalty = (50 - row['profit_margin']) / 50  # Lower margin → Less discount

        # Sales boost function - adjusted with competitor pricing and customer frequency
        base_sales_boost = np.exp(-discount / 20) * row.get('quantity_sold', 1)
        competitor_adjustment = 1 + (competitor_price_gap / row['price']) if row['price'] > 0 else 1
        purchase_frequency_factor = row['customer_purchase_frequency']

        # Final sales adjustment
        sales_boost = base_sales_boost * competitor_adjustment * purchase_frequency_factor

        # Reward function with balanced trade-offs
        reward = (sales_boost * stock_excess_ratio) - (discount * profit_margin_penalty) - (aging_factor * 5)

        # Move to the next product
        self.current_idx = (self.current_idx + 1) % len(self.data)

        return self._get_observation(), reward, False, {}
