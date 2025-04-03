import streamlit as st
import datetime
# import lunarcalendar
from lunarcalendar import Converter, Solar, Lunar

# Define Moving Festivals (Lunar Calendar)
LUNAR_FESTIVALS = {
    "Chinese New Year": (1, 1),
    "Lantern Festival": (1, 15),
    "Qingming Festival": (3, 3),  # Special case (solar term)
    "Dragon Boat Festival": (5, 5),
    "Ghost Festival": (7, 15),
    "Qixi Festival (Chinese Valentine's Day)": (7, 7),
    "Mid-Autumn Festival": (8, 15),
    "Double Ninth Festival": (9, 9),
    "Laba Festival": (12, 8),
}

# Define Fixed Festivals (Gregorian Calendar)
FIXED_FESTIVALS = {
    "New Year's Day": "01-01",
    "Women's Day": "03-08",
    "Arbor Day": "03-12",
    "Labour Day": "05-01",
    "Children's Day": "06-01",
    "National Day": "10-01",
    "Christmas": "12-25",
}

# Convert Lunar Date to Gregorian
# def lunar_to_gregorian(year, lunar_month, lunar_day):
#     """Convert a lunar calendar date to a Gregorian date for the given year."""
#     return lunarcalendar.LunarDate(year, lunar_month, lunar_day).toSolarDate()
# Convert Lunar Date to Gregorian

def lunar_to_gregorian(year, lunar_month, lunar_day):
    """Convert a lunar calendar date to a Gregorian date for the given year."""
    try:
        lunar_date = Lunar(year, lunar_month, lunar_day, isleap=False)
        solar_date = Converter.Lunar2Solar(lunar_date)
        return solar_date.to_date()
    except Exception as e:
        st.warning(f"Error converting Lunar date ({year}-{lunar_month}-{lunar_day}): {e}")
        return None

# Get Upcoming Festivals within Next 30 Days
def get_upcoming_festivals(start_date):
    """Return all festivals occurring within the next 30 days from a given date."""
    year = start_date.year
    end_date = start_date + datetime.timedelta(days=30)

    upcoming_festivals = {}

    # Convert Lunar Festivals to Gregorian
    for name, (lunar_month, lunar_day) in LUNAR_FESTIVALS.items():
        try:
            festival_date = lunar_to_gregorian(year, lunar_month, lunar_day)
            if start_date <= festival_date <= end_date:
                upcoming_festivals[name] = festival_date
        except Exception as e:
            st.warning(f"Error converting {name}: {e}")

    # Add Fixed Festivals
    for name, date_str in FIXED_FESTIVALS.items():
        festival_date = datetime.datetime.strptime(f"{year}-{date_str}", "%Y-%m-%d").date()
        if start_date <= festival_date <= end_date:
            upcoming_festivals[name] = festival_date

    return upcoming_festivals


# Function to format the date output with weekday/weekend and colors
def format_date_with_weekday(date):
    """Format date with bold black date and color-coded weekday/weekend."""
    day_name = date.strftime("%A")  # Get full day name (e.g., Monday, Tuesday)
    is_weekend = day_name in ["Saturday", "Sunday"]
    day_type = "Weekend" if is_weekend else "Weekday"

    # Add color coding for weekdays and weekends
    color = "red" if is_weekend else "green"
    
    return f"<b style='color:black;'>{date.strftime('%Y-%m-%d')}</b> - <span style='color:{color}; font-weight:bold;'>{day_name} - {day_type}</span>"


# Streamlit App
# st.title("📅 Chinese Festivals Calendar")
st.markdown("<h1 style='color:blue;'>📅 Chinese Festivals Calendar</h1>", unsafe_allow_html=True)

# User Input: Start Date
input_date = st.date_input("Select a date", datetime.date.today())

# Find Festivals in the Next 30 Days
upcoming = get_upcoming_festivals(input_date)

# Display Results
if upcoming:
    st.markdown(f"<h4 style='color:grey;'>📆 Upcoming Festivals from {input_date} to {input_date + datetime.timedelta(days=30)}:</h4>", unsafe_allow_html=True)
    
    for festival, date in sorted(upcoming.items(), key=lambda x: x[1]):
        formatted_date = format_date_with_weekday(date)
        st.markdown(f"🗓️ **{festival}:** {formatted_date}", unsafe_allow_html=True)
else:
    st.write("No festivals found in the next 30 days.")