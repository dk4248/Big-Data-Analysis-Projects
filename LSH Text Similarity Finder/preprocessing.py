import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import time
from tqdm import tqdm

def preprocess_text(text):

    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    # Step 1: Lowercasing
    text = text.lower()
    
    # Step 2: Remove special characters, digits, and punctuation using regex
    text = re.sub(r'[^a-z\s]', '', text)
    
    # Step 3: Tokenization
    tokens = word_tokenize(text)
    
    # Step 4: Remove stopwords
    tokens = [word for word in tokens if word not in stop_words]
    
    # Step 5: Lemmatization (optional but useful for reducing words to base form)
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    # Step 6: Join tokens back to form the preprocessed sentence
    preprocessed_text = ' '.join(tokens)
    
    return preprocessed_text

def preprocess(file_name, output_file):

    start_time = time.time()

    with open(file_name, 'r') as file:
        data = file.readlines()

    # Wrap the iteration over the data with tqdm for progress tracking
    preprocessed_data = [preprocess_text(text.strip()) + '\n' for text in tqdm(data, desc="Processing Docs", unit="doc")]

    with open(output_file, 'w') as file:
        file.writelines(preprocessed_data)

    print(f"Preprocessing completed in {time.time() - start_time:.2f} seconds. Preprocessed data saved to '{output_file}'")

