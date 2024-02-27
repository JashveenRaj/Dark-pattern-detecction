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

# Extract product names and "Almost gone" status from the webpage
products = soup.find_all(class_='dne-itemtile-title ellipse-2')
statuses = soup.find_all(class_='dne-itemcard-hotness itemcard-hotness-red dne-itemcard-hotness-with-badge')

# Combine product names and "Almost gone" status into single strings
text_lines = []
for product, status in zip(products, statuses):
    product_name = product.text.strip()
    status_text = status.text.strip()
    combined_text = f"{product_name} {status_text}"
    text_lines.append(combined_text)

# Test your model with the combined text content
predicted_labels = predict(text_lines)

# Print detected products with a sneaky marker indicating potential dark patterns
print("\nDetected Products with Potential Dark Patterns:")
for idx, (text, label) in enumerate(zip(text_lines, predicted_labels)):
    if 'Almost gone' in text:
        print(f"{idx+1}. {text} [Potential Dark Pattern]")  # Indicate potential dark pattern
    else:
        print(f"{idx+1}. {text}")
