# selenium_scraper.py

# Importing necessary modules and classes for Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

# Importing pandas for data manipulation
import pandas as pd

# Importing numpy for handling NaN (Not a Number) values
from numpy import nan


class FinancialDataScraper:
    """
    A class for scraping financial data from NASDAQ using Selenium.

    This class provides methods to initiate a Selenium WebDriver session, navigate
    to the NASDAQ website, and scrape financial data for a specific company based
    on its stock symbol. It handles the intricacies of web navigation, element 
    location, and data extraction, presenting the final data in a structured format.

    Attributes:
        driver_path (str): The file path to the Chrome WebDriver executable.
        browser (webdriver.Chrome): Instance of the Chrome WebDriver, used for web scraping.

    Methods:
        start_browser: Initiates a Chrome browser session using Selenium WebDriver.
        close_browser: Safely closes the Selenium WebDriver session.
        get_elements_text: Retrieves text from web elements found using a specified XPath.
        scrape_company_data: Scrapes financial data for a given company symbol from NASDAQ.
    """

    def __init__(self, driver_path):
        """
        Initializes the scraper with the path to the Chrome WebDriver.

        Args:
            driver_path (str): The file path to the Chrome WebDriver executable.
        """
        self.driver_path = driver_path
        self.browser = None

    def start_browser(self):
        """
        Starts a Chrome browser session using Selenium WebDriver.

        The method initiates a Chrome browser instance which can be used
        for navigating and scraping web pages.
        """
        service = Service(self.driver_path)
        self.browser = webdriver.Chrome(service=service)

    def close_browser(self):
        """
        Closes the current Chrome browser session.

        This method safely shuts down the Selenium WebDriver session.
        """
        if self.browser is not None:
            self.browser.quit()

    def get_elements_text(self, xpath):
        """
        Retrieves the text content of elements found using a specified XPath.

        This method searches for elements on the current webpage based on the
        provided XPath. It returns the text contents of these elements.

        Args:
            xpath (str): The XPath string used to locate the elements.

        Returns:
            list: A list containing the text of each element found. If no elements
            are found, returns a list with four NaN values.
        """
        try:
            elements = self.browser.find_elements(By.XPATH, xpath)
            return [element.text for element in elements if element.text != ""]
        except NoSuchElementException:
            return [nan] * 4

    def scrape_company_data(self, symbol):
        """
        Scrapes financial data for a specified company from the NASDAQ website.

        This method navigates to the NASDAQ website for the given company symbol,
        waits for the financial data to load, and then scrapes the relevant
        information, such as quarterly financial data.

        Args:
            symbol (str): The stock symbol of the company.

        Returns:
            pd.DataFrame: A DataFrame containing the scraped financial data. If no data
            is found or a timeout occurs, an empty DataFrame is returned.
        """
        url = f"http://www.nasdaq.com/symbol/{symbol}/financials?query=income-statement&data=quarterly"

        self.start_browser()

        # Navigate to the financials page
        self.browser.get(url)

        # Data storage
        data = {"company": symbol, "quarter": [], "total_revenue": []}

        try:
            # Wait for the financial data to load
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "tr.financials__row"))
            )

            # Scrape data
            quarters = self.get_elements_text(
                "//thead/tr[th[1][text() = 'Quarter:']]/th[position()>=3]"
            )
            total_revenue = self.get_elements_text(
                "//tr[th[text() = 'Total Revenue']]/td"
            )

            if not quarters or not total_revenue:
                print(f"No data found for symbol: {symbol}")
                return pd.DataFrame()

            data["quarter"] = quarters
            data["total_revenue"] = total_revenue

        except TimeoutException:
            print(f"Timed out waiting for page to load for symbol: {symbol}")
            return pd.DataFrame()  # Return an empty DataFrame if timeout occurs

        finally:
            # Ensure the browser is closed even if an error occurs
            self.close_browser()

        # Convert to DataFrame
        df = pd.DataFrame(data)

        return df
