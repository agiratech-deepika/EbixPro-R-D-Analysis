import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

# Function to create a folder for saving images and videos
def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

# Function to download files (images/videos)
def download_file(url, folder, file_name):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check for successful request
        file_path = os.path.join(folder, file_name)
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded: {file_name}")
        return True  # Return True if download is successful
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False  # Return False if there is an error

# Function to extract video URL using JavaScript execution
def get_video_url(driver):
    try:
        # Try to find video URL using JavaScript execution
        video_url = driver.execute_script("""
            var video = document.querySelector('video');
            if (video && video.src) {
                return video.src;
            } else {
                return null;
            }
        """)
        return video_url
    except Exception as e:
        print("Error executing JavaScript:", e)
        return None

# Function to scrape the Amazon product page
def scrape_amazon_product(url):
    # Chrome setup for Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run without UI
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--log-level=3")
    
    # Setup ChromeDriver service
    service = Service(ChromeDriverManager().install())

    # Start Chrome WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    time.sleep(3)  # Wait for page to load
    
    # Extract Product Name
    product_name = driver.find_element(By.ID, "productTitle").text.strip()
    
    # Extract Description
    try:
        description = driver.find_element(By.ID, "productDescription").text.strip()
    except Exception:
        description = "N/A"
    
    # Extract Image URLs
    image_urls = []
    images = driver.find_elements(By.CSS_SELECTOR, "img[src*='images']")
    image_urls = [img.get_attribute("src") for img in images if "https://" in img.get_attribute("src")]
    
    # Extract Video URL (if any)
    video_url = get_video_url(driver)
    
    # Close the browser
    driver.quit()
    
    # Create a folder for downloading images and videos
    folder_name = "downloaded_files"
    create_folder(folder_name)
    
    # Download the images to local folder
    for i, img_url in enumerate(image_urls, start=1):
        img_file_name = f"image_{i}.jpg"
        download_file(img_url, folder_name, img_file_name)
    
    # Download the video (if available)
    if video_url:
        # If video URL is a blob URL, we need to extract the underlying URL
        if video_url.startswith("blob:"):
            print("Video URL is a blob URL. We need to inspect the actual network request or JavaScript to extract the real video URL.")
            # You can print the blob URL here if needed
            print("Blob Video URL:", video_url)
        else:
            video_file_name = "product_video.mp4"
            is_downloaded = download_file(video_url, folder_name, video_file_name)
            if is_downloaded:
                print("Video Downloaded Successfully!")
            else:
                print("Failed to Download Video.")

    # Return the extracted data
    return {
        "Product Name": product_name,
        "Description": description,
        "Image URLs": image_urls,
        "Video URL": video_url if video_url else "No video available"
    }

# Example usage
product_url = "https://www.amazon.in/SAF-flower-wall-painting-Decoration/dp/B0CYCHLB2L/"
product_data = scrape_amazon_product(product_url)

# Print extracted details
print("Product Name:", product_data["Product Name"])
print("Description:", product_data["Description"])
print("Image URLs:", product_data["Image URLs"])
print("Video URL:", product_data["Video URL"])
