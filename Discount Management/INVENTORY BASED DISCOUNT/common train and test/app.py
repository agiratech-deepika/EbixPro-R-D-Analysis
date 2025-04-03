# # import streamlit as st
# # import gym
# # import numpy as np
# # import pandas as pd
# # from stable_baselines3 import PPO
# # from stable_baselines3.common.vec_env import DummyVecEnv
# # import os

# # # Load Dataset
# # DATASET_PATH = r"C:\Projects\EbixPro_AI_bot\Analysis\Discount Management\INVENTORY BASED DISCOUNT\Data\inventory_based_discount_dataset.csv"
# # MODEL_PATH = "discount_rl_model"

# # # Load and preprocess dataset
# # @st.cache_data
# # def load_data():
# #     df = pd.read_csv(DATASET_PATH)
    
# #     FEATURES = ["Product_ID", "Store_Admin_ID", "Product_Category", "Product_Name", 
# #                 "Product_Price", "Discount_Offered", "Stock_Availability", "Reorder_Threshold", 
# #                 "Average_Daily_Sales", "Days_of_Stock_Left", "Competitor_Price", 
# #                 "Customer_Interest_Score", "Historical_Discount_Impact", "Seasonality_Flag", 
# #                 "Day_of_Week", "Festive_Season"
# #                 ]
# #     df = df[FEATURES]

# #     # Convert Day_of_Week into numerical values
# #     days_mapping = {
# #         'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 
# #         'Friday': 4, 'Saturday': 5, 'Sunday': 6
# #     }
# #     df["Day_of_Week"] = df["Day_of_Week"].map(days_mapping)

# #     # Normalize only numerical features
# #     numeric_cols = [
# #         "Product_Price", "Discount_Offered", "Stock_Availability", "Reorder_Threshold",
# #         "Average_Daily_Sales", "Days_of_Stock_Left", "Competitor_Price", "Customer_Interest_Score",
# #         "Historical_Discount_Impact","Seasonality_Flag", "Festive_Season"]
# #     df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].min()) / (df[numeric_cols].max() - df[numeric_cols].min())
# #     print("Number of features in dataset:", len(df.columns))  # Should be 14

# #     return df

# # df = load_data()

# # # Define Custom Gym Environment
# # class InventoryDiscountEnv(gym.Env):
# #     def __init__(self, data):
# #         super(InventoryDiscountEnv, self).__init__()
# #         self.data = data.values
# #         self.current_step = 0
# #         self.action_space = gym.spaces.Box(low=0, high=30, shape=(1,), dtype=np.float32)
# #         # self.observation_space = gym.spaces.Box(low=0, high=1, shape=(len(df.columns) - 2,), dtype=np.float32)
# #         self.observation_space = gym.spaces.Box(low=0, high=1, shape=(self.data.shape[1] - 2,), dtype=np.float32)


# #     def reset(self):
# #         self.current_step = 0
# #         obs = self.data[self.current_step, 2:]
# #         print("Reset Observation Shape:", obs.shape)  # Should be (14,)
# #         return obs
    

# #     # def reset(self):
# #     #     self.current_step = 0
# #     #     return self.data[self.current_step, 2:]



# #     def step(self, action):
# #         discount = np.clip(action[0], 0, 30)
# #         reward = self.calculate_reward(self.current_step, discount)
# #         self.current_step += 1
# #         done = self.current_step >= len(self.data)
# #         obs = self.data[self.current_step, 2:] if not done else np.zeros(len(df.columns) - 2)
# #         return obs, reward, done, {}

# #     def calculate_reward(self, step, discount):
# #         row = self.data[step]
# #         sales = row[5]
# #         demand_score = row[8]
# #         revenue = sales * (1 - (discount / 100))
# #         stock_left = row[6]
# #         reward = (revenue * demand_score) - (stock_left * 0.1)
# #         if discount > 0:
# #             reward += 0.05 * discount
# #         return reward

# # # Train Model
# # def train_model():
# #     env = DummyVecEnv([lambda: InventoryDiscountEnv(df)])
    
# #     ppo_params = {
# #         "learning_rate": 0.0005,
# #         "n_steps": 4096,
# #         "batch_size": 128,
# #         "n_epochs": 15,
# #         "gamma": 0.98,
# #         "gae_lambda": 0.90,
# #         "clip_range": 0.15,
# #         "ent_coef": 0.05
# #     }

# #     model = PPO("MlpPolicy", env, verbose=1, **ppo_params)
# #     model.learn(total_timesteps=150000)
# #     model.save(MODEL_PATH)
# #     return model

# # # Load or Train Model
# # if os.path.exists(MODEL_PATH + ".zip"):
# #     model = PPO.load(MODEL_PATH)
# # else:
# #     model = train_model()

# # # Streamlit UI
# # st.title("🛒 Dynamic Discount Optimization")
# # st.write("Select a **Seller ID** and **Product** to get an optimized discount suggestion.")

# # # Dropdowns
# # seller_ids = df["Store_Admin_ID"].unique()
# # selected_seller = st.selectbox("Select Seller ID", seller_ids)

# # products = df[df["Store_Admin_ID"] == selected_seller]["Product_Name"].unique()
# # selected_product = st.selectbox("Select Product", products)

# # # Get Product Features
# # # if st.button("Get Discount Recommendation"):
# # #     product_data = df[(df["Store_Admin_ID"] == selected_seller) & (df["Product_Name"] == selected_product)]
    
# # #     if not product_data.empty:
# # #         obs = product_data.iloc[:, 2:].values[0]
# # #         action, _ = model.predict(obs)
# # #         discount_suggestion = round(action[0], 2)
# # #         st.success(f"Recommended Discount: {discount_suggestion}% for Product '{selected_product}'")
# # #     else:
# # #         st.warning("⚠️ Product data not found!")
# # if st.button("Get Discount Recommendation"):
# #     product_data = df[(df["Store_Admin_ID"] == selected_seller) & (df["Product_Name"] == selected_product)]
    
# #     if not product_data.empty:
# #         # Ensure only numeric columns are used
# #         obs = product_data.iloc[:, 2:].select_dtypes(include=[np.number]).values[0].astype(np.float32)

# #         action, _ = model.predict(obs)
# #         discount_suggestion = round(action[0], 2)
# #         st.success(f"Recommended Discount: {discount_suggestion}% for Product '{selected_product}'")
# #     else:
# #         st.warning("⚠️ Product data not found!")


# import streamlit as st
# import pandas as pd
# import numpy as np
# from stable_baselines3 import PPO

# # Load the trained model
# model_path = "discount_rl_model.zip"
# model = PPO.load(model_path)

# # Load dataset
# dataset_path = DATASET_PATH = r"C:\Projects\EbixPro_AI_bot\Analysis\Discount Management\INVENTORY BASED DISCOUNT\Data\inventory_based_discount_dataset.csv"
# df = pd.read_csv(dataset_path)

# # Filter relevant columns
# FEATURES = [
#     "Product_Price", "Discount_Offered", "Stock_Availability", "Average_Daily_Sales", 
#     "Days_of_Stock_Left", "Competitor_Price", "Customer_Interest_Score", 
#     "Historical_Discount_Impact", "Seasonality_Flag", "Festive_Season", "Day_of_Week"
# ]
# df = df[["Product_ID", "Store_Admin_ID"] + FEATURES]

# # Convert categorical 'Day_of_Week' into numerical values
# df["Day_of_Week"] = df["Day_of_Week"].astype('category').cat.codes

# # Streamlit UI
# st.title("AI-Powered Discount Recommendation System")

# # Select Store Admin ID
# store_admins = df["Store_Admin_ID"].unique()
# selected_admin = st.selectbox("Select Store Admin:", store_admins)

# # Filter products based on selected Store Admin
# filtered_products = df[df["Store_Admin_ID"] == selected_admin]["Product_ID"].unique()
# selected_product = st.selectbox("Select Product:", filtered_products)

# # Fetch product data
# if st.button("Get Discount Recommendation"):
#     product_data = df[(df["Store_Admin_ID"] == selected_admin) & (df["Product_ID"] == selected_product)]
    
#     if not product_data.empty:
#         obs = product_data.iloc[:, 2:].values.flatten()  # Extract features
#         obs = np.array(obs).reshape(1, -1)  # Reshape for model
        
#         # Predict optimal discount
#         discount, _ = model.predict(obs)
#         discount = np.clip(discount[0], 0, 30)  # Ensure within range

#         st.success(f"Recommended Discount: {round(discount, 2)}%")
#     else:
#         st.error("No data found for the selected product and store.")

# import streamlit as st
# import pandas as pd
# import numpy as np
# from stable_baselines3 import PPO

# # Load Trained Model
# model = PPO.load("discount_rl_model.zip")

# # Load Dataset
# dataset_path = r"C:\Projects\EbixPro_AI_bot\Analysis\Discount Management\INVENTORY BASED DISCOUNT\Data\inventory_based_discount_dataset.csv"
# df = pd.read_csv(dataset_path)

# # Filter relevant columns
# FEATURES = [
#     "Product_Price", "Stock_Availability", "Average_Daily_Sales",
#     "Days_of_Stock_Left", "Competitor_Price", "Customer_Interest_Score",
#     "Historical_Discount_Impact", "Seasonality_Flag", "Festive_Season", "Day_of_Week"
# ]
# df = df[["Product_ID", "Store_Admin_ID"] + FEATURES]

# # Encode categorical variables
# df["Day_of_Week"] = df["Day_of_Week"].astype('category').cat.codes
# df["Festive_Season"] = df["Festive_Season"].astype('category').cat.codes

# # Streamlit UI
# st.title("AI-Powered Discount Recommendation System")

# store_admins = df["Store_Admin_ID"].unique()
# selected_admin = st.selectbox("Select Store Admin:", store_admins)

# filtered_products = df[df["Store_Admin_ID"] == selected_admin]["Product_ID"].unique()
# selected_product = st.selectbox("Select Product:", filtered_products)

# if st.button("Get Discount Recommendation"):
#     product_data = df[(df["Store_Admin_ID"] == selected_admin) & (df["Product_ID"] == selected_product)]

#     if not product_data.empty:
#         obs = product_data.iloc[:, 2:].values.flatten()
#         obs = np.array(obs).reshape(1, -1)

#         # Predict Discount
#         discount, _ = model.predict(obs)
#         discount = np.clip(discount[0], 0, 30)  

#         st.success(f"Recommended Discount: {round(discount, 2)}%")
#     else:
#         st.error("No data found for the selected product and store.")
