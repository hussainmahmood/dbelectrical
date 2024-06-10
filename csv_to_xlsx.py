import time
import pandas as pd

def main():
    for page in range(1, 835):
        df = pd.read_csv(f'data/{page}.csv')
        df['link'] = df['link'].str.replace('com//pro','com/pro')
        df.to_csv(f'data/{page}.csv', index=False)
        df.to_excel(f'data/{page}.xlsx', index=False)
        
    main_df = pd.read_csv(f'data/products.csv')
    main_df['link'] = main_df['link'].str.replace('com//pro','com/pro')
    main_df.to_csv(f'data/products.csv', index=False)
    main_df.to_excel(f'data/products.xlsx', index=False)

        
if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"--- {time.time() - start_time} seconds ---")

