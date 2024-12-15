import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.homepage import HomePage

@pytest.fixture
def driver():
    # Setup ChromeDriver
    # service = Service(ChromeDriverManager().install())
    service = Service(executable_path='./chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    
    # Navigate to site
    driver.get('https://24h.pchome.com.tw/')
    
    yield driver
    
    # Teardown
    driver.quit()

def test_homepage_search(driver):
    home_page = HomePage(driver)
    home_page.search_product('iPhone')
    
    # Add assertions to verify search results
    assert 'iPhone' in driver.title