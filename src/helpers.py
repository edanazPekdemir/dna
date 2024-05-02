from math import e
from time import sleep
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
import logging
import re

from globals import PRICE_FIELD_XPATH
from globals import (
    BUY_BUTTON_XPATH,
    TOTAL_BASKET_PRICE_XPATH
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

def button_click(driver, xpath, timeout=30):
    try:
        button = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        button.click()
        logger.info(f"Button click successful XPATH:{xpath}")
    except ElementClickInterceptedException:
        # If the click is intercepted, scroll the button into view and try again
        logger.info("Click intercepted, attempting to scroll element into view and retry")
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        time.sleep(1)  # Add a slight delay to ensure JS events are processed
        button.click()
        logger.info(f"Button click successful XPATH:{xpath}")
    except TimeoutException:
        logger.error(f"Timed out while clicking xpath : {xpath}")
        exit(1)
    except Exception as e:
        logger.error(f"An error occurred while clicking xpath : {xpath} error : {e}")
        exit(1)

def enter_url(driver, url):
    logger.info(f"Entering {url}")
    driver.get(url)
    driver.maximize_window()
    sleep(1)

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # Ensure options is passed as a keyword argument explicitly
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver

def get_price(product):
    price_field = product.find_element(By.XPATH, PRICE_FIELD_XPATH)
    cleaned_price = re.sub(r'[^\d]', '', price_field.text)
    return int(cleaned_price)

def get_products_displayed(driver, xpath):
    sleep(5) # wait for products to load
    return driver.find_elements(By.XPATH, xpath)

def add_product_2_basket(product):
    try:
        sleep(1) # wait for products to load
        button_click(product, BUY_BUTTON_XPATH)
        sleep(1) # wait for products to load
        logger.info("product added to the basket")
    except Exception as e:
        logger.error(f"An error occurred while adding product to basket: {e}")

def get_basket_price(driver):
    try:
        price_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, TOTAL_BASKET_PRICE_XPATH))
        )
        price_str = price_field.text
        cleaned_price = re.sub(r'[^\d]', '', price_str)
        return int(cleaned_price)
    except TimeoutException:
        logger.error(f"Timed out while waiting xpath : {TOTAL_BASKET_PRICE_XPATH}")
        exit(1)
    except Exception as e:
        logger.error(f"An error occurred : {e}")
        exit(1)

def select_branch(driver):

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".deliveryContainer"))
        )

        # Find all delivery containers
        delivery_containers = driver.find_elements(By.CSS_SELECTOR, ".deliveryContainer")

        # Loop through each container and check if the delivery price is 'free'
        for container in delivery_containers:
            # Find the price span within this container
            price_span = container.find_element(By.CSS_SELECTOR, ".deliveryPrice")

            # Check if the delivery price text is 'free'
            if price_span.text.lower() == 'free':
                # If free, find the checkbox and click it
                container.click()
                logger.info("Delivery method selected")
                return
    except Exception as e:
        logger.error(f"An error occurred while selecting delivery method: {e}")
        exit(1)

def select_payment(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".paymentContainer"))
        )

        # Find all delivery containers
        delivery_containers = driver.find_elements(By.CSS_SELECTOR, ".paymentContainer")
        delivery_containers[1].click()
        logger.info("Payment method selected")
    except Exception as e:
        logger.error(f"An error occurred while selecting payment method: {e}")
        exit(1)

def enter_text(driver, text, xpath):
    textbox = driver.find_element(By.XPATH, xpath)
    if textbox.get_attribute("value") != "":
        textbox.clear()
    textbox.send_keys(text) 
    textbox.send_keys(Keys.ENTER) 
