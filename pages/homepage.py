from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_page = BasePage(driver)

    def search_product(self, query):
        search_input = (By.XPATH, '//*[@type="search"]')
        search_button = (By.XPATH, '//*[@data-regression="header_search_button"]')

        self.base_page.send_keys(search_input, query)
        self.base_page.click(search_button)