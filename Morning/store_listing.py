import pandas as pd
import numpy as np

def get_store_num():

    store_lt = []

    df = pd.read_excel("THD STORE LIST_05.30.2023.xlsx")
    # print(df.columns)

    for i in df[df['CNTRY_CD'] == 'US']["STORE_NUM"]:
        store_lt.append(i)

    return(sorted(list(set(store_lt))))

if __name__ == '__main__':
    ids = get_store_num()

    # print(len(ids[:-2]))
    print(sorted(ids))

