import psycopg2
from datetime import datetime
import streamlit as st
from psycopg2 import OperationalError

# Connect to your PostgreSQL database
def get_db_connection():
    try:
        # Replace with your actual connection parameters
        connection = psycopg2.connect(
            dbname="event_date_china",  # Your database name
            user="postgres",  # Your username
            password="Deepika1630",  # Your password
            host="localhost",  # Or your host (IP address or domain)
            port="5432"  # Default PostgreSQL port
        )
        print("Connection successful")
        return connection  # Return the connection object
    except OperationalError as e:
        print(f"Error: {e}")
        return None  # Return None if connection fails

# Get sales events from the database
def get_sales_events(current_date):
    connection = get_db_connection()
    if connection is None:
        return []  # Return an empty list if connection fails

    cursor = connection.cursor()
    
    query = """
        SELECT event_name, month, day, product_focus 
        FROM ecommerce_sales_dates1
        WHERE month = %s OR (month < %s AND day >= %s)
    """
    cursor.execute(query, (current_date.month, current_date.month, current_date.day))
    sales_events = cursor.fetchall()
    cursor.close()
    connection.close()
    return sales_events

# Recommend best time to post based on sales event
def recommend_best_time_to_post(sales_events, current_date, category, post_date):
    best_time = ""
    close_events = []
    
    # Default recommendation for regular dates
    post_date_obj = datetime.strptime(post_date, "%Y-%m-%d")
    if post_date_obj.weekday() >= 5:  # Saturday (5) or Sunday (6)
        best_time = "Best time to post: 10 a.m. to 1 p.m. on weekends."
    else:
        best_time = "Best time to post: 9 a.m. to 2 p.m. on weekdays."
    
    for event in sales_events:
        event_name, event_month, event_day, product_focus = event
        event_date = datetime(current_date.year, event_month, event_day)
        days_until_event = (event_date - current_date).days
        
        # If the current date is within a week of the event, recommend posting during peak hours
        if abs(days_until_event) <= 7:
            close_events.append(event_name)
            best_time = f"Recommended posting time for '{event_name}' event: 10 a.m. to 2 p.m. on weekdays."
            if category.lower() in product_focus.lower():
                best_time = f"For your product category '{category}', best to post during peak hours: 10 a.m. to 2 p.m."
                
            # Display both weekday and weekend options
            best_time += f"\nFor weekends: 10 a.m. to 1 p.m."
    
    # If no event is found close, display general recommendation
    if not close_events:
        best_time = "For regular days, post during optimal times: 9 a.m. to 2 p.m. on weekdays. For weekends, try posting from 10 a.m. to 1 p.m."
    
    # Show if it's close to any event
    if close_events:
        event_list = ', '.join(close_events)
        best_time += f"\nThis posting time is close to the following events: {event_list}."
    
    return best_time

# Streamlit Interface
st.title("Best Time to Post Product Based on Ecommerce Sales Events")

# Input fields for current date and product category
current_date = st.date_input("Select Current Date", datetime.today())
category = st.selectbox("Select Product Category", ["Fashion", "Electronics", "Home Goods", "Sports", "Others"])

# Manually enter the date to check
post_date = st.date_input("Enter the Date for Posting", datetime.today())

# Get sales events from the database
sales_events = get_sales_events(current_date)

# Get best time recommendation
best_time = recommend_best_time_to_post(sales_events, current_date, category, str(post_date))

# Display the recommendation
st.write(best_time)
