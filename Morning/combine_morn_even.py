import json
import pandas as pd
import os
import warnings
import numpy as np

warnings.filterwarnings("ignore")

df_main = pd.DataFrame(columns=['Key', 'Value1'])

for each_json_file in os.listdir('brickseek_temp_json_morning_homedepot_2023-09-11_part1'):
    # print(each_json_file)
    if each_json_file == 'already_scraped.json':
        pass
    
    else:
        with open(os.path.join('brickseek_temp_json_morning_homedepot_2023-09-11_part1', each_json_file)) as f:
            d = json.load(f)
            # print(d)
            df1 = pd.DataFrame(d, columns=['Key', 'Value1'])
            df_main = pd.concat([df_main, df1], axis=0)

# df_main = df_main[df_main['Value1'] != int]
print(len(df_main['Key'].unique()))