import re
from bs4 import BeautifulSoup
from selenium import webdriver

# Define a regular expression to match valid URLs
URL_REGEX = re.compile(r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(:\d+)?(?:/[\w/\-?=%&]*)?$')

def validate_url(url):
    """
    Validates that the URL is valid.

    :param url: The URL to validate.
    :return: True if the URL is valid, False otherwise.
    """
    return bool(URL_REGEX.match(url))

def open_virtual_browser(url):
    """
    Open a virtual browser and navigate to a website.

    :param url: The URL of the website to navigate to.
    :return: None
    """
    # Set up the virtual browser
    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # Run the browser in headless mode (i.e., without a visible window)
    browser = webdriver.Chrome(options=options)

    # Navigate to the website
    print("Navigating to {}...".format(url))
    browser.get(url)

    # Web scraping using BeautifulSoup
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    page_title = soup.title.string if soup.title else 'No title found'
    paragraphs = [p.get_text() for p in soup.find_all('p')]

    # Print the page title and paragraphs
    print(f"Page title: {page_title}")
    print("Paragraphs:")
    for i, paragraph in enumerate(paragraphs, start=1):
        print(f"{i}. {paragraph}")

    # Close the browser when done
    browser.quit()