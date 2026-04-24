from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
import os

def test_local_site():
    # Setup the Chrome driver automatically
    # service = Service(ChromeDriverManager().install())
    # driver = webdriver.Chrome(service=service)

    try:
        SAUCE_USERNAME = os.environ.get('SAUCE_USERNAME')
        SAUCE_ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY')

        # Sauce Labs remote URL
        sauce_url = f"https://{SAUCE_USERNAME}:{SAUCE_ACCESS_KEY}@ondemand.us-west-1.saucelabs.com:443/wd/hub"

        # Configure Chrome options with Sauce Labs capabilities
        # chrome_options = ChromeOptions()
        # chrome_options = FirefoxOptions()
        chrome_options = EdgeOptions()
        # chrome_options = SafariOptions()
        # chrome_options = InternetExplorerOptions()
        chrome_options.set_capability("browserVersion", "145")
        chrome_options.set_capability("platformName", "Windows 11")
        # chrome_options.set_capability("webSocketUrl", True)
        # chrome_options.add_argument("--remote-allow-origins=*")

        # 3. Set this dictionary as the value for the "moz:firefoxOptions" capability
        # chrome_options.set_capability("moz:firefoxOptions", moz_firefox_options_dict)

        chrome_options.set_capability(
            "sauce:options",
            {
                "name": "Testing add to cart function",
                # "build": "Python-Selenium-SauceLabs",
                "username": SAUCE_USERNAME,
                "accessKey": SAUCE_ACCESS_KEY,
                # "seleniumVersion": '3.141.1', #3.14.0
                # "devTools": True,
                # "recordLogs": True,
                # "extendedDebugging": True,
                "tunnelName": "oauth-wasiq.wani-2032a_tunnel_name",
                "tunnelOwner": "oauth-wasiq.wani-2032a"
            }
        )

        # Initialize remote WebDriver
        driver = webdriver.Remote(
            command_executor=sauce_url,
            options=chrome_options
        )
        # Navigate to your locally hosted site
        print("Add to cart test")
        driver.get("http://download.oracle.com:8081/")

        # Print the page title to verify connection
        print(f"Page Title: {driver.title}")

        # Keep the window open for 5 seconds to inspect
        time.sleep(1)
        view_item = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div/div/a")
        view_item.click()

        time.sleep(1)
        add_to_cart = driver.find_element(By.XPATH, "/html/body/div/div/div/div/button")
        add_to_cart.click()
        time.sleep(1)
        driver.execute_script('sauce:job-result=passed') #Set the test status to pass

    except Exception as e:
        print(f"An error occurred: {e}")


    finally:
        # Always close the browser
        print("Closing browser.")
        driver.quit()

if __name__ == "__main__":
    test_local_site()

