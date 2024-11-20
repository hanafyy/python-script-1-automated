import requests
from bs4 import BeautifulSoup

# URL of the BBC News main page
url = "https://www.bbc.com/news"

# Send a GET request to the URL
response = requests.get(url)
# Parse the HTML content of the page with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Open a file to save the URLs
with open('bbc_news_links.txt', 'w') as file:
    # Find all hyperlinks on the page
    links = soup.find_all('a', href=True)

    # Filter and print the URLs that are likely to be blog posts or articles
    # This assumes that blogs or articles contain '/news/articles' in their URL
    for link in links:
        href = link['href']
        # Check if the link contains the news path and is a relative link (starts with '/')
        if '/news/articles' in href and href.startswith('/'):
            full_url = f"https://www.bbc.com{href}"
            print(full_url)
            # Write the URL to the file
            file.write(full_url + '\n')
