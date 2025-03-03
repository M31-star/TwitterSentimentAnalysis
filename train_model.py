import pickle
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Download stopwords if not available
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Sample dataset (Replace this with actual dataset)
data = {
    "text": [
        "I love this product! It's amazing.",
        "Absolutely terrible, I hate it.",
        "Best experience ever, highly recommended!",
        "Worst thing I've bought. Waste of money.",
        "Not bad, could be better.",
    ],
    "sentiment": [1, 0, 1, 0, 1],  # 1 = Positive, 0 = Negative
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Preprocessing function
def clean_text(text):
    text = re.sub(r"[^a-zA-Z]", " ", text)  # Remove special characters
    text = text.lower().split()
    text = [word for word in text if word not in stop_words]
    return " ".join(text)

# Apply preprocessing
df["text"] = df["text"].apply(clean_text)

# Split data
X_train, X_test, y_train, y_test = train_test_split(df["text"], df["sentiment"], test_size=0.2, random_state=42)

# Create TF-IDF and Naive Bayes pipeline
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("model", MultinomialNB())
])

# Train the model
pipeline.fit(X_train, y_train)

# Save the trained model
with open("model.pkl", "wb") as model_file:
    pickle.dump(pipeline, model_file)

# Save the vectorizer
with open("vectorizer.pkl", "wb") as vectorizer_file:
    pickle.dump(pipeline.named_steps["tfidf"], vectorizer_file)

print("✅ Model and vectorizer saved successfully!")
