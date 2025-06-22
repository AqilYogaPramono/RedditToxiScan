import re
from typing import List

def clean_text(text: str) -> str:
    # Convert to string and lowercase
    text = str(text).lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    
    # Remove mention
    text = re.sub(r'@\w+', '', text)
    
    # Remove hashtags but keep the word
    text = re.sub(r'#(\w+)', r'\1', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep alphanumeric and spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # Remove single characters (likely noise)
    text = re.sub(r'\b\w\b', '', text)
    
    # Remove extra whitespace again
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading and trailing whitespace
    text = text.strip()
    return text

def clean_comments(comments: List[str]) -> List[str]:
    cleaned_comments = []
    for comment in comments:
        cleaned = clean_text(comment)
        if cleaned and len(cleaned.strip()) > 3:
            cleaned_comments.append(cleaned)
    return cleaned_comments 