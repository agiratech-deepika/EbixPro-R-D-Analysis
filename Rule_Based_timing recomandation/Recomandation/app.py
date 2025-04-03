# import streamlit as st
# from functions.ai_caption_hashtags import generate_caption_and_hashtags
# from functions.posting_time import recommend_posting_time
# from functions.festival_check import is_festival_near
# from utils import PRODUCT_CATEGORIES, POSTING_TIMES
# from datetime import datetime

# # Streamlit UI for Product Posting and AI Caption & Hashtag suggestions
# st.set_page_config(page_title="Best Time & Platform for Product Posting in China", layout="wide")
# st.title("📢 Best Time & Platform for Product Posting in China with AI-Generated Captions & Hashtags")

# # Side Menu for User Input
# st.sidebar.title("Details on Product")
# selected_category = st.sidebar.selectbox("Select Product Category", list(PRODUCT_CATEGORIES.keys()))
# # product_description = st.sidebar.text_area("Enter Product Description", "Example: A stylish red dress perfect for summer!")
# product_description = st.sidebar.text_area("Enter Product Description", "", placeholder="Example: A stylish red dress perfect for summer!")
# selected_date = st.sidebar.date_input("Select Posting Date", datetime.now())

# # Placeholder for Results in the Main Area
# result_placeholder = st.empty()

# # Buttons for different functionalities
# button_ai_caption = st.sidebar.button("Get AI Caption & Hashtags")
# button_best_platform = st.sidebar.button("Get Best Platform & Timing")
# button_festival = st.sidebar.button("Get Upcoming Festival")

# # Function to display AI-generated caption and hashtags
# def show_ai_caption_and_hashtags():
#     caption, hashtags = generate_caption_and_hashtags(selected_category, product_description)
#     print(generate_caption_and_hashtags)
#     with result_placeholder.container():
#         st.subheader("📝 AI-Generated Caption:")
#         st.write(caption)
#         st.subheader("🔖 Suggested Hashtags:")
#         st.write(", ".join(hashtags))

# # Function to display best platform and timing
# def show_best_platform_and_timing():
#     recommendations, day_name = recommend_posting_time(selected_category, selected_date.strftime("%Y-%m-%d"))
#     with result_placeholder.container():
#         st.subheader(f"📌 Recommended Best Social Media Platforms & Times for '{selected_category}' Products to Post on {selected_date}:")
#         st.markdown(f"**Selected Date:** {selected_date} ({day_name})")
        
#         if recommendations:
#             for platform, time in recommendations.items():
#                 st.markdown(f"✅ **{platform}**: {time}")
#         else:
#             st.warning("No recommendations available for this category.")

# # Function to display festivals
# def show_upcoming_festivals():
#     upcoming_festivals = is_festival_near(selected_date.strftime("%Y-%m-%d"))
#     with result_placeholder.container():
#         if upcoming_festivals:
#             st.subheader("⚡ Upcoming Festivals ⚡")
#             for festival in upcoming_festivals:
#                 st.warning(festival)
#         else:
#             st.warning("No upcoming festivals within the next 7 days.")

# # Display content based on button clicks
# if button_ai_caption:
#     show_ai_caption_and_hashtags()

# elif button_best_platform:
#     show_best_platform_and_timing()

# elif button_festival:
#     show_upcoming_festivals()


import streamlit as st
from functions.ai_caption_hashtags import generate_caption_and_hashtags
from functions.posting_time import recommend_posting_time
from functions.festival_check import is_festival_near
from utils import PRODUCT_CATEGORIES, PRODUCT_LISTS
from datetime import datetime

# Streamlit UI for Product Posting
st.set_page_config(page_title="Best Time & Platform for Product Posting in China", layout="wide")
st.title("📢 Best Time & Platform for Product Posting in China with AI-Generated Captions & Hashtags")

# Side Menu for User Input
st.sidebar.title("Details on Product")

# Step 1: Select Product Category
selected_category = st.sidebar.selectbox("Select Product Category", list(PRODUCT_CATEGORIES.keys()))

# Step 2: Load Products Dynamically based on Category
if selected_category:
    products_in_category = PRODUCT_LISTS.get(selected_category, [])
    selected_product = st.sidebar.selectbox("Select Product", products_in_category)

# Step 3: Enter Product Description
product_description = st.sidebar.text_area("Enter Product Description", "", placeholder="Example: A stylish red dress perfect for summer!")

# Step 4: Select Posting Date
selected_date = st.sidebar.date_input("Select Posting Date", datetime.now())

# Placeholder for Results in the Main Area
result_placeholder = st.empty()

# Buttons for different functionalities
button_ai_caption = st.sidebar.button("Get AI Caption & Hashtags")
button_best_platform = st.sidebar.button("Get Best Platform & Timing")
button_festival = st.sidebar.button("Get Upcoming Festival")

# # Function to display AI-generated caption and hashtags
# def show_ai_caption_and_hashtags():
#     caption, hashtags,accuracy = generate_caption_and_hashtags(selected_product,selected_product,product_description)
#     with result_placeholder.container():
#         st.subheader(f"📝 AI-Generated Caption for '{selected_product}':")
#         st.write(caption)
#         st.subheader("🔖 Suggested Hashtags:")
#         st.write(", ".join(hashtags))
#         st.subheader(f"📝 AI-Generated Accuracy on Caption and Hastags':")
#         st.write(accuracy)

import streamlit as st

# Function to display AI-generated caption and hashtags
def show_ai_caption_and_hashtags():
    caption, hashtags, accuracy = generate_caption_and_hashtags(selected_product, selected_product, product_description)
    
    with result_placeholder.container():
        st.markdown(f"<h2 style='color:#4A90E2;'>📝 AI-Generated Caption for '{selected_product}':</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:20px;'>{caption}</p>", unsafe_allow_html=True)
        
        st.markdown(f"<h2 style='color:#4A90E2;'>🔖 Suggested Hashtags:</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:18px;'>{', '.join(hashtags)}</p>", unsafe_allow_html=True)
        
        st.markdown(f"<h2 style='color:#4A90E2;'>📊 AI-Generated Accuracy on Caption and Hashtags:</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:20px; font-weight:bold;'>{accuracy}%</p>", unsafe_allow_html=True)


# Function to display best platform and timing
def show_best_platform_and_timing():
    recommendations, day_name = recommend_posting_time(selected_category, selected_date.strftime("%Y-%m-%d"))
    with result_placeholder.container():
        st.subheader(f"📌 Best Social Media Platforms & Times for '{selected_product}' on {selected_date}:")
        st.markdown(f"**Selected Date:** {selected_date} ({day_name})")
        if recommendations:
            for platform, time in recommendations.items():
                st.markdown(f"✅ **{platform}**: {time}")
        else:
            st.warning("No recommendations available for this category.")

# Function to display upcoming festivals
def show_upcoming_festivals():
    upcoming_festivals = is_festival_near(selected_date.strftime("%Y-%m-%d"))
    with result_placeholder.container():
        if upcoming_festivals:
            st.subheader("⚡ Upcoming Festivals ⚡")
            for festival in upcoming_festivals:
                st.warning(festival)
        else:
            st.warning("No upcoming festivals within the next 7 days.")

# Display content based on button clicks
if button_ai_caption:
    show_ai_caption_and_hashtags()

elif button_best_platform:
    show_best_platform_and_timing()

elif button_festival:
    show_upcoming_festivals()
