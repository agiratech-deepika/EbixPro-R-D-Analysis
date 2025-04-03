import streamlit as st
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd

# Extended List of Major Chinese Shopping Festivals (ignoring the year)
CHINA_SHOPPING_FESTIVALS = {
    "Chinese New Year Sales": "02-10",
    "618 Shopping Festival": "06-18",
    "Double 11 (Singles' Day)": "11-11",
    "Double 12": "12-12",
    "National Day Sales": "10-01",
    "Mid-Autumn Festival": "09-17",
    "Women’s Day": "03-08",
    "Mother’s Day": "05-12",
    "Black Friday": "11-29",
    "Labor Day": "05-01",
    "Valentine’s Day": "02-14",
    "Qixi Festival (Chinese Valentine's Day)": "08-09",  
    "99 Wine Festival": "09-09",  
    "Men’s Festival": "04-24 to 04-26", 
    "Suning's 418 Shopping Festival": "04-08",
    "520 'I Love You' Day": "05-20",
    "Children’s Day": "06-01",
}

#Category-specific Peak Posting Hours
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
    input_month_day = date_obj.strftime("%m-%d")  # Get the month and day part of the input date
    
    # Check if the date is near a shopping festival (within 3 days before)
    for festival, festival_date in CHINA_SHOPPING_FESTIVALS.items():
        # If the festival date is a range, handle it differently
        if "to" in festival_date:
            start_date_str, end_date_str = festival_date.split(" to ")
            start_date_obj = datetime.strptime(start_date_str, "%m-%d")
            end_date_obj = datetime.strptime(end_date_str, "%m-%d")
            
            # Adjust the year to the same as the input date
            start_date_obj = start_date_obj.replace(year=date_obj.year)
            end_date_obj = end_date_obj.replace(year=date_obj.year)
            
            if start_date_obj <= date_obj <= end_date_obj:
                return f"{festival} is happening! Recommended peak posting hours for {category}: 9 AM - 11 AM & 7 PM - 12 AM."
        
        else:
            festival_month_day = festival_date  # Only consider month and day part
            
            # festivals directly (no year comparison, only month-day)
            if festival_month_day == input_month_day:
                return f"{festival} is today! Recommended peak posting hours for {category}: 9 AM - 11 AM & 7 PM - 12 AM."
            
            # Handle fixed-date festivals directly (no year comparison, only month-day)
            festival_obj = datetime.strptime(festival_date + "-2024", "%m-%d-%Y")

            # Check if the input date is within 3 days before the festival date
            festival_obj = festival_obj.replace(year=date_obj.year)  
            three_days_before_festival = festival_obj - timedelta(days=3)
            
            # Compare only month and day, ignore the year for both
            if three_days_before_festival.strftime("%m-%d") <= input_month_day <= festival_obj.strftime("%m-%d"):
                return f"{festival} is near! Recommended peak posting hours for {category}: 9 AM - 11 AM & 7 PM - 12 AM."

    # If category exists in CATEGORY_PEAK_TIMES, use it to get recommended hours
    category_times = CATEGORY_PEAK_TIMES.get(category, CATEGORY_PEAK_TIMES["Electronics"])  # Default to Electronics if unknown category

    # Check if the given date is a weekend (Saturday/Sunday)
    if date_obj.weekday() in [5, 6]:  # 5 = Saturday, 6 = Sunday
        return f"Weekend detected! Recommended posting times for {category}: {category_times['evening']} (Evening)."

    # If it's a weekday (Monday - Friday), check if the date is near a festival (pre-festival detection)
    return f"Weekday detected! Recommended posting times for {category}: {category_times['weekday']} (Lunch) or {category_times['evening']} (After Work)."

# Streamlit App Layout
st.title("Best Time to Post Product Recommendations")
st.write("This tool helps e-commerce platform sellers determine the best times to post their products based on the product category and date.")

# Input for date and product category
input_date = st.date_input("Enter the Date for Posting (YYYY-MM-DD)", datetime.today())
category = st.selectbox("Select Product Category", ["Electronics", "Fashion", "Home Goods", "Toys & Games", "Beauty", "Books & Stationery", "Sports & Outdoor", "Health & Wellness", "Luxury Goods", "Automotive", "Food & Beverages"])

# When the user presses the button, calculate the best time to post
if st.button("Get Best Posting Time"):
    # Convert the date from date_input to string
    input_date_str = input_date.strftime("%Y-%m-%d")
    
    # Get the recommended posting time
    recommended_time = get_best_posting_time(input_date_str, category)
    
    # Display the result
    st.subheader(f"Recommended Posting Time for {category} on {input_date_str}:")
    st.write(recommended_time)
