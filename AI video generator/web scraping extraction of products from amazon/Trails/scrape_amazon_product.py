from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def scrape_amazon_product(url):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run without UI (optional)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--log-level=3")  # Suppress logs

    # Automatically download and use the correct ChromeDriver version
    service = Service(ChromeDriverManager().install())

    # Start Selenium WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open Amazon product page
    driver.get(url)
    time.sleep(3)  # Wait for the page to load

    # Get page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Extract product name
    try:
        product_name = soup.find("span", {"id": "productTitle"}).get_text(strip=True)
    except AttributeError:
        product_name = "N/A"

    # Extract product description
    try:
        description = soup.find("div", {"id": "productDescription"}).get_text(strip=True)
    except AttributeError:
        description = "N/A"

    # Extract all product images
    image_urls = []
    try:
        images = soup.select("img[src*='images']")  # Select all images
        image_urls = [img["src"] for img in images if "https://" in img["src"]]
    except Exception:
        pass

    # Extract product video (if available)
    video_url = None
    try:
        video_tag = soup.find("video")
        if video_tag:
            video_url = video_tag["src"]
    except Exception:
        pass

    # Close the browser
    driver.quit()

    # Return extracted data
    return {
        "Product Name": product_name,
        "Description": description,
        "Image URLs": image_urls,
        "Video URL": video_url if video_url else "No video available"
    }

# Example Usage
# product_url = "https://www.amazon.in/SAF-flower-wall-painting-Decoration/dp/B0CYCHLB2L/"
product_url = "https://www.amazon.in/HOMFIL-Kalpavriksha-Fengshui-Showpiece-Decoration/dp/B0DJNQ26QF/ref=sr_1_2_sspa?crid=1N0GRDED536VY&dib=eyJ2IjoiMSJ9.k_X44hceryfn0LDz45Ykp6Hz5cfNSEusy6fhzgSbIX5eqbxj7gcZyTOM7256EB9IoLVwJVDFRkkAAGWv6Xv0uw6QeGyMHJEAnQG3d_Eozfy78DBj3PCG7lAifEbi1zq_dCjoWO4iEj4HLQ_SEdfmuVMGZVT4A4S3tFcMpaenNLYVYxt94huHoJixegHeIeFhGf1UarH6q0DoM6wcVPtk0XlxBQM8wcIAjAyutYAvNhYtQouNDOK9-aB7i370bROXA49sACZdtj5uLjGDnurNhKvyiR_rgYK4iIsyl6eyf8E.4mvdCqfWSc9RI46BtXwfQ3dqr-gEiAlCSUfNHQjB0UY&dib_tag=se&keywords=home%2Bdecoration%2Bitems%2Bfor%2Bliving%2Broom&qid=1739432858&sprefix=home%2Caps%2C201&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1"
# product_url = "https://www.amazon.in/SAF-flower-wall-painting-Decoration/dp/B0CYCHLB2L/"
product_data = scrape_amazon_product(product_url)

# Print the extracted data
print("Product Name:", product_data["Product Name"])
print("Description:", product_data["Description"])
print("Image URLs:", product_data["Image URLs"])
print("Video URL:", product_data["Video URL"])
