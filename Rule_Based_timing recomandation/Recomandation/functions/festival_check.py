import datetime
from utils import CHINA_SHOPPING_FESTIVALS

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



# import datetime
# import chinese_calendar as cn_cal

# def get_upcoming_chinese_festivals(selected_date):
#     """
#     Check for upcoming Chinese holidays within the next 5 days from the selected date.
#     If the festival is on the exact selected date, it will be listed as today.
#     """
#     selected_date_obj = datetime.date.fromisoformat(selected_date)
#     upcoming_festivals = []

#     for day_offset in range(6):  # Check today + next 5 days
#         check_date = selected_date_obj + datetime.timedelta(days=day_offset)
#         holiday_detail = cn_cal.get_holiday_detail(check_date)  # Correct method to get the holiday detail

#         if holiday_detail[0]:  # If it's a holiday
#             holiday_name = holiday_detail[1]  # Get the holiday name from the tuple

#             # Only add valid holiday names (filter out None values)
#             if holiday_name and holiday_name != 'None':
#                 # If it's the exact festival day, show it as today
#                 if day_offset == 0:
#                     upcoming_festivals.append(f"{holiday_name} is today! ({check_date})")
#                 else:
#                     upcoming_festivals.append(f"{holiday_name} is near! ({check_date})")

#     return upcoming_festivals

# # Example Usage
# selected_date = '2025-02-04'
# print(get_upcoming_chinese_festivals(selected_date))





