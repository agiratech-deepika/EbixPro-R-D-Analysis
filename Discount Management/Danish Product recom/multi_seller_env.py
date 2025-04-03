import numpy as np
from gym import spaces
import random

# Define the Z-score normalization function
def normalize_z_score(df, column):
    mean = df[column].mean()
    std = df[column].std()
    df[column + '_z'] = (df[column] - mean) / std
    return df

class MultiSellerEnv:
    def __init__(self, seller_data, seller_ids):
        # Initialize the environment with seller data and seller IDs
        self.seller_data = seller_data
        self.seller_ids = seller_ids

        # Apply Z-score normalization to the necessary columns
        self.seller_data = normalize_z_score(self.seller_data, 'stock_quantity')
        self.seller_data = normalize_z_score(self.seller_data, 'quantity_sold')
        self.seller_data = normalize_z_score(self.seller_data, 'trend_score')
        self.seller_data = normalize_z_score(self.seller_data, 'sales_revenue')
        self.seller_data = normalize_z_score(self.seller_data, 'price')

        # Define action and observation space
        self.action_space = spaces.Discrete(len(seller_data['product_id'].unique()))
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(5,), dtype=np.float32)

        self.current_seller_id = None
        self.current_seller_products = None
        self.current_step = 0

    def reset(self):
        # Reset the environment and select a random seller
        self.current_seller_id = random.choice(self.seller_ids)
        self.current_seller_products = self.seller_data[self.seller_data['seller_id'] == self.current_seller_id]
        self.current_step = 0

        # Return the initial observation (features of the first product for the selected seller)
        return self._get_observation()

    def _get_observation(self):
        # Get the normalized features of the current product
        product = self.current_seller_products.iloc[self.current_step]
        return np.array([
            product['stock_quantity_z'],
            product['quantity_sold_z'],
            product['trend_score_z'],
            product['sales_revenue_z'],
            product['price_z']
        ])

    def step(self, action):
        # Ensure the action is within bounds
        if action >= len(self.current_seller_products):
            action = 0  # Reset to first product if action is invalid

        # Select the product corresponding to the action
        product = self.current_seller_products.iloc[action]

        # Get the Z-score normalized values for reward calculation
        stock_quantity_z = product['stock_quantity_z']
        quantity_sold_z = product['quantity_sold_z']
        trend_score_z = product['trend_score_z']
        sales_revenue_z = product['sales_revenue_z']
        price_z = product['price_z']

        # Calculate individual rewards for each factor
        # 1) Sales Revenue Reward
        sales_revenue_reward = sales_revenue_z  # Higher revenue contributes positively
        if stock_quantity_z < 0:  # Low stock adds additional positive contribution
            sales_revenue_reward += abs(stock_quantity_z)

        # 2) Quantity Sold Reward
        quantity_sold_reward = quantity_sold_z  # Higher quantity sold contributes positively
        if stock_quantity_z < 0:  # Low stock adds additional positive contribution
            quantity_sold_reward += abs(stock_quantity_z)

        # 3) Trend Score Reward
        trend_score_reward = trend_score_z  # Higher trend score contributes positively
        if stock_quantity_z < 0:  # Low stock adds additional positive contribution
            trend_score_reward += abs(stock_quantity_z)

        # 4) Low Stock, High Demand Reward
        low_stock_high_demand_reward = 0
        if stock_quantity_z < 0 and quantity_sold_z > 0:  # Low stock + high demand
            low_stock_high_demand_reward = abs(stock_quantity_z) + quantity_sold_z

        # 5) Price Optimization Reward
        price_optimization_reward = 0
        if price_z < 0 and quantity_sold_z > 0:  # Lower price + high demand
            price_optimization_reward = abs(price_z) + quantity_sold_z

        # Combine all rewards into a final reward
        reward = (
            sales_revenue_reward +
            quantity_sold_reward +
            trend_score_reward +
            low_stock_high_demand_reward +
            price_optimization_reward
        )

        # Move to next step
        self.current_step += 1
        done = self.current_step >= len(self.current_seller_products)

        if not done:
            observation = self._get_observation()
        else:
            observation = np.zeros(self.observation_space.shape)

        return observation, reward, done, {"message": "Reward calculated based on updated logic"}