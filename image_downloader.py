import os
import time
import base64
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

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

    print('starting the web service')
    driver = uc.Chrome(version_main=142)
    print('loaded the diver')
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
        except:
            first_img = driver.find_element(By.XPATH, '(//img)[8]')

        
        input('check the xpath')
        # Get full-size image src
        img_url = first_img.get_attribute("src")


        # Split header and base64 data
        header, encoded = img_url.split(",", 1)

        # Decode base64
        image_bytes = base64.b64decode(encoded)

        # Save to file
        with open(f"image_paths/{search_term}.jpg", "wb") as f:
            f.write(image_bytes)

        print("Saved image successfully")

        

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

