import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from utils.config import ConfigManager
from utils.custom_logger import LoggerManager

# Initialize config and logger
config = ConfigManager()
logger = LoggerManager.get_logger()

def pytest_addoption(parser):
    """
    Add command-line options for test configuration
    """
    parser.addoption(
        "--browser", 
        action="store", 
        default="chrome", 
        help="Specify browser: chrome or firefox"
    )
    parser.addoption(
        "--env", 
        action="store", 
        default="prod", 
        help="Specify environment: prod or staging"
    )

@pytest.fixture(scope="session")
def config_data():
    """
    Fixture to provide configuration data across tests
    """
    return {
        'url': config.get('ENVIRONMENTS', 'prod_url'),
        'timeout': config.get_int('DEFAULT', 'timeout', 10),
        'browser': config.get('DEFAULT', 'browser', 'chrome')
    }

@pytest.fixture(scope="function")
def driver(request):
    """
    Fixture to initialize and manage WebDriver
    """
    # Get browser from command-line or config
    browser = request.config.getoption("--browser").lower()
    
    # WebDriver setup
    if browser == 'chrome':
        chrome_options = ChromeOptions()
        # Add Chrome-specific options
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-extensions')
        
        # Ensure the ChromeDriver is the correct version
        # service = Service(ChromeDriverManager(version="latest").install())
        service = Service(executable_path='./chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=chrome_options)
        yield driver
        driver.quit()
    
    elif browser == 'firefox':
        firefox_options = FirefoxOptions()
        # Add Firefox-specific options
        firefox_options.add_argument('-start-maximized')
        
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
    
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    # Set implicit wait
    driver.implicitly_wait(10)
    
    # Navigate to base URL
    base_url = config.get('ENVIRONMENTS', 'prod_url')
    driver.get(base_url)
    
    # Log browser and URL
    logger.info(f"Initializing {browser.upper()} WebDriver")
    logger.info(f"Navigating to {base_url}")
    
    yield driver
    
    # Cleanup
    driver.quit()
    logger.info("WebDriver closed")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture test status and take screenshot on failure
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == 'call' and report.failed:
        # Create screenshots directory
        screenshots_dir = os.path.join(os.getcwd(), 'screenshots')
        os.makedirs(screenshots_dir, exist_ok=True)
        
        # Get driver from fixture if available
        driver = item.funcargs.get('driver')
        
        if driver:
            # Generate screenshot filename
            screenshot_filename = os.path.join(
                screenshots_dir, 
                f'{item.name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            )
            
            # Take screenshot
            driver.save_screenshot(screenshot_filename)
            logger.error(f"Test failed. Screenshot saved: {screenshot_filename}")