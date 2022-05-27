from lib2to3.pgen2 import driver
# from requests import request
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep

import os
import json
import requests

def get_chrome():
    # chrome setting
    d = DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = {'performance': 'ALL'}

    opt = webdriver.ChromeOptions()
    opt.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    opt.add_argument("--headless")
    opt.add_argument("--disable-dev-shm-usage")
    opt.add_argument("--no-sandbox")
    opt.add_argument('--disable-blink-features=AutomationControlled')

    return webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=opt, desired_capabilities=d)

def get_search_log():
    driver = get_chrome()
    driver.get('https://lvr.land.moi.gov.tw/')


    sleep(1)    
    driver._switch_to.frame(0)
    
    # 選縣市
    select_city = Select(driver.find_element_by_xpath("//*[@id='p_city']"))
    select_city.select_by_value('M')
    sleep(1)

    # 選鄉鎮
    select_town = Select(driver.find_element_by_xpath("//*[@id='p_town']"))
    select_town.select_by_value('M03')
    
    # 取消勾選房地
    driver.execute_script("document.getElementById('customCheck1').click()")
    
    # 勾選土地
    driver.execute_script("document.getElementById('customCheck2').click()")
    
    # 點選搜尋鍵
    driver.find_element_by_link_text('搜尋').click()

    sleep(3)
    request_log = driver.get_log('performance')[1000::]
    driver.close()
    return request_log

def get_url_from_connection_log():
    request_log = get_search_log()

    for i in range(len(request_log)):
        if request_log[i]['level'] == 'INFO':
            tmp = request_log[i]['message']
            if json.loads(tmp)['message']['params'].get('request') != None:
                if json.loads(tmp)['message']['params'].get('request').get('url') != None:
                    if 'https://lvr.land.moi.gov.tw/SERVICE/QueryPrice/' in json.loads(tmp)['message']['params'].get('request').get('url'):
                        print('我要的東西', json.loads(tmp)['message']['params'].get('request').get('url'))
                        # driver.close()
                        return json.loads(tmp)['message']['params'].get('request').get('url')

def get_house_pirce_data():
    # url = get_url_from_connection_log()
    # return requests.get(url).json()
    with open('/app/records_json.json') as f:
        data = json.load(f)

    print(data)
    return data
