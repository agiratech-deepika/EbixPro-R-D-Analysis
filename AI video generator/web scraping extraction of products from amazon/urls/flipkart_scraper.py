from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from selenium.common.exceptions import TimeoutException


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def download_file(url, folder_name, file_name):
    try:
        # Using requests to download the image
        import requests
        response = requests.get(url)
        with open(os.path.join(folder_name, file_name), 'wb') as file:
            file.write(response.content)
        return True
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False

# def scrape_flipkart_product(product_url):
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")  # Run headless browser (without UI)
#     chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
#     # Start the driver
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#     driver.get(product_url)
    
#     # Wait for the page to load and necessary elements to appear
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.VU-ZEz")))
    
#     # Extract Product Name
#     try:
#         product_name = driver.find_element(By.CSS_SELECTOR, "span.VU-ZEz").text.strip()
#     except Exception as e:
#         product_name = f"Product name not found: {e}"
    
#     # Extract Description
#     try:
#         description_elements = driver.find_elements(By.CSS_SELECTOR, "div._1mXcCf, div._2v7lu1")
#         descriptions = list(set([desc.text.strip() for desc in description_elements if desc.text.strip()]))
#         final_description = descriptions[0] if descriptions else "No description available"
#     except Exception:
#         final_description = "No description available"
    
#     # Extract Image URLs
#     image_urls = []
#     try:
#         images = driver.find_elements(By.CSS_SELECTOR, "div._2r2iyk img[src*='images']")
#         image_urls = [img.get_attribute("src") for img in images if "https://" in img.get_attribute("src")]
#     except Exception as e:
#         print(f"Error extracting images: {e}")
    
#     # Flipkart typically doesn't offer video URLs for products
#     video_url = None
    
#     driver.quit()
    
#     # Download images
#     folder_name = "downloaded_flipkart_files"
#     create_folder(folder_name)
    
#     image_files = []
#     for i, img_url in enumerate(image_urls, start=1):
#         img_file_name = f"product_image_{i}.jpg"
#         if download_file(img_url, folder_name, img_file_name):
#             image_files.append(os.path.join(folder_name, img_file_name))
    
#     # Return the product data as a dictionary
#     return {
#         "Product Name": product_name,
#         "Description": final_description,
#         "Image Files": image_files,
#         "Video URL": video_url if video_url else "No video available"
#     }

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def scrape_flipkart_product(product_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless browser (without UI)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(product_url)

    # Initialize variables to default values
    product_name = "Product name not found"
    product_description = "Product description not found"
    
    try:
        # Increased wait time and ensuring element is visible
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.VU-ZEz")))
        
       
        # Extract Product Name
        try:
            product_name = driver.find_element(By.CSS_SELECTOR, "span.VU-ZEz").text.strip()
        except Exception as e:
            product_name = f"Product name not found: {e}"
        
        # Extract Product Description
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.cPHDOP.col-12-12 .pqHCzB")))
        product_description = driver.find_element(By.CSS_SELECTOR, "div.cPHDOP.col-12-12 .pqHCzB").text.strip()
    
    except TimeoutException as e:
        print("Timeout while waiting for elements: ", e)
    
    driver.quit()
    
    return {
        "Product Name": product_name,
        "Product Description": product_description
    }


# Example URL for a Flipkart product
flipkart_url = "https://www.flipkart.com/fastrack-revoltt-fs1-1-85-advanced-blazing-fast-ui-working-crown-aivoice-assistant-ip68-smartwatch/p/itm94125c1b4eb6a?pid=SMWH44FUPGVB7CT5&lid=LSTSMWH44FUPGVB7CT5N3WFII&marketplace=FLIPKART&store=ajy%2Fbuh&srno=b_1_14&otracker=browse&fm=organic&iid=c7e22a96-1d5b-4725-8c7f-c514aeab64bf.SMWH44FUPGVB7CT5.SEARCH&ppt=browse&ppn=browse&ssid=epfgty7i9s0000001739796771599"
# flipkart_url = "https://www.flipkart.com/atcx-cotton-chef-s-apron-medium/p/itm13dbe6284f99a?pid=APRGJFDQBPFHRTHH&lid=LSTAPRGJFDQBPFHRTHH3MFFL4&marketplace=FLIPKART&store=jra%2Fiwp&srno=b_1_1&otracker=nmenu_sub_Home%20%26%20Furniture_0_Kitchen%20%26%20Table%20Linen&fm=factBasedRecommendation%2FrecentlyViewed&iid=en__4O3yLUk4E5V1uZWZ2kJQ4ELnStdmSo1OGuH55e0Gw94pCx8wigOnx0tPgoxTyz-pYLKPZd7woJZZs5Kbnes3g%3D%3D&ppt=browse&ppn=browse&ssid=n0pushpi7k0000001739862178290"
product_data = scrape_flipkart_product(flipkart_url)
print(product_data)
