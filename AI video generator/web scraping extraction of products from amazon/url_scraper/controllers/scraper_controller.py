import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from Models.product_model import ProductModel
from config import TEMP_FOLDER

def clear_temp_folder():
    """Delete all files in temp before new extraction"""
    for file in os.listdir(TEMP_FOLDER):
        os.remove(os.path.join(TEMP_FOLDER, file))

def download_file(url, folder, file_name):
    """Download image or video"""
    response = requests.get(url, stream=True)
    response.raise_for_status()
    file_path = os.path.join(folder, file_name)
    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    return file_path

def scrape_product(url):
    """Scrape product details from Amazon/Flipkart"""
    db = ProductModel()
    existing_product = db.get_product_by_url(url)

    if existing_product:
        return existing_product  # Return cached data

    clear_temp_folder()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(3)

    # Extract Product Name
    try:
        product_name = driver.find_element(By.ID, "productTitle").text.strip()
    except Exception:
        product_name = "N/A"

    # Extract Description
    try:
        description_elements = driver.find_elements(By.ID, "productDescription")
        descriptions = list(set([desc.text.strip() for desc in description_elements if desc.text.strip()]))
        final_description = descriptions[0] if descriptions else "N/A"
    except Exception:
        final_description = "N/A"

    # Extract Product Image URLs
    image_urls = []
    try:
        images = driver.find_elements(By.CSS_SELECTOR, "div#altImages img[src*='images']")
        image_urls = [img.get_attribute("src") for img in images if "https://" in img.get_attribute("src")]
    except Exception as e:
        print(f"Error extracting images: {e}")

    # Extract Product Video URL (if available)
    video_url = None
    try:
        video_element = driver.find_element(By.CSS_SELECTOR, "video source")
        video_url = video_element.get_attribute("src") if video_element else None
    except Exception:
        video_url = None  # No video found

    driver.quit()

    image_paths = [download_file(img_url, TEMP_FOLDER, f"image_{i}.jpg") for i, img_url in enumerate(image_urls)]
    video_path = download_file(video_url, TEMP_FOLDER, "video.mp4") if video_url else None

    product_data = {
        "given_url": url,
        "product_name": product_name,
        "description": final_description,
        "source": "Amazon",
        "image_url": image_urls,
        "video_url": video_url,
        "image_path": image_paths,
        "video_path": video_path,
    }

    db.insert_product(product_data)
    db.close()
    return product_data
