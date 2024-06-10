import sys, os , time , requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse


def main():
    options = uc.ChromeOptions() 
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-gpu')
    driver = uc.Chrome(use_subprocess=True, options=options, version_main = 95) 
    main_arr = []
    make_arr = ['ISUZU', 'KTM', 'AMC', 'CAN-AM', 'MARINER']
    for make in make_arr:
        df = pd.read_csv(f'data/{make}.csv')
        samples = df.sample(n=8, replace=False)
        for i, sample in samples.iterrows():
            fitment_query = urllib.parse.quote(f"{sample['make']}>{sample['type']}>{sample['model']}>{sample['year']}", safe='').replace('%', '$25')
            driver.get(f"https://www.dbelectrical.com/shop/?view=products#/pf:ss_fitment:{fitment_query}")    
            time.sleep(1)
            innerEl = WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.CLASS_NAME, "productGrid")))
            productGrid = bs(innerEl.get_attribute('outerHTML'), "lxml")
            df_arr = []
            for product in productGrid.find_all('li', class_='product'):
                product_arr = []
                product_arr.append(sample['make'])
                product_arr.append(sample['type'])
                product_arr.append(sample['model'])
                product_arr.append(sample['year'])
                product_arr.append(product.find('div', class_='card-sku').get_text().strip())
                product_arr.append(product.find('img', class_='card-image')['src'].replace("/320w/", "/1280x1280/"))
                productTitle = product.find('h3', class_='card-title').find('a')
                product_arr.append(f"https://www.dbelectrical.com{productTitle['href']}")
                product_arr.append(productTitle.get_text().strip())
                product_arr.append(product.find('div', class_='card-text').find('span', class_='price price--withoutTax').get_text().strip())
                df_arr.append(product_arr)

            main_arr += df_arr
        
    main_df = pd.DataFrame(data=main_arr, columns=['make', 'type', 'model', 'year', 'sku', 'image', 'link', 'title', 'price'])
    main_df.to_csv(f'data/sample_products1.csv', index=False)
    main_df.to_excel(f'data/sample_products1.xlsx', index=False)
    driver.quit()
        

        
if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"--- {time.time() - start_time} seconds ---")