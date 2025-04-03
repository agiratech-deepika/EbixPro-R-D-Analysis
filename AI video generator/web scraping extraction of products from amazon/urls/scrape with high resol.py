# import os
# import requests
# import streamlit as st
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# import time
# from webdriver_manager.chrome import ChromeDriverManager
# from PIL import Image

# # Function to create a folder for saving images and videos
# def create_folder(folder_name):
#     if not os.path.exists(folder_name):
#         os.makedirs(folder_name)

# # Function to download files (images/videos)
# def download_file(url, folder, file_name):
#     try:
#         response = requests.get(url, stream=True)
#         response.raise_for_status()
#         file_path = os.path.join(folder, file_name)
#         with open(file_path, 'wb') as file:
#             for chunk in response.iter_content(chunk_size=8192):
#                 file.write(chunk)
#         return file_path  # Return the file path for display in Streamlit
#     except Exception as e:
#         st.error(f"Error downloading {url}: {e}")
#         return None

# # Function to scrape Amazon product details
# def scrape_amazon_product(url):
#     # Chrome setup for Selenium
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--disable-blink-features=AutomationControlled")
#     chrome_options.add_argument("--log-level=3")
    
#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=chrome_options)
#     driver.get(url)
#     time.sleep(3)  # Wait for page to load
    
#     # Extract Product Name
#     try:
#         product_name = driver.find_element(By.ID, "productTitle").text.strip()
#     except Exception:
#         product_name = "N/A"

#     # Extract Description
#     try:
#         description_elements = driver.find_elements(By.ID, "productDescription")
#         descriptions = list(set([desc.text.strip() for desc in description_elements if desc.text.strip()]))
#         final_description = descriptions[0] if descriptions else "N/A"
#     except Exception:
#         final_description = "N/A"

#     # Extract Product Image URLs
#     image_urls = []
#     try:
#         images = driver.find_elements(By.CSS_SELECTOR, "div#altImages img[src*='images']")
#         image_urls = [img.get_attribute("src") for img in images if "https://" in img.get_attribute("src")]
#     except Exception as e:
#         st.error(f"Error extracting images: {e}")

#     driver.quit()

#     # Create folder for storing images
#     folder_name = "downloaded_images"
#     create_folder(folder_name)

#     # Download images
#     image_paths = []
#     for i, img_url in enumerate(image_urls, start=1):
#         img_file_name = f"product_image_{i}.jpg"
#         img_path = download_file(img_url, folder_name, img_file_name)
#         if img_path:
#             image_paths.append(img_path)

#     return {
#         "Product Name": product_name,
#         "Description": final_description,
#         "Image URLs": image_urls,
#         "Image Paths": image_paths,
#     }

# # Streamlit UI
# st.set_page_config(page_title="Amazon Product Scraper", layout="wide")
# st.title("Amazon Product Scraper")

# # Input for Amazon product URL
# product_url = st.text_input("Enter Amazon Product URL:")

# if st.button("Extract Product Details"):
#     if product_url:
#         with st.spinner("Scraping product details..."):
#             product_data = scrape_amazon_product(product_url)

#         # Display Product Name and Description
#         st.subheader("Product Name")
#         st.write(product_data["Product Name"])

#         st.subheader("Description")
#         st.write(product_data["Description"])

#         # Display Images in Grid Layout
#         st.subheader("Product Images")
#         if product_data["Image Paths"]:
#             cols = st.columns(len(product_data["Image Paths"]))  # Create columns dynamically
#             for i, img_path in enumerate(product_data["Image Paths"]):
#                 with cols[i]:
#                     st.image(Image.open(img_path), use_column_width=True)
#         else:
#             st.write("No images found.")
#     else:
#         st.error("Please enter a valid Amazon product URL.")


import os
import requests
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

# Function to create a folder for saving images and videos
def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

# Function to download files (images/videos)
def download_file(url, folder, file_name):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        file_path = os.path.join(folder, file_name)
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        return file_path  # Return the file path for display in Streamlit
    except Exception as e:
        st.error(f"Error downloading {url}: {e}")
        return None

# Function to scrape Amazon product details
def scrape_amazon_product(url):
    # Chrome setup for Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--log-level=3")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    time.sleep(3)  # Wait for page to load
    
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
        st.error(f"Error extracting images: {e}")

    # Extract Product Video URL (if available)
    video_url = None
    try:
        video_element = driver.find_element(By.CSS_SELECTOR, "video source")
        video_url = video_element.get_attribute("src") if video_element else None
    except Exception:
        video_url = None  # No video found

    driver.quit()

    # Create folder for storing images & videos
    folder_name = "downloaded_content"
    create_folder(folder_name)

    # Download images
    image_paths = []
    for i, img_url in enumerate(image_urls, start=1):
        img_file_name = f"product_image_{i}.jpg"
        img_path = download_file(img_url, folder_name, img_file_name)
        if img_path:
            image_paths.append(img_path)

    # Download video (if available)
    video_path = None
    if video_url:
        video_path = download_file(video_url, folder_name, "product_video.mp4")

    return {
        "Product Name": product_name,
        "Description": final_description,
        "Image URLs": image_urls,
        "Image Paths": image_paths,
        "Video URL": video_url,
        "Video Path": video_path,
    }

# Streamlit UI
st.set_page_config(page_title="Amazon Product Scraper", layout="wide")
st.title("Amazon Product Scraper")

# Input for Amazon product URL
product_url = st.text_input("Enter Amazon Product URL:")

if st.button("Extract Product Details"):
    if product_url:
        with st.spinner("Scraping product details..."):
            product_data = scrape_amazon_product(product_url)

        # Display Product Name and Description
        st.subheader("Product Name")
        st.write(product_data["Product Name"])

        st.subheader("Description")
        st.write(product_data["Description"])

        # Display Images in Grid Layout
        st.subheader("Product Images")
        if product_data["Image Paths"]:
            cols = st.columns(len(product_data["Image Paths"]))  # Create columns dynamically
            for i, img_path in enumerate(product_data["Image Paths"]):
                with cols[i]:
                    st.image(Image.open(img_path), use_column_width=True)
        else:
            st.write("No images found.")

        # Display Video (if available)
        st.subheader("Product Video")
        if product_data["Video Path"]:
            st.video(product_data["Video Path"])
        else:
            st.write("No video found.")
    else:
        st.error("Please enter a valid Amazon product URL.")
