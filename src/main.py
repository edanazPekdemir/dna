from itertools import product
import logging
from time import sleep
from helpers import (
    select_branch,
    get_driver,
    button_click,
    enter_url,
    get_products_displayed,
    get_price,
    add_product_2_basket,
    get_basket_price,
    select_payment,
    enter_text
)
from globals import (
    URL,
    LANG_SELECTOR_BUTTON_XPATH,
    ENG_SELECT_OPT_XPATH,
    LANG_CONFIRM_BUTTON_XPATH,
    CAT_COMPUTERS_XPATH,
    LAPTOPS_XPATH,
    HI_2_LO_XPATH,
    DISPLAYED_ELEMENTS_XPATH,
    CAT_PHONES_XPATH,
    LO_2_HI_XPATH,
    MOBILE_PHONES_XPATH,
    ACCEPT_COOKIES_XPATH,
    BASKET_XPATH,
    CONFIRM_BASKET_BTN_XPATH,
    BASKET_DO_NO_ADD_ANYTHING_XPATH,
    PAYMENT_CONT_XPATH,
    AVOID_PREMIUM_POPUP_XPATH,
    EMAIL_TEXT_BOX_XPATH,
    PHONE_TEXT_BOX_XPATH,
    FINISH_ORDER_BTN_XPATH
)

logger = logging.getLogger(__name__)

def add_expensive_from_laptops(driver):

    button_click(driver, CAT_COMPUTERS_XPATH)
    button_click(driver, LAPTOPS_XPATH)
    button_click(driver, HI_2_LO_XPATH)
    products = get_products_displayed(driver, DISPLAYED_ELEMENTS_XPATH)
    add_product_2_basket(products[0])
    price = get_price(products[0])

    return price

def add_cheapest_from_phones(driver):

    enter_url(driver, URL)
    button_click(driver, CAT_PHONES_XPATH)
    button_click(driver, MOBILE_PHONES_XPATH)
    button_click(driver, LO_2_HI_XPATH)
    products = get_products_displayed(driver, DISPLAYED_ELEMENTS_XPATH)
    add_product_2_basket(products[0])
    price = get_price(products[0])

    return price

def confirm_basket(driver, price_expected):
    button_click(driver, BASKET_XPATH)
    price = get_basket_price(driver)

    if(price != price_expected):
        logger.error("Wrong total price!")
        exit(1)
    
    logger.info("Product total prices are correct")
    button_click(driver, CONFIRM_BASKET_BTN_XPATH)
    button_click(driver, BASKET_DO_NO_ADD_ANYTHING_XPATH)
    select_branch(driver)
    sleep(5)
    select_payment(driver)
    sleep(5) # wait for continue button to be activated
    button_click(driver, PAYMENT_CONT_XPATH)
    button_click(driver, AVOID_PREMIUM_POPUP_XPATH)
    enter_text(driver, "johndoe@gmail.com", EMAIL_TEXT_BOX_XPATH)
    sleep(2)
    enter_text(driver, "123456789", PHONE_TEXT_BOX_XPATH)
    #this line will create a real order on alza.cz
    #button_click(driver, FINISH_ORDER_BTN_XPATH)

def main():
    driver = get_driver()

    enter_url(driver, URL)
    button_click(driver, LANG_SELECTOR_BUTTON_XPATH)
    button_click(driver, ENG_SELECT_OPT_XPATH)
    button_click(driver, LANG_CONFIRM_BUTTON_XPATH)
    button_click(driver, ACCEPT_COOKIES_XPATH)

    exp_price = add_expensive_from_laptops(driver)
    cheapest_price = add_cheapest_from_phones(driver)
    tot_price = exp_price + cheapest_price
    
    confirm_basket(driver, tot_price)
    logger.info("Order placed successfully test service will be terminated in 10 seconds ")
    sleep(10)
    driver.quit()

if __name__ == "__main__":
    main()
