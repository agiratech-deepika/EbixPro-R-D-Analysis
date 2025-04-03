from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Setup Chrome options (optional)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in the background (no UI)

# Set the path to ChromeDriver
service = Service(r"C:\Users\Agira\chromedriver\chromedriver-win64\chromedriver.exe")  # Make sure chromedriver is in your system path

# Start WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open a webpage
driver.get("https://www.amazon.in")

# Print the page title
print("Page Title:", driver.title)

# Close the browser
driver.quit()
