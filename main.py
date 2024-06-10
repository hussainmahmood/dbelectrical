import sys, os , time , requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    options = uc.ChromeOptions() 
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-gpu')
    driver = uc.Chrome(use_subprocess=True, options=options, version_main = 95) 
    main_arr = []
    for page in range(1, 835):
        driver.get(f"https://www.dbelectrical.com/shop/?view=products&pp={page}")
        time.sleep(1)
        innerEl = WebDriverWait(driver, 2000).until(EC.presence_of_element_located((By.CLASS_NAME, "productGrid")))
        productGrid = bs(innerEl.get_attribute('outerHTML'), "lxml")
        df_arr = []
        for product in productGrid.find_all('li', class_='product'):
            product_arr = []
            product_arr.append(product.find('div', class_='card-sku').get_text().strip())
            product_arr.append(product.find('img', class_='card-image')['src'].replace("/320w/", "/1280x1280/"))
            productTitle = product.find('h3', class_='card-title').find('a')
            product_arr.append(f"https://www.dbelectrical.com{productTitle['href']}")
            product_arr.append(productTitle.get_text().strip())
            product_arr.append(product.find('div', class_='card-text').find('span', class_='price price--withoutTax').get_text().strip())
            df_arr.append(product_arr)

        df = pd.DataFrame(data=df_arr, columns=['sku', 'image', 'link', 'title', 'price'])
        df.to_csv(f'data/{page}.csv', index=False)
        main_arr += df_arr
    
    main_df = pd.DataFrame(data=main_arr, columns=['sku', 'image', 'link', 'title', 'price'])
    main_df.to_csv(f'data/products.csv', index=False)
    driver.quit()
        

        
if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"--- {time.time() - start_time} seconds ---")

