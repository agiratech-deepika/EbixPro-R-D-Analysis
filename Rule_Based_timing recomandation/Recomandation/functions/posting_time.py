import datetime
from utils import PRODUCT_CATEGORIES, POSTING_TIMES

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

    return recommendations, day_name
