import os
import requests
from bs4 import BeautifulSoup

API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom"
headers = {"Authorization": "Bearer token"} 
# Create a folder for summaries if it doesn't already exist
summarization_folder = './summarization'
os.makedirs(summarization_folder, exist_ok=True)

# Path to the file containing URLs
urls_file_path = 'bbc_news_links.txt'

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Read URLs from the file
with open(urls_file_path, 'r') as file:
    urls = [line.strip() for line in file if line.strip()]

# Iterate over each URL
for url in urls:
    # Extract the article ID from the URL
    article_id = url.split('/')[-1]  # Assuming the ID is the last segment after the last slash
    
    try:
        # Fetch the content of the article
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        article_text = ' '.join(p.get_text() for p in soup.find_all('p'))
        
        # Send text for summarization
        output = query({
            "inputs": article_text,
            "parameters": {"max_length": 150},
            "options": {"use_cache": False, "wait_for_model": True}
        })
        
        # Extract summarized text
        summarized_text = output[0]['generated_text']

        # Save the summary to a file named by the article ID
        summary_file_path = os.path.join(summarization_folder, f'{article_id}.txt')
        with open(summary_file_path, 'w', encoding='utf-8') as summary_file:
            summary_file.write(summarized_text)

        print(f'Summary for {article_id} saved.')

    except Exception as e:
        print(f'Failed to process {url}: {e}')
