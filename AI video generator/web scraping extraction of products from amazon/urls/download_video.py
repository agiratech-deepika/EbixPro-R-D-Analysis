import time
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Setup undetected Chrome driver with DevTools protocol enabled
options = uc.ChromeOptions()
options.add_argument("--headless=new")  # Optional: Run without opening a window
options.add_argument("--disable-blink-features=AutomationControlled")

# Enable the DevTools logging
capabilities = DesiredCapabilities.CHROME
capabilities['loggingPrefs'] = {'performance': 'ALL'}

driver = uc.Chrome(options=options, desired_capabilities=capabilities)

# Open Amazon product page
product_url = "https://www.amazon.in/dp/B0B5LTXD5H"  # Replace with actual product URL
driver.get(product_url)
time.sleep(5)  # Wait for the page to load

# Extract network logs
logs = driver.get_log('performance')

video_url = None
for entry in logs:
    message = entry['message']
    if '.mp4' in message:
        # Extract the video URL from the log entry
        start_idx = message.find('https://')
        end_idx = message.find('.mp4') + 4  # Add 4 to include .mp4
        video_url = message[start_idx:end_idx]
        print(f"Found video URL: {video_url}")
        break

if video_url:
    # Download the video
    response = requests.get(video_url, stream=True)
    with open("amazon_video.mp4", "wb") as video_file:
        for chunk in response.iter_content(chunk_size=1024):
            video_file.write(chunk)
    print("Download complete: amazon_video.mp4")
else:
    print("No video URL found.")

driver.quit()
