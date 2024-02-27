import torch
from transformers import RobertaModel, RobertaTokenizer
from bs4 import BeautifulSoup
import requests

# Defining the model architecture
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

# Instantiate the model
model = RobertaClass()

# Load the model
model.load_state_dict(torch.load(r'C:\Users\Jash\OneDrive\Desktop\finalmodel2\pytorch_roberta_sentiment.bin', map_location=torch.device('cpu')))

# Define the inference function to accept multiple inputs
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

# Send a GET request to the eBay Global Deals webpage
url = 'https://www.ebay.com/globaldeals'
response = requests.get(url)

# Parse the HTML content of the webpage
soup = BeautifulSoup(response.text, 'html.parser')

# Extract product names and prices from the webpage
products = soup.find_all(class_='dne-itemtile-title ellipse-2')
prices = soup.find_all(class_='dne-itemcard-hotness itemcard-hotness-red dne-itemcard-hotness-with-badge')

# Extract text content and split it by lines
text_lines = []
for product, price in zip(products, prices):
    item_name = product.text.strip()
    item_price = price.text.strip()
    lines = f"{item_name}: {item_price}".split(':')
    text_lines.extend(lines)

# Test your model with the scraped text content
predicted_labels = predict(text_lines)

# Print scrapped text fed into the loaded model
print("\nScrapped text fed into the loaded model:")
for text, label in zip(text_lines, predicted_labels):
    if label == 0:
        print(f"\033[91m{text} | Predicted Label: dark pattern\033[0m")
    else:
        print(f"Text: {text} | Predicted Label: not a dark pattern")
