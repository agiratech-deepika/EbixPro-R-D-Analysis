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

PRODUCT_LISTS = {
    "Fashion": ["Red Dress", "Leather Jacket", "Sneakers"],
    "Electronics": ["Smartphone", "Laptop", "Bluetooth Speaker"],
    "Beauty": ["Lipstick", "Moisturizer", "Perfume"],
    "Home Goods": ["Sofa", "Vacuum Cleaner", "Coffee Maker"],
    "Toys & Games": ["LEGO Set", "Board Game", "RC Car"],
    "Sports & Outdoor": ["Running Shoes", "Yoga Mat", "Bicycle"],
    "Books & Stationery": ["Notebook", "Fountain Pen", "Planner"],
    "Luxury Goods": ["Designer Bag", "Luxury Watch", "Gold Necklace"],
    "Automotive": ["Car Dash Cam", "GPS Navigator", "Car Air Purifier"],
    "Food & Beverages": ["Green Tea", "Chocolate Box", "Instant Noodles"]
}