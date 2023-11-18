import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd


class LinkScraper:
    """
    A scraper that collects links from a given website. It navigates through specified
    classes to extract relevant hyperlinks.

    Attributes:
        base_url (str): The base URL from which the scraper will start scraping.
        class_names (list): A list of class names to find the links within the HTML content.
        df (DataFrame): A pandas DataFrame that stores the collected links.
    """

    def __init__(self, base_url, class_names):
        """
        Initializes the LinkScraper with a base URL and class names.

        Parameters:
            base_url (str): The starting URL for the scraper.
            class_names (list): Class names to guide the scraping process.
        """
        self.base_url = base_url
        self.class_names = class_names
        self.df = pd.DataFrame(columns=["Link"])

    def fetch_content(self, url):
        """
        Fetches the HTML content of a given URL.

        Parameters:
            url (str): The URL from which to fetch content.

        Returns:
            str: The HTML content of the page.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
        return ""

    def parse_for_links(self, content, class_name):
        """
        Parses the HTML content to extract links contained within elements of a specified class.

        Parameters:
            content (str): HTML content to be parsed.
            class_name (str): The class name within which to search for links.

        Returns:
            list: A list of hyperlinks extracted from the content.
        """
        soup = BeautifulSoup(content, "html.parser")
        containers = soup.find_all(class_=class_name)
        links = []
        for container in containers:
            a_tags = container.find_all("a")
            for a_tag in a_tags:
                href = a_tag.get("href")
                if href:
                    full_url = urljoin(self.base_url, href)
                    links.append(full_url)
        return links

    def scrape(self):
        """
        Initiates the scraping process from the base URL and collects links across multiple
        levels as specified by the class names.

        Returns:
            DataFrame: A DataFrame containing all the scraped links.
        """
        all_links = []
        # First level scraping
        content = self.fetch_content(self.base_url)
        cat_content_links = self.parse_for_links(content, self.class_names[0])

        # Second level scraping
        for link in cat_content_links[:1]:
            content = self.fetch_content(link)
            filter_content_links = self.parse_for_links(content, self.class_names[1])

            # Third level scraping
            for f_link in filter_content_links[:1]:
                content = self.fetch_content(f_link)
                paging_links = self.parse_for_links(content, self.class_names[2])

                # Fourth level scraping
                for p_link in paging_links:
                    content = self.fetch_content(p_link)
                    add_image_links = self.parse_for_links(content, self.class_names[3])
                    all_links.extend(
                        add_image_links
                    )  # Store all links from fourth level scraping

        # Create DataFrame
        self.df = pd.DataFrame(all_links, columns=["Link"])

    def save_to_csv(self, file_name):
        """
        Saves the collected links to a CSV file.

        Parameters:
            file_name (str): The name of the file to save the links.
        """
        if self.df.empty:
            print("DataFrame is empty. Please scrape data before saving to CSV.")
        else:
            self.df.to_csv(file_name, index=False)
            print(f"Data saved to {file_name}")

    def get_dataframe(self):
        """
        Retrieves the DataFrame containing the scraped links. If the DataFrame is empty,
        it initiates the scraping process.

        Returns:
            DataFrame: The DataFrame containing the scraped links.
        """
        if self.df.empty:
            self.scrape()
        return self.df


class DataScraper:
    """
    A scraper that extracts detailed data from each webpage given by the links.

    Attributes:
        data (list of dict): A list that stores all the extracted data points.
    """

    def __init__(self):
        """
        Initializes the DataScraper.
        """
        self.data = []

    def fetch_content(self, url):
        """
        Fetches the HTML content of a given URL.

        Parameters:
            url (str): The URL from which to fetch content.

        Returns:
            BeautifulSoup: The BeautifulSoup object of the page.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def clean_text(self, text):
        """
        Cleans and formats the text extracted from the HTML.

        Parameters:
            text (str): The text to clean.

        Returns:
            str: The cleaned text.
        """
        return " ".join(text.split()) if text else ""

    def scrape(self, soup):
        """
        Scrapes data from a BeautifulSoup object representing a webpage.

        Parameters:
            soup (BeautifulSoup): The BeautifulSoup object to scrape data from.

        Returns:
            dict: The extracted data.
        """
        if soup:
            description_elem = soup.find(itemprop="description")
            description_text = (
                self.clean_text(description_elem.text) if description_elem else ""
            )
            related_categories_elem = soup.select(".description p a")
            categories = (
                [self.clean_text(a.text) for a in related_categories_elem]
                if related_categories_elem
                else []
            )

            data = {
                "updated_date": self.clean_text(
                    soup.select_one(".updated-date").text.replace("Last Updated : ", "")
                )
                if soup.select_one(".updated-date")
                else "",
                "views": int(
                    self.clean_text(
                        soup.select_one(".visits").text.replace("views", "")
                    )
                )
                if soup.select_one(".visits")
                else 0,
                "description": description_text,
                "phone": self.clean_text(
                    soup.select_one('meta[itemprop="telephone"]')["content"]
                )
                if soup.select_one('meta[itemprop="telephone"]')
                else "",
                "email": self.clean_text(
                    soup.select_one('meta[itemprop="email"]')["content"]
                )
                if soup.select_one('meta[itemprop="email"]')
                else "",
                "website": self.clean_text(
                    soup.select_one('a[itemprop="url"]').get("href")
                )
                if soup.select_one('a[itemprop="url"]')
                else "",
                "reviews": self.clean_text(soup.select_one("#review .alert").text)
                if soup.select_one("#review .alert")
                else "No reviews posted",
                "related_categories": ", ".join(categories),
                "postal_code": self.clean_text(
                    soup.select_one('meta[itemprop="postalCode"]')["content"]
                )
                if soup.select_one('meta[itemprop="postalCode"]')
                else "",
                "fax_number": self.clean_text(
                    soup.select_one('meta[itemprop="faxNumber"]')["content"]
                )
                if soup.select_one('meta[itemprop="faxNumber"]')
                else "",
            }
            return data
        return {}

    def scrape_sites(self, sites_list):
        """
        Scrapes data from a list of websites.

        Parameters:
            sites_list (list of str): A list of URLs to scrape.
        """
        for url in sites_list:
            print(f"Scraping {url}")
            soup = self.fetch_content(url)
            scraped_data = self.scrape(soup)
            # print(scraped_data)
            if scraped_data:
                self.data.append(scraped_data)
            else:
                print(f"Failed to scrape data from {url}")

    def to_dataframe(self):
        """
        Converts the scraped data into a pandas DataFrame.

        Returns:
            DataFrame: The DataFrame containing the scraped data.
        """
        return pd.DataFrame(self.data)

    def save_to_csv(self, filename):
        """
        Saves the scraped data to a CSV file.

        Parameters:
            filename (str): The filename for the CSV where data will be saved.
        """
        df = self.to_dataframe()
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")


# Usage
# You will have to uncomment and fill in the base_url and class_names as per your requirement
# base_url = 'https://www.example.com/'
# class_names = ['class1', 'class2', 'class3', 'class4']
# scraper = LinkScraper(base_url, class_names)
# scraper.scrape()
# scraper.save_to_csv('scraped_links.csv')
