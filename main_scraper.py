#%%
import pandas as pd
from bs4 import BeautifulSoup
import requests
# Extract tables using pandas. 

def extractor(url):
    tables = pd.read_html(url)

# Parse month and year using beautifulsoup
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('span', class_='page-title')
    title = title.text
    new_title = title.replace(" eBay GPU Prices", "").strip('\n')
    
# create customized column using parsed data > GPU Name, Month (avg price), Sold amount
    for table in tables:
        table.drop(table.iloc[:, 3:], axis=1, inplace=True)

# redesign the table accrodingly
    new_table = pd.concat([tables[0], tables[1]], ignore_index=True)
    new_table.rename({'Avg eBay Price' : new_title + '(Avg Price)'}, axis=1, inplace=True)
    new_table['GPU'] = new_table['GPU'].str.replace(r'\(.*?\)', '', regex=True)

# export table to a csv file with the months name
    new_table.to_csv(f"CSV/{new_title}.csv", index=False)
    print(f"CSV Export Successful - {new_title}")

if __name__ == "__main__":
    url = "https://www.tomshardware.com/news/gpu-pricing-index"
    for i in range(1, 12):
        extractor(url + f'/{i}')



