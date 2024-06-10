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
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-gpu')
    driver = uc.Chrome(use_subprocess=True, options=options, version_main = 95) 
    product_df_arr = []
    make_arr = []
    df = pd.read_csv(f'data/make_type_model_year.csv')
    len_df = len(df)
    count = 0
    start_time = time.time()
    for i, row in df.iterrows():
        count += 1
        product_make_arr = []
        fitment_query = urllib.parse.quote(f"{row['make']}>{row['type']}>{row['model']}>{row['year']}", safe='').replace('%', '$25')
        driver.get(f"https://www.dbelectrical.com/shop/?view=products#/pf:ss_fitment:{fitment_query}")    
        headingEl = WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.CLASS_NAME, "page-heading")))
        pageHeading = bs(headingEl.get_attribute('outerHTML'), "lxml")
        product_count = int(pageHeading.find('span', class_='ss__search-header__count-total').get_text().strip())
        if product_count > 24:
            raise Exception('too many products found')
        df.at[i, 'product_count'] = product_count
        innerEl = WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.CLASS_NAME, "productGrid")))
        productGrid = bs(innerEl.get_attribute('outerHTML'), "lxml")
        for product in productGrid.find_all('li', class_='product'):
            product_arr = []
            product_arr.append(row['make'])
            product_arr.append(row['type'])
            product_arr.append(row['model'])
            product_arr.append(row['year'])
            product_arr.append(product.find('div', class_='card-sku').get_text().strip())
            product_arr.append(product.find('img', class_='card-image')['src'].replace("/320w/", "/1280x1280/"))
            productTitle = product.find('h3', class_='card-title').find('a')
            product_arr.append(f"https://www.dbelectrical.com{productTitle['href']}")
            product_arr.append(productTitle.get_text().strip())
            product_arr.append(product.find('div', class_='card-text').find('span', class_='price price--withoutTax').get_text().strip())
            product_make_arr.append(product_arr)
        
        time_elapsed = time.time() - start_time
        time_per_row = time_elapsed/count
        print(f"{count}/{len_df} - {round(count*100/len_df, 2)}% done", f"{row['make']}>{row['type']}>{row['model']}>{row['year']}:", product_count, len(product_make_arr), f"time elapsed={time_elapsed}s", f"{time_per_row}s/row", f"ETA={time_per_row*(len_df-count)}s")
        if product_count != len(product_make_arr):
            raise Exception('Product count not matched')
        product_make_df = pd.DataFrame(data=product_make_arr, columns=['make', 'type', 'model', 'year', 'sku', 'image', 'link', 'title', 'price'])
        product_make_df.to_csv(f"products_by_make/{fitment_query}.csv", index=False)
        df.to_csv(f'data/make_type_model_year.csv', index=False)
        product_df_arr += product_make_arr

    product_df = pd.DataFrame(data=product_df_arr, columns=['make', 'type', 'model', 'year', 'sku', 'image', 'link', 'title', 'price'])
    product_df.to_csv(f'data/products_with_make.csv', index=False)
    product_df.to_excel(f'data/products_with_make.xlsx', index=False)
    
    
    driver.quit()
        

        
if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"--- {time.time() - start_time} seconds ---")