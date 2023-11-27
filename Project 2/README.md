# Working With Web Data

## Description

This project is designed to demonstrate advanced data handling techniques in Python, including XML parsing, API interaction, web scraping, and data analysis. It consists of three main modules: `SitemapParser`, `StockDataCollector`, and a web scraping module encompassing `LinkScraper` and `DataScraper`.

## Installation


To install this package, follow these steps:

1. Clone the repository:
git clone https://github.com/anuzz999/DAV-5400.git

2. Navigate to the project directory:
cd DAV-5400/Project 2

3. Install the package:

python setup.py install

## Usage

Each module in this package serves a different purpose:

### SitemapParser

Used for parsing XML sitemaps from a specified domain.

Example usage:

python
from my_package.sitemap_parser import SitemapParser
parser = SitemapParser('https://example.com')
parser.start_parsing()


## Setup

### Obtaining an API Key

1. Go to the [Alpha Vantage website](https://www.alphavantage.co/support/#api-key) (or relevant site) and follow the instructions to obtain an API key.
2. Once you have your API key, you'll need to set it as an environment variable on your machine.

### Setting the Environment Variable

#### For Windows:
- Open the Start Search, type in "env", and choose "Edit the system environment variables".
- In the System Properties window, click on the "Environment Variables..." button.
- Under the "User variables" section, click "New...".
- Enter `ALPHA_VANTAGE_API_KEY` as the variable name and your API key as the value.

#### For macOS/Linux:
- Open your terminal.
- Add the following line to your `~/.bashrc`, `~/.zshrc`, or equivalent shell configuration file:
  ```bash
  export ALPHA_VANTAGE_API_KEY='your_api_key_here'


Web Scraping (LinkScraper and DataScraper)
Collects hyperlinks and detailed data from web pages.

Example usage:

from my_package.web_scraping import LinkScraper, DataScraper

# Initialize and use the LinkScraper and DataScraper as required

## Contributing
Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

# License
This project is licensed under the MIT License - see the LICENSE file for details.

# Author
Anuj Kumar Shah - ashah5@mail.yu.edu

# Acknowledgements
Thanks to Stefanie Molin's "Hands-On Data Analysis with Pandas" for guidance on building Python packages.



