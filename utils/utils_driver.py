import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service    

def initialise_selenium_driver():
    options = uc.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    prefs = {
        "profile.managed_default_content_settings.images": 2
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--lang=en-US")
    options.add_argument(r'--user-data-dir=C:\Users\jagadish\AppData\Local\Google\Chrome\User Data\Default')
    driver = uc.Chrome(service=Service(), options=options)
    
    return driver


