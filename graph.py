import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the TSV dataset file
DATA_PATH = r"C:\Users\Jash Progs\Dark patterns\dataset.tsv"
pandas_df = pd.read_csv(DATA_PATH, sep='\t')

# Display the first few rows of the dataset
print(pandas_df.head())

# Plotting the count of each category
sns.countplot(x='Pattern Category', data=pandas_df)
plt.xticks(rotation=45)  # Rotate category labels for better readability
plt.tight_layout()  # Adjust layout to prevent labels from being cut off
plt.xlabel("Pattern Category")
plt.ylabel("Count")
plt.title("Count of Patterns in Each Category")
plt.savefig("pattern_category_count.png")  # Save the plot as an image file
plt.show()
