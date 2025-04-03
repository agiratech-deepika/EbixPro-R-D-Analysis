from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def scrape_amazon_product(url):
    # Configure Chrome options to avoid detection
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run browser in headless mode
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass detection
    chrome_options.add_argument("--window-size=1920,1080")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=chrome_options)
    
    # Open the product page
    driver.get(url)
    time.sleep(5)  # Wait for elements to load

    # Extract product name
    try:
        product_name = driver.find_element(By.ID, "productTitle").text.strip()
    except:
        product_name = "Not found"

    # Extract product description
    try:
        description = driver.find_element(By.ID, "feature-bullets").text.strip()
    except:
        description = "Not found"

    # Extract all product images
    images = []
    try:
        image_elements = driver.find_elements(By.CSS_SELECTOR, "#altImages img")
        for img in image_elements:
            img_url = img.get_attribute("src").replace("_SS40_", "_SL1000_")  # Get high-resolution image
            images.append(img_url)
    except:
        images = ["No images found"]

    # Extract product video (if available)
    video_url = "No video available"
    try:
        video_element = driver.find_element(By.CSS_SELECTOR, "video")
        video_url = video_element.get_attribute("src")
    except:
        pass  # No video found

    # Close the browser
    driver.quit()

    # Return extracted data
    return {
        "Product Name": product_name,
        "Description": description,
        "Images": images,
        "Video URL": video_url
    }

# Example Amazon Product URL (You can replace this with any valid Amazon product link)
amazon_url = "https://www.amazon.in/SAF-flower-wall-painting-Decoration/dp/B0CYCHLB2L/"
product_data = scrape_amazon_product(amazon_url)

# Print the extracted data
print("Product Name:", product_data["Product Name"])
print("Description:", product_data["Description"])
print("Images:", product_data["Images"])
print("Video URL:", product_data["Video URL"])
