# selenium_scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import pandas as pd
from numpy import nan


class FinancialDataScraper:
    """
    This class provides methods to scrape financial data from NASDAQ using Selenium.
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
        Starts a browser session.
        """
        service = Service(self.driver_path)
        self.browser = webdriver.Chrome(service=service)

    def close_browser(self):
        """
        Closes the browser session.
        """
        if self.browser is not None:
            self.browser.quit()

    def get_elements_text(self, xpath):
        """
        Finds elements using the given XPath and returns their text.
        Args:
            xpath (str): The XPath to find the elements.
        Returns:
            list: A list containing the text of each element found.
        """
        try:
            elements = self.browser.find_elements(By.XPATH, xpath)
            return [element.text for element in elements if element.text != ""]
        except NoSuchElementException:
            return [nan] * 4

    def scrape_company_data(self, symbol):
        """
        Scrapes financial data for the given company symbol from NASDAQ.
        Args:
            symbol (str): The company's stock symbol.
        Returns:
            pd.DataFrame: A DataFrame containing the scraped data.
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
