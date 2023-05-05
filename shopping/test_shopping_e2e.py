import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@pytest.fixture
def browser():
    # Initialize the browser and navigate to Amazon Shopping
    driver = webdriver.Chrome()
    driver.get('https://www.amazon.com/')
    yield driver
    # Close the browser after the test has finished
    driver.quit()

def test_shopping_flow(browser):
    # Search for a product
    search_box = browser.find_element(By.ID, 'twotabsearchtextbox')
    search_box.send_keys('Python Programming')
    search_box.send_keys(Keys.RETURN)

    # Wait for search results to load and validate the search return
    search_results = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'search')))
    assert 'Python Programming' in browser.title

    # Choose a product from the list
    product_link = browser.find_element(By.LINK_TEXT, 'Python Programming: An Introduction to Computer Science, 3rd Ed.')
    product_link.click()

    # Add the product to cart
    add_to_cart_button = browser.find_element(By.ID, 'add-to-cart-button')
    add_to_cart_button.click()

    # Wait for the confirmation message of product added to cart
    added_items = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.ID, 'add-to-cart-confirmation-image')))
    
    # Go to cart after adding items
    go_to_cart_button = browser.find_element(By.ID, 'sw-gtc')
    go_to_cart_button.click()
    
    # Wait for the cart to update and validate the product list
    cart_items = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.a-truncate-cut')))
    assert any('Python Programming: An Introduction' in item.text for item in cart_items)
