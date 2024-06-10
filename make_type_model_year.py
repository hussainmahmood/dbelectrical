import os, time
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor

def get_type_model_year(make_in):
    df_arr = []
    if os.path.isfile(f'data/{make_in.text.replace("/", "-")}.csv'):
        df = pd.read_csv(f'data/{make_in.text.replace("/", "-")}.csv')
        df_arr = df.values.tolist()
        print(df_arr)
        return df_arr
    options = uc.ChromeOptions() 
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-gpu')
    driver = uc.Chrome(use_subprocess=True, options=options, version_main = 95) 
    driver.get("https://www.dbelectrical.com")
    part_finder = WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.ID, "part-finder")))
    make = part_finder.find_element(By.XPATH, f"//select[@class='ss__finder-select-item']/option[text()='{make_in.text}']")
    make.click()
    time.sleep(5)
    type_select = part_finder.find_elements(By.CLASS_NAME, "ss__finder-select-item")[1]
    for type in type_select.find_elements(By.XPATH, "*")[1:]:
        type.click()
        time.sleep(5)
        model_select = part_finder.find_elements(By.CLASS_NAME, "ss__finder-select-item")[2]    
        for model in model_select.find_elements(By.XPATH, "*")[1:]:
            model.click()
            time.sleep(5)
            year_select = part_finder.find_elements(By.CLASS_NAME, "ss__finder-select-item")[3]
            for year in year_select.find_elements(By.XPATH, "*")[1:]:
                print([make.text, type.text, model.text, year.text])
                df_arr.append([make.text, type.text, model.text, year.text])
    df = pd.DataFrame(data=df_arr, columns=['make', 'type', 'model', 'year'])
    df.to_csv(f'data/{make.text.replace("/", "-")}.csv', index=False)
    driver.quit()
    return df_arr



def main():
    options = uc.ChromeOptions() 
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-gpu')
    driver = uc.Chrome(use_subprocess=True, options=options, version_main = 95) 
    driver.get("https://www.dbelectrical.com")
    part_finder = WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.ID, "part-finder")))
    make_select = part_finder.find_elements(By.CLASS_NAME, "ss__finder-select-item")[0]    
    # with ThreadPoolExecutor(6) as executor:
    #     result = executor.map(get_type_model_year, make_select.find_elements(By.XPATH, "*")[1:])

    main_arr = []
    for make in make_select.find_elements(By.XPATH, "*")[1:]:
        df = pd.read_csv(f'make_type_model_year_by_company/{make.text.replace("/", "-")}.csv')
        main_arr += df.values.tolist()

    driver.quit()
    df = pd.DataFrame(data=main_arr, columns=['make', 'type', 'model', 'year'])
    df.to_csv('data/make_type_model_year.csv', index=False)
        

        
if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"--- {time.time() - start_time} seconds ---")

