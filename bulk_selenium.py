from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Load numbers
with open("numbers.txt", "r") as file:
    numbers = [line.strip() for line in file]

# Your message
message = "Hello! This is my test message with Selenium."

# Setup Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://web.whatsapp.com")

# Wait for you to scan QR code manually
print("Scan QR code and press Enter here...")
input()

# Send messages
for number in numbers:
    print(f"Sending to {number}...")
    driver.get(f"https://wa.me/{number}")
    time.sleep(5)

    # Click 'Continue to Chat'
    try:
        continue_button = driver.find_element(By.XPATH, "//a[contains(@href, 'send?phone')]")
        continue_button.click()
    except:
        print(f"Could not find Continue button for {number}. Skipping.")
        continue

    time.sleep(5)

    # Switch to WhatsApp web
    try:
        use_whatsapp = driver.find_element(By.XPATH, "//a[contains(@href, '/accept')]")
        use_whatsapp.click()
    except:
        pass  # Sometimes it goes straight to chat

    time.sleep(10)

    # Type and send the message
    try:
        msg_box = driver.find_element(By.XPATH, "//div[@title='Type a message']")
        msg_box.click()
        msg_box.send_keys(message)
        msg_box.send_keys(Keys.ENTER)
        print(f"Sent to {number}")
    except:
        print(f"Could not send to {number}")

    time.sleep(5)  # Wait before next

print("Done!")
driver.quit()