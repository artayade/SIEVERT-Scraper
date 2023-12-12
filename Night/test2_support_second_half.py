import os
from time import sleep
from datetime import datetime
import json
from store_listing import get_store_num
import winsound

global_date = '2023-12-07'

if __name__ == '__main__':
    while True:
        if os.path.exists(f'brickseek_temp_json_night_homedepot_{global_date}_part2/already_scraped.json'):
            with open(f'brickseek_temp_json_night_homedepot_{global_date}_part2/already_scraped.json') as f:
                d = json.load(f)
            
            already_scraped_ids = d

            if len(already_scraped_ids) >= 950:
                print("All ids scraped!!!")
                break

            else:
                os.system('python homedepot_test_v2_part2_NEW.py')
                frequency = 2500  # Set Frequency To 2500 Hertz
                duration = 1000  # Set Duration To 1000 ms == 1 second
                winsound.Beep(frequency, duration)
                sleep(100)
        
        else:
            os.system('python homedepot_test_v2_part2_NEW.py')
            frequency = 2500  # Set Frequency To 2500 Hertz
            duration = 1000  # Set Duration To 1000 ms == 1 second
            winsound.Beep(frequency, duration)
            sleep(100)
      
 
   

