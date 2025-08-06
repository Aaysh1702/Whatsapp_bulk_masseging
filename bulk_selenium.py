from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import urllib.parse

# Load numbers
with open("numbers.txt", "r", encoding="utf-8") as file:
    numbers = [line.strip() for line in file]

# Your message
message = "Your message"

# Setup
options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\SeleniumProfile")
options.add_argument("--profile-directory=Default")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open WhatsApp Web
driver.get("https://web.whatsapp.com")
input("Scan QR and press ENTER when ready...")

# Loop
for number in numbers:
    encoded_message = urllib.parse.quote(message)
    url = f"https://web.whatsapp.com/send?phone={number}&text={encoded_message}"
    driver.get(url)
    print(f"Checking {number}...")

    try:
        wait = WebDriverWait(driver, 20)

        # Wait for either Send button or "invalid number" banner
        send_button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Send"]'))
        )
        
        # Click Send
        driver.execute_script(
            "document.querySelector('button[aria-label=\"Send\"]').click();"
        )
        print(f"Sent to {number}")

    except:
        # Check if error banner exists
        try:
            error_banner = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Phone number shared via URL is invalid')]"))
            )
            print(f"Skipped invalid number: {number}")
        except:
            print(f"Skipped {number} — reason unknown (slow net?)")

    time.sleep(2)

print("Done!")
driver.quit()
