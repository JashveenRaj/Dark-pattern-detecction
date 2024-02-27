from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def highlight_elements(driver, words_to_highlight):
    # Get the current URL
    current_url = driver.current_url

    # Skip highlighting if the current URL is from google.com
    if current_url.startswith("https://www.google.com/"):
        return

    for word in words_to_highlight:
        # Find all elements containing the word
        elements_with_word = driver.find_elements(By.XPATH, f"//*[contains(text(), '{word}')]")

        # Highlight the parent div tag containing each element
        for element in elements_with_word:
            try:
                # Find the parent div tag of the element
                parent_div = element.find_element(By.XPATH, "./ancestor::div[1]")

                # Apply the background color directly to the parent div tag
                driver.execute_script("arguments[0].setAttribute('style', 'background: yellow; border: 2px solid red;');", parent_div)
            except Exception as e:
                print(f"An error occurred: {e}")

def main():
    # Set up the Chrome driver
    driver = webdriver.Chrome()
    
    # List of words or phrases to highlight
    words_to_highlight = ["Special Offer!", "hours", "Hurry", "Only", "few", "left", "Alicia Regis", "gift cards", "Almost gone", "Off","sold","watching","left at this price","Limited quantity available","have already sold"]

    try:
        while True:
            highlight_elements(driver, words_to_highlight)
            time.sleep(2)

    except KeyboardInterrupt:        
        print("Stopping the script.")

if __name__ == "__main__":
    main()
