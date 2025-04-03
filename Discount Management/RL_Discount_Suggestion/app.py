# # import streamlit as st
# # import pandas as pd
# # import numpy as np
# # from stable_baselines3 import PPO
# # from train_env import InventoryDiscountEnv

# # # Load dataset
# # DATA_PATH = r"C:\Projects\EbixPro_AI_bot\Analysis\Discount Management\RL_Discount_Suggestion\Data\ecommerce dataset.csv"
# # df = pd.read_csv(DATA_PATH)

# # # Load trained PPO model
# # MODEL_PATH = "ppo_discount_model.zip"
# # model = PPO.load(MODEL_PATH)

# # st.title("📉 Inventory Discount Recommendation System")

# # # Seller ID Selection
# # seller_ids = df['seller_id'].unique()
# # selected_seller = st.selectbox("Select Seller ID", seller_ids)

# # # Filter products under selected seller
# # seller_products = df[df['seller_id'] == selected_seller]

# # # Product Selection
# # selected_product = st.selectbox("Select Product", seller_products['product_name'].unique())

# # # Get product details
# # product_data = seller_products[seller_products['product_name'] == selected_product].iloc[0]

# # st.write("### Product Details:")
# # st.write(product_data)

# # # Extract Features for Model Prediction
# # obs = np.array([
# #     product_data['stock_quantity'],
# #     product_data['price'],
# #     product_data['trend_score'],
# #     product_data['days_in_inventory']
# # ], dtype=np.float32).reshape(1, -1)

# # # Predict Recommended Discount
# # action, _ = model.predict(obs)
# # # recommended_discount = round(action[0], 2)
# # recommended_discount = round(float(action[0]), 2)


# # st.write(f"### 💡 Recommended Discount: **{recommended_discount}%**")

# import streamlit as st
# import pandas as pd
# import numpy as np
# from stable_baselines3 import PPO
# from train_env import InventoryDiscountEnv

# # Load dataset
# DATA_PATH = r"C:\Projects\EbixPro_AI_bot\Analysis\Discount Management\RL_Discount_Suggestion\Data\ecommerce dataset.csv"
# df = pd.read_csv(DATA_PATH)

# # Load trained PPO model
# MODEL_PATH = "ppo_discount_model.zip"
# model = PPO.load(MODEL_PATH)

# st.title("📉 Inventory Discount Recommendation System")

# # Seller ID Selection
# seller_ids = df['seller_id'].unique()
# selected_seller = st.selectbox("Select Seller ID", seller_ids)

# # Filter products under selected seller
# seller_products = df[df['seller_id'] == selected_seller]

# # Product Selection
# selected_product = st.selectbox("Select Product", seller_products['product_name'].unique())

# # Get product details
# product_data = seller_products[seller_products['product_name'] == selected_product].iloc[0]

# st.write("### Product Details:")
# st.write(product_data)

# # Extract Features for Model Prediction
# obs = np.array([
#     product_data['stock_quantity'],
#     product_data['price'],
#     product_data['trend_score'],
#     product_data['days_in_inventory']
# ], dtype=np.float32).reshape(1, -1)

# # Predict Recommended Discount
# action, _ = model.predict(obs)
# recommended_discount = round(action[0].item(), 2)  # FIX: Convert NumPy value to Python float

# st.write(f"### 💡 Recommended Discount: **{recommended_discount}%**")

# import streamlit as st
# import pandas as pd
# import numpy as np
# from stable_baselines3 import PPO

# # Load dataset
# DATA_PATH = r"C:\Projects\EbixPro_AI_bot\Analysis\Discount Management\RL_Discount_Suggestion\Data\ecommerce dataset.csv"
# df = pd.read_csv(DATA_PATH)

# # Load trained model
# MODEL_PATH = "ppo_discount_model.zip"
# model = PPO.load(MODEL_PATH)

# # Streamlit UI
# st.title("📉 Inventory Discount Recommendation System")

# # Step 1: Select Seller ID (Dropdown, No Pre-selection)
# seller_ids = df['seller_id'].unique()
# selected_seller = st.selectbox("Select Seller ID", options=["Select"] + list(seller_ids), index=0)

# # Step 2: Select Product (Only After Seller is Chosen)
# if selected_seller != "Select":
#     seller_products = df[df['seller_id'] == selected_seller]['product_name'].unique()
#     selected_product = st.selectbox("Select Product", options=["Select"] + list(seller_products), index=0)

#     # Step 3: Only Proceed If Both Selections Are Made
#     if selected_product != "Select":
#         product_data = df[(df['seller_id'] == selected_seller) & (df['product_name'] == selected_product)].iloc[0]

#         # Display Product Details
#         st.write("### Product Details:")
#         st.write(product_data)

#         # Step 4: Prepare observation for model
#         obs = np.array([
#             product_data['stock_quantity'],
#             product_data['price'],
#             product_data['trend_score'],
#             product_data['days_in_inventory']
#         ], dtype=np.float32).reshape(1, -1)

#         # Step 5: Get Model Prediction
#         action, _ = model.predict(obs)
#         recommended_discount = round(float(action[0]), 2)

#         # Display Discount Recommendation
#         st.write(f"### 💡 Recommended Discount: **{recommended_discount}%**")
# import streamlit as st
# import pandas as pd
# import numpy as np
# from stable_baselines3 import PPO

# # Load dataset
# DATA_PATH = r"C:\Projects\EbixPro_AI_bot\Analysis\Discount Management\RL_Discount_Suggestion\Data\ecommerce dataset.csv"

# # Ensure correct data types
# df = pd.read_csv(DATA_PATH)

# # Convert numeric columns explicitly to avoid serialization errors
# numeric_columns = ['stock_quantity', 'price', 'trend_score', 'days_in_inventory']
# for col in numeric_columns:
#     df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert non-numeric values to NaN

# # Load trained model
# MODEL_PATH = "ppo_discount_model.zip"
# try:
#     model = PPO.load(MODEL_PATH)
# except Exception as e:
#     st.error(f"⚠️ Model loading failed: {e}")
#     st.stop()  # Stop execution if the model fails to load

# # Streamlit UI
# st.title("📉 Inventory Discount Recommendation System")

# # Step 1: Select Seller ID (Dropdown, No Pre-selection)
# seller_ids = df['seller_id'].unique().tolist()
# selected_seller = st.selectbox("Select Seller ID", options=["Select"] + seller_ids, index=0)

# # Step 2: Select Product (Only After Seller is Chosen)
# if selected_seller != "Select":
#     seller_products = df[df['seller_id'] == selected_seller]['product_name'].unique().tolist()
#     selected_product = st.selectbox("Select Product", options=["Select"] + seller_products, index=0)

#     # Step 3: Only Proceed If Both Selections Are Made
#     if selected_product != "Select":
#         product_data = df[(df['seller_id'] == selected_seller) & (df['product_name'] == selected_product)].iloc[0]

#         # Display Product Details
#         st.write("### Product Details:")
#         st.write(product_data)

#         # Step 4: Prepare observation for model
#         obs = np.array([
#             product_data['stock_quantity'],
#             product_data['price'],
#             product_data['trend_score'],
#             product_data['days_in_inventory']
#         ], dtype=np.float32).reshape(1, -1)

#         # Step 5: Get Model Prediction
#         try:
#             action, _ = model.predict(obs)
#             recommended_discount = round(float(action.item()), 2)  # Extract scalar safely
#             st.write(f"### 💡 Recommended Discount: **{recommended_discount}%**")
#         except Exception as e:
#             st.error(f"⚠️ Model prediction failed: {e}")

# import streamlit as st
# import pandas as pd
# import numpy as np
# import torch
# from stable_baselines3 import PPO

# # Load dataset
# DATA_PATH = r"C:\Projects\EbixPro_AI_bot\Analysis\Discount Management\RL_Discount_Suggestion\Data\ecommerce dataset.csv"

# # Ensure correct data types
# df = pd.read_csv(DATA_PATH)

# # Convert numeric columns explicitly to avoid serialization errors
# numeric_columns = ['stock_quantity', 'price', 'trend_score', 'days_in_inventory']
# for col in numeric_columns:
#     df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert non-numeric values to NaN

# # Load trained model
# MODEL_PATH = "ppo_discount_model.zip"
# try:
#     device = "cuda" if torch.cuda.is_available() else "cpu"
#     model = PPO.load(MODEL_PATH, device=device)  # Ensure proper device usage
# except Exception as e:
#     st.error(f"⚠️ Model loading failed: {e}")
#     st.stop()  # Stop execution if the model fails to load

# # Streamlit UI
# st.title("📉 Inventory Discount Recommendation System")

# # Step 1: Select Seller ID
# seller_ids = df['seller_id'].dropna().unique().tolist()
# selected_seller = st.selectbox("Select Seller ID", options=["Select"] + seller_ids, index=0)

# # Step 2: Select Product (Only After Seller is Chosen)
# if selected_seller != "Select":
#     seller_products = df[df['seller_id'] == selected_seller]['product_name'].dropna().unique().tolist()
#     selected_product = st.selectbox("Select Product", options=["Select"] + seller_products, index=0)

#     # Step 3: Only Proceed If Both Selections Are Made
#     if selected_product != "Select":
#         product_data = df[(df['seller_id'] == selected_seller) & (df['product_name'] == selected_product)].iloc[0]

#         # Display Product Details
#         st.write("### Product Details:")
#         st.write(product_data.to_frame().T)  # Display in table format

#         # Step 4: Prepare observation for model
#         obs = np.array([
#             product_data['stock_quantity'],
#             product_data['price'],
#             product_data['trend_score'],
#             product_data['days_in_inventory']
#         ], dtype=np.float32).reshape(1, -1)

#         # Step 5: Get Model Prediction
#         try:
#             action, _ = model.predict(obs)
#             recommended_discount = round(float(action.item()), 2)  # Extract scalar safely
#             st.write(f"### 💡 Recommended Discount: **{recommended_discount}%**")
#         except Exception as e:
#             st.error(f"⚠️ Model prediction failed: {e}")

import streamlit as st
import pandas as pd
import numpy as np
import torch
from stable_baselines3 import PPO

# Load dataset
DATA_PATH = r"C:\Projects\EbixPro_AI_bot\Analysis\Discount Management\RL_Discount_Suggestion\Data\ecommerce dataset.csv"
df = pd.read_csv(DATA_PATH)

# Ensure correct data types
numeric_columns = ['stock_quantity', 'price', 'trend_score', 'days_in_inventory', 'profit_margin', 'competitor_price', 'customer_purchase_frequency']
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')  

# Load trained model
MODEL_PATH = "ppo_discount_model.zip"
try:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = PPO.load(MODEL_PATH, device=device)
except Exception as e:
    st.error(f"⚠️ Model loading failed: {e}")
    st.stop()

# Streamlit UI
st.title("📉 Inventory Discount Recommendation System")

# Step 1: Select Seller ID
seller_ids = df['seller_id'].dropna().unique().tolist()
selected_seller = st.selectbox("Select Seller ID", options=["Select"] + seller_ids, index=0)

# Step 2: Select Product (Only After Seller is Chosen)
if selected_seller != "Select":
    seller_products = df[df['seller_id'] == selected_seller]['product_name'].dropna().unique().tolist()
    selected_product = st.selectbox("Select Product", options=["Select"] + seller_products, index=0)

    if selected_product != "Select":
        product_data = df[(df['seller_id'] == selected_seller) & (df['product_name'] == selected_product)].iloc[0]
        st.write("### Product Details:")
        st.write(product_data.to_frame().T)  # Display in table format

        # Prepare observation for model
        obs = np.array([
            product_data['stock_quantity'],
            product_data['price'],
            product_data['trend_score'],
            product_data['days_in_inventory'],
            product_data['reorder_threshold'],  
            product_data['competitor_price'],
            product_data['profit_margin'],
            product_data['customer_purchase_frequency']
        ], dtype=np.float32).reshape(1, -1)


        try:
            action, _ = model.predict(obs)
            recommended_discount = round(float(action.item()), 2)
            st.write(f"### 💡 Recommended Discount: **{recommended_discount}%**")
        except Exception as e:
            st.error(f"⚠️ Model prediction failed: {e}")
