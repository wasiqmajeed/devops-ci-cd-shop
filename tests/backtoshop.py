from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def test_local_site():
    # Setup the Chrome driver automatically
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Navigate to your locally hosted site
        print("Back to Shop test")
        driver.get("http://127.0.0.1:8081/")

        # Print the page title to verify connection
        print(f"Page Title: {driver.title}")

        # Keep the window open for 5 seconds to inspect
        time.sleep(1)
        view_item = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/div/a")
        view_item.click()

        time.sleep(1)
        back_to_homepage = driver.find_element(By.XPATH, "/html/body/div/div/div/div/a")
        back_to_homepage.click()
        time.sleep(2)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Always close the browser
        print("Closing browser.")
        driver.quit()

if __name__ == "__main__":
    test_local_site()

