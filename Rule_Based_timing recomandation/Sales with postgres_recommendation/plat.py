import streamlit as st
import datetime

# Define product-category-to-platform mappings
PRODUCT_CATEGORIES = {
    "Fashion": ["WeChat", "Weibo", "Xiaohongshu"],
    "Electronics": ["WeChat", "Weibo", "Douyin"],
    "Beauty": ["Xiaohongshu", "Douyin", "Weibo"],
    "Home Goods": ["WeChat", "Weibo"],
    "Toys & Games": ["Weibo", "Douyin", "Bilibili"],
    "Sports & Outdoor": ["WeChat", "Weibo"],
    "Books & Stationery": ["WeChat", "Weibo", "Bilibili"],
    "Luxury Goods": ["WeChat", "Xiaohongshu"],
    "Automotive": ["WeChat", "Weibo"],
    "Food & Beverages": ["WeChat", "Weibo", "Douyin"]
}

# Define best posting times for each platform
POSTING_TIMES = {
    "WeChat": {"weekday": "8 AM - 10 AM", "weekend": "9 AM - 11 AM"},
    "Weibo": {"weekday": "11 AM - 1 PM", "weekend": "10 AM - 12 PM"},
    "Douyin": {"weekday": "12 PM - 1 PM", "weekend": "7 PM - 9 PM"},
    "Xiaohongshu": {"weekday": "11 AM - 1 PM", "weekend": "8 PM - 10 PM"},
    "Bilibili": {"weekday": "8 PM - 11 PM", "weekend": "7 PM - 11 PM"}
}

# Define China shopping festivals
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
    "Men’s Festival": "04-24",  
    "Suning's 418 Shopping Festival": "04-08",
    "520 'I Love You' Day": "05-20",
    "Children’s Day": "06-01",
}

def is_festival_near(selected_date):
    """
    Check if a shopping festival is within the next 7 days or today, and return its name and date.
    """
    selected_date_obj = datetime.datetime.strptime(selected_date, "%Y-%m-%d")
    upcoming_festivals = []

    current_year = selected_date_obj.year
    for festival, date_str in CHINA_SHOPPING_FESTIVALS.items():
        festival_date = datetime.datetime.strptime(f"{current_year}-{date_str}", "%Y-%m-%d")
        days_diff = (festival_date - selected_date_obj).days

        # If the festival is today
        if days_diff == 0:
            upcoming_festivals.append(f"{festival} is today!")
        
        # If the festival is within the next 7 days
        elif 0 < days_diff <= 7:
            upcoming_festivals.append(f"{festival} is near! ({festival_date.strftime('%Y-%m-%d')})")

    return upcoming_festivals

def recommend_posting_time(product_category, date):
    """
    Recommend the best platforms and posting times for a given product category and date.
    """
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
    day_type = "weekend" if date_obj.weekday() >= 5 else "weekday"
    day_name = "Weekend" if date_obj.weekday() >= 5 else "Weekday"

    if product_category not in PRODUCT_CATEGORIES:
        return {}, []

    recommended_platforms = PRODUCT_CATEGORIES[product_category]
    recommendations = {}

    for platform in recommended_platforms:
        time_slot = POSTING_TIMES.get(platform, {}).get(day_type, "No data available")
        recommendations[platform] = time_slot

    # Check for upcoming shopping festivals
    upcoming_festivals = is_festival_near(date)

    return recommendations, upcoming_festivals, day_name

# Streamlit UI
st.title("📢 Best Time & Platform for Product Posting in China")

# Select product category
selected_category = st.selectbox("Select Product Category", list(PRODUCT_CATEGORIES.keys()))

# Select date
selected_date = st.date_input("Select Posting Date", datetime.date.today())

if st.button("Get Recommendations"):
    recommendations, upcoming_festivals, day_name = recommend_posting_time(selected_category, selected_date.strftime("%Y-%m-%d"))

    # Display the festivals section first
    if upcoming_festivals:
        st.subheader("⚡ Upcoming Festivals ⚡")
        for festival in upcoming_festivals:
            st.warning(festival)

    st.subheader(f"📌 Recommended Best Social Media Platforms & Times for '{selected_category}' Products to Post on {selected_date}:")
    
    # Display whether the selected date is a weekday or weekend
    st.markdown(f"**Selected Date:** {selected_date} ({day_name})")

    if recommendations:
        for platform, time in recommendations.items():
            st.markdown(f"✅ **{platform}**: {time}")
    else:
        st.warning("No recommendations available for this category.")
