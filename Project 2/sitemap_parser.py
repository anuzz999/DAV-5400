import requests
import pandas as pd
from bs4 import BeautifulSoup
import os


class SitemapParser:
    def __init__(self, domain):
        """
        Initializes the SitemapParser.

        Parameters:
        domain (str): The domain to parse sitemaps from.
        """
        self.domain = domain
        self.sitemap_dataframes = {}

    def start_parsing(self):
        """
        Initiates the parsing process of sitemaps found in the domain's robots.txt.
        """
        self.get_all_sitemaps()

    def fetch_content(self, url):
        """
        Fetches content from a URL.

        Parameters:
        url (str): URL to fetch content from.

        Returns:
        str: Content of the page or an empty string if an error occurs.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching content from {url}: {e}")
            return ""

    def parse_sitemap(self, sitemap_url):
        """
        Parses the sitemap from a given URL and extracts URLs into a DataFrame.

        Parameters:
        sitemap_url (str): URL of the sitemap to parse.
        """
        xml_content = self.fetch_content(sitemap_url)
        if not xml_content:
            return

        soup = BeautifulSoup(xml_content, "xml")
        urls = [loc.text for loc in soup.find_all("loc")]
        for url in urls:
            if url.endswith(".xml"):
                self.parse_sitemap(url)

        self.create_dataframe(sitemap_url, urls)

    def create_dataframe(self, sitemap_url, urls):
        """
        Creates a DataFrame from a list of URLs and adds it to the sitemap_dataframes dictionary.

        Parameters:
        sitemap_url (str): URL of the sitemap being parsed.
        urls (list): List of URLs to include in the DataFrame.
        """
        df = pd.DataFrame(urls, columns=["URLs"])
        df = self.extract_subdirectories(df)
        key = self.generate_key(sitemap_url)
        self.sitemap_dataframes[key] = df

    def generate_key(self, sitemap_url):
        """
        Generates a unique key for the sitemap.

        Parameters:
        sitemap_url (str): URL of the sitemap.

        Returns:
        str: A unique key for the sitemap.
        """
        return os.path.basename(sitemap_url).split(".")[0]

    def get_all_sitemaps(self):
        """
        Fetches the robots.txt file from the domain and parses it to find sitemap URLs.
        Then, parses each sitemap URL found.
        """
        robots_txt_url = f"{self.domain}/robots.txt"
        robots_txt_content = self.fetch_content(robots_txt_url)

        if not robots_txt_content:
            print(f"No content found in {robots_txt_url}")
            return

        for line in robots_txt_content.splitlines():
            if line.startswith("Sitemap:"):
                sitemap_url = line.split("Sitemap:")[1].strip()
                self.parse_sitemap(sitemap_url)

    def extract_subdirectories(self, df):
        """
        Extracts subdirectories from the URLs in the DataFrame.

        Parameters:
        df (DataFrame): DataFrame with a column 'URLs' containing URLs.

        Returns:
        DataFrame: Updated DataFrame with subdirectory columns.
        """

        def extract(url):
            return url.replace(self.domain, "").strip("/").split("/")

        max_subdir = 0
        for index, row in df.iterrows():
            subdirs = extract(row["URLs"])
            max_subdir = max(max_subdir, len(subdirs))
            df.loc[index, [f"subdirectory{i+1}" for i in range(len(subdirs))]] = subdirs

        for i in range(max_subdir):
            df[f"subdirectory{i+1}"] = df[f"subdirectory{i+1}"].fillna("")

        return df

    def save_as_csv(self, directory="sitemaps"):
        """
        Saves all sitemap DataFrames to CSV files.

        Parameters:
        directory (str): Directory to save the CSV files in.
        """
        if not os.path.exists(directory):
            os.makedirs(directory)

        for key, df in self.sitemap_dataframes.items():
            filename = f"{key}.csv"
            filepath = os.path.join(directory, filename)
            df.to_csv(filepath, index=False)
            print(f"Saved: {filepath}")
