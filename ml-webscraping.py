from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import torch
from transformers import RobertaModel, RobertaTokenizer

class RobertaClass(torch.nn.Module):
    def __init__(self):
        super(RobertaClass, self).__init__()
        self.l1 = RobertaModel.from_pretrained("roberta-base")
        self.pre_classifier = torch.nn.Linear(768, 768)
        self.dropout = torch.nn.Dropout(0.3)
        self.classifier = torch.nn.Linear(768, 5)  # Assuming 5 classes

    def forward(self, input_ids, attention_mask, token_type_ids):
        output_1 = self.l1(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        hidden_state = output_1[0]
        pooler = hidden_state[:, 0]
        pooler = self.pre_classifier(pooler)
        pooler = torch.nn.ReLU()(pooler)
        pooler = self.dropout(pooler)
        output = self.classifier(pooler)
        return output

def predict(texts):
    tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
    inputs = tokenizer.batch_encode_plus(
        texts,
        add_special_tokens=True,
        max_length=256,
        pad_to_max_length=True,
        return_token_type_ids=True,
        return_tensors='pt',
        truncation=True
    )
    with torch.no_grad():
        outputs = model(inputs['input_ids'], inputs['attention_mask'], inputs['token_type_ids'])
    _, predicted = torch.max(outputs, 1)
    return predicted.tolist()

def highlight_elements(driver, words_to_highlight):
    # Get the current URL
    current_url = driver.current_url

    # Skip highlighting if the current URL is from google.com
    if current_url.startswith("https://www.google.com/"):
        return

    # Extract text content from the webpage
    page_text = driver.find_element(By.TAG_NAME, 'body').text
    
    # Predict labels for the extracted text
    predicted_labels = predict([page_text])
    
    # Highlight the text based on predicted labels
    for label, word in zip(predicted_labels, words_to_highlight):
        if label == 1:  # Assuming label 1 corresponds to highlighting
            elements_with_word = driver.find_elements(By.XPATH, f"//*[contains(text(), '{word}')]")
            for element in elements_with_word:
                try:
                    parent_div = element.find_element(By.XPATH, "./ancestor::div[1]")
                    driver.execute_script("arguments[0].setAttribute('style', 'background: yellow; border: 2px solid red;');", parent_div)
                except Exception as e:
                    print(f"An error occurred: {e}")

def main():
    # Set up the Chrome driver
    driver = webdriver.Chrome()
    
    # Load the pre-trained model
    model = RobertaClass()
    model.load_state_dict(torch.load(r'C:\Users\Lenovo\Desktop\pradarsh html\model.bin', map_location=torch.device('cpu')))
    
    # List of words or phrases to highlight
    words_to_highlight = ["Special Offer!", "hours", "Hurry", "Only", "few", "left", "55", "00", "Alicia Regis", "gift cards"]

    try:
        while True:
            driver.get("YOUR_WEBSITE_URL_HERE")
            time.sleep(2)  # Allow some time for the page to load
            highlight_elements(driver, words_to_highlight)

    except KeyboardInterrupt:        
        print("Stopping the script.")

if __name__ == "__main__":
    main()
