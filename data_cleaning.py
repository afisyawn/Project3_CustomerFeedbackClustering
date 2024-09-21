"""
Did this step on collab because it's less time consuming
"""

import pandas as pd
import numpy as np
from nlp_id.tokenizer import Tokenizer
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from nlp_id.stopword import StopWord
from nlp_id.lemmatizer import Lemmatizer
import emoji
import re
import json
import logging
from tqdm import tqdm

#Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize progress bar
tqdm.pandas()

#Define slang category
logging.info("Loading slang category dataset....")
with open("combined_slang_words.txt") as f:
    slang_dict = json.load(f)
logging.info(f"Dataset load with {len(slang_dict)} records")

#Read csv data and make new copy
logging.info("Loading dataset....")
df = pd.read_csv("document/gi_review_id.csv")
logging.info(f"Dataset load with {len(df)} records")
cleaned_data = df.copy()

#Data cleaning
logging.info("Starting data cleaning process....")

cleaned_data = cleaned_data.dropna(subset=["reviewId", "content", "at"])
cleaned_data["thumbsUpCount"].fillna(0, inplace=True)
cleaned_data.drop_duplicates(subset=["reviewId"], inplace=True)
cleaned_data = cleaned_data[cleaned_data["score"].between(1, 5)]
cleaned_data = cleaned_data[cleaned_data["thumbsUpCount"] <= 10_000]
cleaned_data["content"] = cleaned_data["content"].str.lower()
cleaned_data["appVersion"] = cleaned_data["appVersion"].astype(str)
cleaned_data["reviewCreatedVersion"] = cleaned_data["reviewCreatedVersion"].astype(str)
cleaned_data["at"] = pd.to_datetime(cleaned_data["at"], errors='coerce')
cleaned_data["repliedAt"] = pd.to_datetime(cleaned_data["repliedAt"], errors='coerce')

logging.info("Basic cleaning complete")


#Initialize token & make token from review
logging.info("Starting tokenization process...")
tokenizer = Tokenizer()
cleaned_data["content"] = cleaned_data["content"].apply(tokenizer.tokenize)
logging.info("Tokenization completed")
print(cleaned_data["content"].head())


#Stopword removal
def remove_stopwords(tokens):
    stopword = StopWord()
    return [word for word in tokens if word not in stopword.get_stopword()]

logging.info("Starting stopword removal....")
cleaned_data["content"] = cleaned_data["content"].apply(remove_stopwords)
logging.info("Stopword removal completed")
print(cleaned_data["content"].head())


#Replace slang word
def replace_slang(tokens):
    return [slang_dict.get(word, word) for word in tokens]

logging.info("Starting replace slang word....")
cleaned_data["content"] = cleaned_data["content"].apply(replace_slang)
logging.info("Replacing slang word completed")


#Lemmatization
logging.info("Starting lemmatization...")
lemmatizer = Lemmatizer()
cleaned_data["content"] = cleaned_data["content"].apply(lambda tokens: [lemmatizer.lemmatize(token) for token in tokens])
logging.info("Lemmatization completed")
print(cleaned_data["content"].head())


#Remove special char and digit
def clean_tokens(tokens):
    return [re.sub(r"[^\w\s]", "", re.sub(r"\d+", "", token)) for token in tokens]

logging.info("Starting removing special char and digit...")
cleaned_data["content"] = cleaned_data["content"].apply(clean_tokens)
logging.info("Removing char and digit completed")
print(cleaned_data["content"].head())


#Converts emoji to text
logging.info("Starting converting emoji....")
cleaned_data["content"] = cleaned_data["content"].apply(lambda tokens: [emoji.demojize(token) for token in tokens])
logging.info("Converting emoji completed")
print(cleaned_data["content"].head())

#Clean the empty token/sentence
cleaned_data["content"] = cleaned_data["content"].apply(lambda sentence: [word for word in sentence if word.strip()])

#Save into the new csv file
cleaned_data.to_csv("cleaned_data_content.csv", index=False)
logging.info(f"Data cleaned and saved as 'cleaned_data_content.csv'")