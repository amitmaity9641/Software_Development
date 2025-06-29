import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Set headers to mimic a browser visit
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

def scrape_amazon(search_query, num_pages=1):
    base_url = 'https://www.amazon.com/s?k='
    products = []
    
    for page in range(1, num_pages + 1):
        url = f"{base_url}{search_query.replace(' ', '+')}&page={page}"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        items = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        for item in items:
            try:
                name = item.find('span', {'class': 'a-size-medium'}).text.strip()
            except:
                name = 'N/A'
                
            try:
                price = item.find('span', {'class': 'a-offscreen'}).text.strip()
            except:
                price = 'N/A'
                
            try:
                rating = item.find('span', {'class': 'a-icon-alt'}).text.strip().split()[0]
            except:
                rating = 'N/A'
                
            try:
                review_count = item.find('span', {'class': 'a-size-base'}).text.strip()
            except:
                review_count = 'N/A'
                
            products.append({
                'Name': name,
                'Price': price,
                'Rating': rating,
                'Review Count': review_count,
                'Page': page
            })
        
        time.sleep(2)  # Be polite with delay between requests
    
    return products

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    return df

def main():
    st.title("🛒 E-Commerce Web Scraper")
    st.write("Extract product information from Amazon and save to CSV")
    
    with st.form("scraper_form"):
        search_query = st.text_input("Enter product to search:", "laptops")
        num_pages = st.slider("Number of pages to scrape:", 1, 5, 1)
        submit = st.form_submit_button("Scrape Data")
    
    if submit:
        with st.spinner(f"Scraping {num_pages} page(s) of {search_query} products..."):
            try:
                products = scrape_amazon(search_query, num_pages)
                
                if not products:
                    st.warning("No products found. Try a different search term.")
                    return
                
                # Generate filename with timestamp
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                filename = f"amazon_{search_query}_{timestamp}.csv"
                
                df = save_to_csv(products, filename)
                
                st.success(f"Successfully scraped {len(products)} products!")
                
                # Show data preview
                st.subheader("Scraped Data Preview")
                st.dataframe(df.head())
                
                # Download button
                with open(filename, "rb") as f:
                    st.download_button(
                        label="Download CSV",
                        data=f,
                        file_name=filename,
                        mime="text/csv"
                    )
                
                # Clean up
                os.remove(filename)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Note: Amazon may be blocking automated requests. Try again later.")

if __name__ == "__main__":
    main()