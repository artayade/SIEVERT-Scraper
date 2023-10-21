from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.events import EVENT_JOB_ERROR
from homedepot_test_v2_part1 import run
from datetime import datetime
from time import sleep
import os
import json

def run_():
    try:
        run()
    except Exception:
        print(f"Error occuered at {datetime.now().time()}")
        scheduler.shutdown(wait=False)

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    job_id = scheduler.add_job(run_, "date", run_date = '2023-09-13 13:12:00')
    scheduler.start()
    sleep(360)

    while datetime.now().hour > 18 and datetime.now().hour < 24:
        if scheduler.state == 0:
            if os.path.exists(f'brickseek_temp_json_morning_homedepot_{datetime.now().date()}_part1/already_scraped.json'):
                with open(f'brickseek_temp_json_morning_homedepot_{datetime.now().date()}_part1/already_scraped.json') as f:
                    d = json.load(f)
                
                already_scraped_ids = d

                if len(already_scraped_ids) >= 950:
                    print("All ids scraped!!!")
                    break 
                else:
                    scheduler = BlockingScheduler()
                    scheduler.add_job(run_)
                    scheduler.start()
                    # scheduler.shutdown(wait=False)
                    sleep(480)
    
            else:
                scheduler = BlockingScheduler()
                scheduler.add_job(run_)
                scheduler.start()
                # scheduler.shutdown(wait=False)
                sleep(480)




