import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
import requests

# Function to scrape data from Wikipedia
def scrape_data(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find('table', class_='wikitable')
    return table

# Function to process table data into a DataFrame
def process_data(table):
    headers = table.find_all('th')
    titles = [header.text.strip() for header in headers]
    
    rows_data = []
    rows = table.find_all('tr')[1:]
    
    for row in rows:
        cells = row.find_all('td')
        row_data = [cell.text.strip() for cell in cells]
        rows_data.append(row_data)
    
    df = pd.DataFrame(rows_data, columns=titles)
    return df

# Function to visualize top 5 industries by frequency
def visualize_top_industries(df):
    plt.figure(figsize=(10, 4))
    sns.countplot(y='Industry', data=df, order=df['Industry'].value_counts().index[:5])
    plt.title("Top 5 Industries In the US")
    plt.xlabel("Frequency")
    plt.ylabel("Industry Type")
    plt.tight_layout()
    plt.savefig('Top 5 Industries In the US.png')
    plt.show()

# Function to visualize top 5 companies by revenue
def visualize_top_companies(df):
    df['Revenue (USD millions)'] = df['Revenue (USD millions)'].str.replace(',', '').astype(float)
    top_10 = df.sort_values(by='Revenue (USD millions)', ascending=False).head(5)
    
    plt.figure(figsize=(8, 4))
    plt.bar(top_10['Name'], top_10['Revenue (USD millions)'], color='#002B00')
    plt.title('Top 5 Companies by Revenue')
    plt.xlabel('Company Name')
    plt.ylabel('Revenue (Million $)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('Top 5 Companies by Revenue.png')
    plt.show()

# Main function to orchestrate the entire process
def main():
    url = "https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue"
    table = scrape_data(url)
    df = process_data(table)
    
    # Save DataFrame to CSV
    df.to_csv("Top Companies in US.csv", index=False)
    
    # Visualize top industries and top companies
    visualize_top_industries(df)
    visualize_top_companies(df)

if __name__ == "__main__":
    main()
