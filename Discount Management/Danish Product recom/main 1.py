# import streamlit as st
# import pandas as pd
# from stable_baselines3 import PPO
# from multi_seller_env import MultiSellerEnv

# # Load the dataset
# seller_data = pd.read_csv(r'C:\Project\product_recommendation\ecommerce.csv')

# # Extract unique seller IDs
# seller_ids = seller_data['seller_id'].unique()

# # Create an environment
# env = MultiSellerEnv(seller_data, seller_ids)

# # Load trained model or train if not available
# try:
#     model = PPO.load("multi_seller_recommendation_model")
# except:
#     model = PPO('MlpPolicy', env, verbose=1)
#     model.learn(total_timesteps=10000)
#     model.save("multi_seller_recommendation_model")

# # Streamlit App for Seller Product Recommendation
# st.title('Multi-Seller Product Recommendation System')

# # User Input for Seller ID
# seller_id = st.text_input("Enter your Seller ID")

# if seller_id:
#     try:
#         # Convert seller_id to int for comparison
#         seller_id = int(seller_id)

#         if seller_id not in seller_ids:
#             st.error("Seller ID not found!")
#         else:
#             # Filter seller's product data
#             seller_products = seller_data[seller_data['seller_id'] == seller_id]

#             if seller_products.empty:
#                 st.error("No products found for this seller!")
#             else:
#                 st.subheader("Seller Product Data")
#                 st.write(seller_products)

#                 # Reset environment for the specific seller
#                 env.current_seller_id = seller_id
#                 env.current_seller_products = seller_products
#                 obs = env.reset()

#                 # Calculate rewards for all products using the environment's step function
#                 rewards = []
#                 for idx, product in seller_products.iterrows():
#                     action = idx  # Use product index as action
#                     obs, reward, done, _ = env.step(action)
#                     rewards.append({
#                         'product_name': product['product_name'],
#                         'category': product['product_category'],
#                         'price': product['price'],
#                         'stock_quantity': product['stock_quantity'],
#                         'trend_score': product['trend_score'],
#                         'quantity_sold': product['quantity_sold'],
#                         'reward': reward
#                     })

#                 # Show all products with reward points in table format
#                 st.subheader("All Products with Reward Points")
#                 rewards_df = pd.DataFrame(rewards)
#                 st.table(rewards_df)

#                 # Input for number of recommendations
#                 num_recommendations = st.number_input("Enter the number of recommendations", min_value=1, max_value=10, value=5)

#                 # Sort recommendations by reward (descending order)
#                 recommendations = sorted(rewards, key=lambda x: x['reward'], reverse=True)[:num_recommendations]

#                 # Show top recommendations in table format
#                 st.subheader(f"Top {num_recommendations} Recommended Products")
#                 recommendations_df = pd.DataFrame(recommendations)
#                 st.table(recommendations_df)

#     except ValueError:
#         st.error("Please enter a valid Seller ID (numeric).")



import streamlit as st
import pandas as pd
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from multi_seller_env import MultiSellerEnv


# Load the dataset
seller_data = pd.read_csv(r'C:\Projects\EbixPro_AI_bot\Analysis\Discount Management\Danish Product recom\ecommerce.csv')

# Extract unique seller IDs
seller_ids = seller_data['seller_id'].unique()

# Streamlit App for Seller Product Recommendation
st.title('Multi-Seller Product Recommendation System')

# Initialize session state for rewards
if 'rewards' not in st.session_state:
    st.session_state.rewards = None

# User Input for Seller ID
seller_id = st.text_input("Enter your Seller ID")

if seller_id:
    try:
        # Convert seller_id to int for comparison
        seller_id = int(seller_id)

        if seller_id not in seller_ids:
            st.error("Seller ID not found!")
        else:
            # Filter seller's product data
            seller_products = seller_data[seller_data['seller_id'] == seller_id]

            if seller_products.empty:
                st.error("No products found for this seller!")
            else:
                st.subheader("Seller Product Data")
                st.write(seller_products)

                # Check if rewards are already calculated for this seller
                if st.session_state.rewards is None or st.session_state.current_seller_id != seller_id:
                    # Create an environment for the specific seller
                    env = MultiSellerEnv(seller_data, seller_ids)
                    env.current_seller_id = seller_id
                    env.current_seller_products = seller_products
                    obs = env.reset()

                    # Load or train the model
                    try:
                        model = PPO.load("multi_seller_recommendation_model")
                    except:
                        # Use vectorized environment for faster training
                        vec_env = make_vec_env(lambda: MultiSellerEnv(seller_data, seller_ids), n_envs=4)
                        model = PPO('MlpPolicy', vec_env, verbose=1, learning_rate=0.0003, n_steps=2048, batch_size=64)
                        model.learn(total_timesteps=20000)
                        model.save("multi_seller_recommendation_model")

                    # Calculate rewards for all products using the environment's step function
                    rewards = []
                    for idx, product in seller_products.iterrows():
                        action = idx  # Use product index as action
                        obs, reward, done, _ = env.step(action)
                        rewards.append({
                            'product_name': product['product_name'],
                            'category': product['product_category'],
                            'price': product['price'],
                            'stock_quantity': product['stock_quantity'],
                            'trend_score': product['trend_score'],
                            'quantity_sold': product['quantity_sold'],
                            'reward': reward
                        })

                    # Store rewards and current seller ID in session state
                    st.session_state.rewards = rewards
                    st.session_state.current_seller_id = seller_id

                # Show all products with reward points in table format
                st.subheader("All Products with Reward Points")
                rewards_df = pd.DataFrame(st.session_state.rewards)
                st.table(rewards_df)

                # Input for number of recommendations
                num_recommendations = st.number_input("Enter the number of recommendations", min_value=1, max_value=10, value=5)

                # Sort recommendations by reward (descending order)
                recommendations = sorted(st.session_state.rewards, key=lambda x: x['reward'], reverse=True)[:num_recommendations]

                # Show top recommendations in table format
                st.subheader(f"Top {num_recommendations} Recommended Products")
                recommendations_df = pd.DataFrame(recommendations)
                st.table(recommendations_df)

    except ValueError:
        st.error("Please enter a valid Seller ID (numeric).")