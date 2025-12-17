import os
import time
import shutil
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# -------------------------
# CONFIG
# -------------------------
IMAGE_DIR = "image_paths"
os.makedirs(IMAGE_DIR, exist_ok=True)

# -------------------------
# UTILS
# -------------------------
def sanitize_filename(text):
    """Remove forbidden characters from filename."""
    return "".join(c for c in text if c.isalnum() or c in "._-")

# -------------------------
# MAIN FUNCTION
# -------------------------
def download_image(search_term):
    """Use undetected Selenium to download the first Google image directly to disk."""
    filename = sanitize_filename(search_term) + ".jpg"
    filepath = os.path.join(IMAGE_DIR, filename)
    
    if os.path.exists(filepath):
        print(f"Already exists: {filename}")
        return filepath

    
    driver = uc.Chrome(version_main=142)

    try:
        driver.get("https://www.google.com")
        time.sleep(1)

        
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        # Click Images tab (your XPath)
        images_tab = driver.find_element(By.XPATH, "//a//span[contains(text(),'Images')]")
        images_tab.click()
        time.sleep(2)

        # Click first image to preview
        try :
            first_img = driver.find_element(By.XPATH, '(//img)[9]')
            first_img.click()
        except:
            first_img = driver.find_element(By.XPATH, '(//img)[8]')
            first_img.click()

        
        input('check the xpath')
        # Get full-size image src
        img_url = first_img.get_attribute("src")

        # in this part use butful soop to download it 
        r = requests.get(img_url, stream=True)
        if r.status_code == 200:
            with open(filepath, "wb") as f:
                shutil.copyfileobj(r.raw, f)
            print(f"Downloaded: {filename}")
            return filepath
        else:
            print(f"Failed to download image for: {search_term}")
            return None

    except Exception as e:
        print(f"Error downloading {search_term}: {e}")
    finally:
        driver.quit()


def download_images_for_data(data_to_upload, limit=False):
    items = data_to_upload if not limit else data_to_upload[:2]
    for item in items:
        search_term = f"{item['brand']} {item['name']}"
        download_image(search_term)


if __name__ == "__main__":
    from data_extract import extract_data
    data_to_upload = extract_data("data.xls")
    download_images_for_data(data_to_upload, limit=True)

