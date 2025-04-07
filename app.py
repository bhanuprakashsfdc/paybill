from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
# Optional: for automating OS save dialog
# import pyautogui

# ----------- Get user input ------------
service_number = input("Enter your Service Number: ")
upi_id = input("Enter your UPI ID (e.g., XXX@ybl): ")
today = datetime.date.today().strftime('%Y-%m-%d')
filename = f"{service_number}_{today}.pdf"

# ----------- Setup Chrome driver with print to PDF -------------
options = webdriver.ChromeOptions()
prefs = {
    "printing.print_preview_sticky_settings.appState": '{"recentDestinations":[{"id":"Save as PDF","origin":"local"}],"selectedDestinationId":"Save as PDF","version":2}',
    "savefile.default_directory": "/Users/yourname/Downloads",  # CHANGE path on Mac/Windows/Linux
    "printing.default_destination_selection_rules": {"kind": "local", "namePattern": "Save as PDF"},
    "download.prompt_for_download": False,
}
options.add_experimental_option("prefs", prefs)
options.add_argument("--kiosk-printing")  # Enables silent printing

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ----------- Step 1: Open payment page --
url = "https://payments.billdesk.com/MercOnline/SPDCLController"
driver.get(url)
driver.maximize_window()
time.sleep(3)

try:
    # Enter service number
    driver.find_element(By.ID, "txtCustomerID").send_keys(service_number)
    print("✅ Service number entered. Please solve the captcha manually...")
    time.sleep(10)

    # Click first and second submit
    driver.find_element(By.ID, "submitButton").click()
    time.sleep(10)
    driver.find_element(By.NAME, "btn2").click()
    time.sleep(10)

    # UPI steps
    driver.find_element(By.CSS_SELECTOR, 'a[data-value="txtBankIDUPI-OTHER"]').click()
    time.sleep(10)
    driver.find_element(By.ID, "proceedForm").click()
    time.sleep(10)
    driver.find_element(By.ID, "confirmTrxn").click()
    time.sleep(10)
    upi_input = driver.find_element(By.ID, "vpAddress")
    upi_input.clear()
    upi_input.send_keys(upi_id)
    driver.find_element(By.ID, "validateUser").click()
    print("🚀 Final payment submitted.")

    # Wait for payment to complete and page to render print button
    time.sleep(120)
    
    # print_button = driver.find_element(By.ID, "printBtn")
    # print_button.click()
    # print("🖨️ Print button clicked (PDF Save dialog should open)")

    # Optional: simulate OS save using pyautogui (uncomment if needed)
    # time.sleep(3)
    # pyautogui.typewrite(filename)
    # pyautogui.press('enter')
    # print(f"💾 File saved as {filename}")

    #print("⏳ Waiting 10 minutes for user to confirm or complete file save...")
    #time.sleep(600)  # Wait for 10 minutes

    # Click "Make Another Payment"
    make_another_btn = driver.find_element(By.ID, "makePaymentBtn")
    make_another_btn.click()
    print("🔁 Ready for another payment...")

except Exception as e:
    print("❌ Error during automation:", e)

input("✅ Done. Press Enter to close browser manually...")
