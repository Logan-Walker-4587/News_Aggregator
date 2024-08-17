import requests
from bs4 import BeautifulSoup
import streamlit as st

# Function to fetch news articles
def fetch_news(api_key):
    url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['articles'][:10]
    else:
        return []

# Function to scrape content from a news article
def scrape_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        content = ' '.join([para.get_text() for para in paragraphs])
        return content[:500] + '...'  # Limit to first 500 characters for display
    except Exception as e:
        return f"Failed to scrape content: {e}"

# Streamlit App
def main():
    st.title("News Display App")
    api_key = st.text_input("Enter your NewsAPI key")

    if st.button("Give News"):
        if api_key:
            articles = fetch_news(api_key)
            if articles:
                for article in articles:
                    st.subheader(article['title'])
                    st.write(f"URL: {article['url']}")
                    content = scrape_content(article['url'])
                    st.write(content)
                    st.markdown(f"[Read more...]({article['url']})")
            else:
                st.write("No news available at the moment.")
        else:
            st.write("Please enter a valid API key.")

if __name__ == "__main__":
    main()
