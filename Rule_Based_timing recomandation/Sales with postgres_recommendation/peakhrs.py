import streamlit as st
from datetime import datetime, timedelta

# # List of Major Chinese Shopping Festivals
# CHINA_SHOPPING_FESTIVALS = {
#     "Chinese New Year Sales": "2024-02-10",
#     "618 Shopping Festival": "2024-06-18",
#     "Double 11 (Singles' Day)": "2024-11-11",
#     "Double 12": "2024-12-12",
#     "National Day Sales": "2024-10-01",
#     "Mid-Autumn Festival": "2024-09-17",
#     "Women’s Day": "2024-03-08",
#     "Mother’s Day": "2024-05-12",
#     "Black Friday": "2024-11-29",
#     "Labor Day": "2024-05-01",
#     "Valentine’s Day": "2024-02-14",
# }

CHINA_SHOPPING_FESTIVALS = {
    "Chinese New Year Sales": "2024-02-10",
    "618 Shopping Festival": "2024-06-18",
    "Double 11 (Singles' Day)": "2024-11-11",
    "Double 12": "2024-12-12",
    "National Day Sales": "2024-10-01",
    "Mid-Autumn Festival": "2024-09-17",
    "Women’s Day": "2024-03-08",
    "Mother’s Day": "2024-05-12",
    "Black Friday": "2024-11-29",
    "Labor Day": "2024-05-01",
    "Valentine’s Day": "2024-02-14",
    "Qixi Festival (Chinese Valentine's Day)": "2024-08-09",  # Added Qixi Festival
    "Singles' Day (Double 11)": "2024-11-11",  # Double-check for extended festivals
    "99 Wine Festival": "2024-09-09",  # New addition
}

# # Category-specific Peak Posting Hours
# CATEGORY_PEAK_TIMES = {
#     "Electronics": {"weekday": "12 PM - 2 PM", "evening": "8 PM - 10 PM"},
#     "Fashion": {"weekday": "1 PM - 3 PM", "evening": "7 PM - 9 PM"},
#     "Home Goods": {"weekday": "12 PM - 2 PM", "evening": "8 PM - 10 PM"},
#     "Toys & Games": {"weekday": "3 PM - 5 PM", "evening": "6 PM - 9 PM"},
#     "Beauty": {"weekday": "11 AM - 1 PM", "evening": "7 PM - 9 PM"},
#     "Books & Stationery": {"weekday": "12 PM - 2 PM", "evening": "7 PM - 9 PM"},
#     "Sports & Outdoor": {"weekday": "12 PM - 2 PM", "evening": "6 PM - 8 PM"},
#     "Health & Wellness": {"weekday": "10 AM - 12 PM", "evening": "7 PM - 9 PM"},
# }

CATEGORY_PEAK_TIMES = {
    "Electronics": {"weekday": "12 PM - 2 PM", "evening": "8 PM - 10 PM"},
    "Fashion": {"weekday": "1 PM - 3 PM", "evening": "7 PM - 9 PM"},
    "Home Goods": {"weekday": "12 PM - 2 PM", "evening": "8 PM - 10 PM"},
    "Toys & Games": {"weekday": "3 PM - 5 PM", "evening": "6 PM - 9 PM"},
    "Beauty": {"weekday": "11 AM - 1 PM", "evening": "7 PM - 9 PM"},
    "Books & Stationery": {"weekday": "12 PM - 2 PM", "evening": "7 PM - 9 PM"},
    "Sports & Outdoor": {"weekday": "12 PM - 2 PM", "evening": "6 PM - 8 PM"},
    "Health & Wellness": {"weekday": "10 AM - 12 PM", "evening": "7 PM - 9 PM"},
    "Luxury Goods": {"weekday": "12 PM - 2 PM", "evening": "7 PM - 9 PM"},
    "Automotive": {"weekday": "10 AM - 12 PM", "evening": "8 PM - 10 PM"},
    "Food & Beverages": {"weekday": "12 PM - 2 PM", "evening": "6 PM - 8 PM"},
}

# Function to check if the given date is near a shopping festival
def get_best_posting_time(input_date, category):
    """
    Determines the best time to post a product based on whether the date falls near a major
    Chinese shopping festival or a regular weekday/weekend and considers the product category.
    
    :param input_date: (str) Date in "YYYY-MM-DD" format
    :param category: (str) Category of the product being posted
    :return: (str) Recommended posting time
    """
    date_obj = datetime.strptime(input_date, "%Y-%m-%d")
    
    # Check if the date is near a shopping festival (within 3 days before)
    for festival, festival_date in CHINA_SHOPPING_FESTIVALS.items():
        festival_obj = datetime.strptime(festival_date, "%Y-%m-%d")

        if festival_obj.month == date_obj.month and festival_obj.day == date_obj.day:
            return f"{festival} is today! Recommended peak posting hours for {category}: 9 AM - 11 AM & 7 PM - 12 AM."

        if festival_obj - timedelta(days=3) <= date_obj <= festival_obj:
            return f"{festival} is near! Recommended peak posting hours for {category}: 9 AM - 11 AM & 7 PM - 12 AM."

    # If category exists in CATEGORY_PEAK_TIMES, use it to get recommended hours
    category_times = CATEGORY_PEAK_TIMES.get(category, CATEGORY_PEAK_TIMES["Electronics"])  # Default to Electronics if unknown category

    # Check if the given date is a weekend (Saturday/Sunday)
    if date_obj.weekday() in [5, 6]:  # 5 = Saturday, 6 = Sunday
        return f"Weekend detected! Recommended posting times for {category}: {category_times['evening']} (Evening)."

    # If it's a weekday (Monday - Friday)
    return f"Weekday detected! Recommended posting times for {category}: {category_times['weekday']} (Lunch) or {category_times['evening']} (After Work)."

# Streamlit App Layout
st.title("Best Time to Post Product Recommendations")
st.write("This tool helps e-commerce platform sellers determine the best times to post their products based on the product category and date.")

# Input for date and product category
input_date = st.date_input("Enter the Date for Posting (YYYY-MM-DD)", datetime.today())
category = st.selectbox("Select Product Category", ["Electronics", "Fashion", "Home Goods", "Toys & Games", "Beauty", "Books & Stationery", "Sports & Outdoor", "Health & Wellness"])

# When the user presses the button, calculate the best time to post
if st.button("Get Best Posting Time"):
    # Convert the date from date_input to string
    input_date_str = input_date.strftime("%Y-%m-%d")
    
    # Get the recommended posting time
    recommended_time = get_best_posting_time(input_date_str, category)
    
    # Display the result
    st.subheader(f"Recommended Posting Time for {category} on {input_date_str}:")
    st.write(recommended_time)

