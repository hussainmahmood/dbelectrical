import time
import pandas as pd
from bs4 import BeautifulSoup as bs
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    options = uc.ChromeOptions() 
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-gpu')
    driver = uc.Chrome(use_subprocess=True, options=options, version_main = 95) 
    df = pd.read_csv(f'data/products.csv')
    df["category"] = ""
    df["subcategory"] = ""
    df["rating"] = ""
    df["review_count"] = ""
    for i, product in df.iterrows():
        print(i, product['link'])
        driver.get(product['link'])
        try:
            innerEl = WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.ID, "main-content")))
            productBody = bs(innerEl.get_attribute('outerHTML'), "lxml")
            breadcrumbs = productBody.find_all('li', class_='breadcrumb')
            if len(breadcrumbs) >= 3:
                df.at[i, 'category'] = breadcrumbs[1].get_text().strip()
                print(breadcrumbs[1].get_text().strip())
            if len(breadcrumbs) >= 4:
                df.at[i, 'subcategory'] = breadcrumbs[2].get_text().strip()
                print(breadcrumbs[2].get_text().strip())    
            reviewEl = WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.ID, "customer-reviews")))
            reviews = bs(reviewEl.get_attribute('outerHTML'), "lxml")
            df.at[i, 'rating'] = reviews.find('span', class_='avg-score').get_text().strip()
            df.at[i, 'review_count'] = reviews.find('span', class_='reviews-qa-label').get_text().replace(' Reviews', '').strip()
        except:
            pass

    
    df.to_csv('data/products_with_category_reviews.csv', index=False)
    df.to_excel('data/products_with_category_reviews.xlsx', index=False)
    driver.quit()

        
if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"--- {time.time() - start_time} seconds ---")