import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def highlight_text_on_page(url):
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome()

    # Open the webpage
    driver.get(url)

    # Define the pattern using regular expression
    pattern = r"In demand\.\s*\d+\s*people bought this in the last\s*\d+\s*hours\."

    # Find all elements containing the pattern and highlight them
    all_text_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'In demand.')]")

    for element in all_text_elements:
        if re.search(pattern, element.text):
            driver.execute_script("arguments[0].setAttribute('style', 'background-color: yellow;');", element)

    # Wait for a few seconds to see the highlighted text (adjust as needed)
    time.sleep(5)

    # Close the WebDriver
    driver.quit()

# List of URLs of the webpages you want to highlight the text on
urls = ["https://www.etsy.com/in-en/listing/1461977631/custom-couple-portrait-couple-drawing?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=personalized+gifts&ref=sc_gallery-1-1&pro=1&frs=1&bes=1&sts=1&search_preloaded_img=1&plkey=434b5cf46c85ac194d00749afe3dfbbd3e0063ee%3A1461977631", "https://www.etsy.com/in-en/listing/1569574696/faceless-portrait-custom-illustration?ga_order=most_relevant&ga_search_type=all&ga_view_type=gallery&ga_search_query=&ref=sc_gallery-1-1&pro=1&frs=1&plkey=75406ce318913878e666ecafa025d23d25e06f62%3A1569574696"]

# Highlight text on each page
for url in urls:
    highlight_text_on_page(url)
