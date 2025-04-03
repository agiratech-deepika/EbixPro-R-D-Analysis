import pandas as pd
import random

# Sample data for different customer behaviors and segments
data = {
    'Customer_Type': ['New', 'Returning', 'New', 'Returning', 'New'],
    'Discount': [10, 20, 25, 30, 15],
    'Time_Sensitivity': ['Limited Time', 'Flash Sale', 'Last Chance', '24 Hours Left', 'Hurry'],
    'Additional_Benefits': ['Free Shipping', 'Free Gift', 'Extra Points', 'Free Returns', 'Free Shipping'],
    'Product_Type': ['Electronics', 'Clothing', 'Furniture', 'Books', 'Beauty'],
    'Behavior': ['Browsed', 'Abandoned Cart', 'Idle Cart', 'Purchased', 'Returned'],
    'Consumption': ['High', 'Low', 'Medium', 'High', 'Low']
}

# Create DataFrame
df = pd.DataFrame(data)

# Define a function to generate promotional names based on customer behavior and segments
def generate_promo_name(row):
    customer_type = row['Customer_Type']
    discount = row['Discount']
    time_sensitivity = row['Time_Sensitivity']
    additional_benefit = row['Additional_Benefits']
    product_type = row['Product_Type']
    behavior = row['Behavior']
    consumption = row['Consumption']
    
    # Base template generation logic
    if time_sensitivity in ['Limited Time', 'Flash Sale', 'Last Chance']:
        urgency_phrase = f"Hurry! {time_sensitivity} – "
    else:
        urgency_phrase = f"Only {time_sensitivity} Left! "
    
    # Discount message
    discount_phrase = f"Get {discount}% off"
    
    # Additional benefit message
    benefit_phrase = f" + {additional_benefit}" if additional_benefit else ""
    
    # Targeted Message
    if customer_type == 'New':
        targeted_message = f"Just for You! "
    else:
        targeted_message = f"Exclusive for Returning Customers! "
    
    # Customize messages based on behavior and consumption
    if behavior == 'Browsed':
        behavior_message = "Still Thinking? "
    elif behavior == 'Abandoned Cart':
        behavior_message = "Complete Your Purchase Now! "
    elif behavior == 'Idle Cart':
        behavior_message = "Your Cart is Waiting – Act Fast! "
    elif behavior == 'Purchased':
        behavior_message = "Thank You for Your Purchase! "
    elif behavior == 'Returned':
        behavior_message = "We Miss You! Come Back and Save! "
    
    # Customize messages based on consumption power
    if consumption == 'High':
        consumption_message = "Enjoy Big Savings on Your Next Order!"
    elif consumption == 'Medium':
        consumption_message = "Shop More, Save More!"
    else:
        consumption_message = "Get Started with 10% Off Your Next Purchase!"

    # Complete promotional name
    promo_name = f"{targeted_message}{behavior_message}{urgency_phrase}{discount_phrase}{benefit_phrase} on {product_type} – {consumption_message}"
    
    return promo_name

# Apply the function to generate promotional names for each row
df['Promo_Name'] = df.apply(generate_promo_name, axis=1)

# Display the final dataset with generated promo names
print("\nGenerated Promotional Names:")
print(df[['Customer_Type', 'Behavior', 'Consumption', 'Promo_Name']])
