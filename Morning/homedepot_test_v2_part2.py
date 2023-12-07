import pandas as pd
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, WebDriverException, SessionNotCreatedException, ElementNotInteractableException, StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
import numpy as np
import pandas as pd
import random
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
from datetime import date, datetime
from store_listing import get_store_num
import os
import json

def get_part_of_day(h):
    return (
        "morning"
        if 5 <= h <= 11
        else "afternoon"
        if 12 <= h <= 17
        else "evening"
        if 18 <= h <= 22
        else "night"
    )

def initialize_user_agent_and_ip_rotation():
    useragent_obj = UserAgent(browsers=["edge", "firefox", "safari", 'chrome'], use_external_data=True)
    useragent = str(useragent_obj.random)
    PROXY = "http://api.scraperapi.com?api_key={}&url=http://httpbin.org/ip&render=true".format("b85d057a0618675b026177fb3351ea6d")
    # PROXY = "65.109.160.214:8080"
    return(useragent, PROXY)

def required_options_and_Driver(type_of_driver=True):
    # chromedriver_autoinstaller.install()

    # few error handling
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless=new')
    # options.add_experimental_option("detach", True)
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-site-isolation-trials")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument('--disable-blink-features=AutomationControlled')
    # options.add_argument("--user-data-dir=" + r"C:\Users\artayade\AppData\Local\Google\Chrome\User Data\Default")
    # options.add_argument("--incognito")

    useragent, PROXY = initialize_user_agent_and_ip_rotation()

    # user agent rotation
    options.add_argument("user-agent={}".format(useragent))
    options.add_argument("--start-maximized")
    # ip rotation

    options.add_argument("--proxy-server={}".format(PROXY))

    if type_of_driver == True:
        driver = uc.Chrome(options=options, driver_executable_path='chromedriver/chromedriver.exe')
    else:
        driver = webdriver.Chrome(options=options)

    driver.delete_all_cookies()

    return(driver)

def run():
    already_scraped_ids = []
    
    if os.path.exists(f'brickseek_temp_json_morning_homedepot_{datetime.now().date()}_part2/already_scraped.json'):
        with open(f'brickseek_temp_json_morning_homedepot_{datetime.now().date()}_part2/already_scraped.json') as f:
            d = json.load(f)

        if len(d) == 1:
            already_scraped_ids = d
        else:
            already_scraped_ids = d

        # print(already_scraped_ids)

    driver = required_options_and_Driver()
    
    driver.get("https://www.homedepot.com/p/14-1-oz-MAPP-Gas-Cylinder-1-in-Valve-No-Regulator-Required-221197/318912570")

    # driver.implicitly_wait(10)
    sleep(10)
    driver.set_page_load_timeout(10)
    # sleep(3)
    # print("page loaded")

    driver.execute_script("window.scrollBy(0, 800)")

    try:
        driver.find_element(By.CSS_SELECTOR, '#root > div > div:nth-child(3) > div > div > div.col__12-12.col__5-12--sm > div > div > div:nth-child(10) > div > div > div:nth-child(2) > div > div > div.buybox__actions--atc > div > div > div > button').click()
        sleep(5)
        driver.implicitly_wait(15)
    except:
        addtocart = driver.find_element(By.CLASS_NAME, 'buybox__atc')
        addtocart.find_element(By.TAG_NAME, 'button').click()
        sleep(5)
        driver.implicitly_wait(15)

    driver.get('https://www.homedepot.com/mycart/home')

    driver.implicitly_wait(3)

    # - - -  - - -  - - -  - - -  - - -  - - -  - - -  - - -  - - -  - - -  - - -  - - - 
    # check if item has been added to cart
    try:
        try:
            # checking cart cpunt
            cart_Ct = driver.find_element(By.XPATH, '//*[@id="headerCart"]/div[1]/span[2]').text
            if cart_Ct != '0':
                print("Item added to cart")
            else:
                print("Item couldnt be added to cart")
                driver.quit()
        except:
            print("Item couldnt be added to cart")
            driver.quit()

        while True:
            try:
                drop_down_btn = wait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "MyStoreWrapper")))
                drop_down_btn.click()
                sleep(1)
                
                # store_no = driver.find_elements(By.CLASS_NAME, 'u__medium')[1].text
                # sleep(1)

                select_btn = wait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#myStoreDropdown > div > div.col__12-12.u--text-md > a')))
                select_btn.click()
                sleep(1)
                break
            except:
                driver.refresh()
                sleep(5)
                continue

        # store no which are already scraped
        main_counter = 0

        for each_store_no in get_store_num()[1000:]:
            todays_stock_status = []

            if str(each_store_no)[-1].isalpha():
                continue
            
            else:      
                while True:
                    try:
                        if each_store_no not in already_scraped_ids:
                            
                            if main_counter != 0:
                                # store no which are not scraped, keep limit = 100 and then try other script
                                
                                while True:
                                    try:
                                        driver.find_element(By.CLASS_NAME, "MyStoreWrapper").click()
                                        sleep(4)
                                        driver.implicitly_wait(10)
                                        select_btn = wait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#myStoreDropdown > div > div.col__12-12.u--text-md > a')))
                                        select_btn.click()
                                        sleep(2)
                                        break
                                    except:
                                        driver.refresh()
                                        sleep(5)
                                        continue 
                                    
                                    # except NoSuchElementException or TimeoutException:
                                    #     driver.refresh()
                                    #     sleep(2)
                                    #     drop_down_btn = wait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "MyStoreWrapper")))
                                    #     drop_down_btn.click()
                                    #     sleep(2)
                                    #     select_btn = wait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#myStoreDropdown > div > div.col__12-12.u--text-md > a')))
                                    #     select_btn.click()
                                    #     sleep(2)

                            next_store_no = driver.find_element(By.ID, 'myStore-formInput')
                            next_store_no.send_keys(each_store_no)
                            next_store_no.send_keys(Keys.ENTER)
                            sleep(2)

                            first_store_to_select = driver.find_elements(By.CLASS_NAME, 'localization__store')[0]
                            current_store_no = first_store_to_select.text.split("\n")[0].split("#")[-1]
                            first_store_to_select.find_element(By.CLASS_NAME, 'localization__button--select').click()
                            sleep(5)

                            try:
                                qty = driver.find_element(By.CLASS_NAME, 'fulfillment-qty-row').text
                                qty = int(qty.split(" ")[0])
                            except:
                                qty = 0

                            todays_stock_status.append([current_store_no, qty])

                            with open(f'brickseek_temp_json_morning_homedepot_{datetime.now().date()}_part2/{each_store_no}.json', "w") as file:
                                json.dump(todays_stock_status, file)

                            if os.path.exists(f'brickseek_temp_json_morning_homedepot_{datetime.now().date()}_part2/already_scraped.json'):
                                with open(f'brickseek_temp_json_morning_homedepot_{datetime.now().date()}_part2/already_scraped.json', 'r') as file:
                                    existing_data = json.load(file)

                                existing_data.append(each_store_no)

                                with open(f'brickseek_temp_json_morning_homedepot_{datetime.now().date()}_part2/already_scraped.json', 'w') as file:
                                    json.dump(existing_data, file)
                            else:
                                with open(f'brickseek_temp_json_morning_homedepot_{datetime.now().date()}_part2/already_scraped.json', 'w') as file:
                                    json.dump([each_store_no], file)

                            main_counter += 1

                        else:
                            pass
                        
                        break

                    except SessionNotCreatedException or WebDriverException or NoSuchElementException or TimeoutException or ElementNotInteractableException or StaleElementReferenceException:
                        driver.refresh()
                        sleep(3)

        driver.quit()

    except NoSuchElementException:
        driver.quit()

    # - - -  - - -  - - -  - - -  - - -  - - -  - - -  - - -  - - -  - - -  - - -  - - -

def main():
    os.makedirs(f'brickseek_temp_json_morning_homedepot_{datetime.now().date()}_part2', exist_ok=True)
    run()

if __name__ == '__main__':

    main()
