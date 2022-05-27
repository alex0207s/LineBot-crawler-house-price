from app import line_bot_api, handler

from linebot.models import MessageEvent, TextMessage, TextSendMessage
# import requests

import os 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from time import sleep
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import json

def get_chrom():
    d = DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = {'performance': 'ALL'}
    opt = webdriver.ChromeOptions()
    opt.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    opt.add_argument("--headless")
    opt.add_argument("--disable-dev-shm-usage")
    opt.add_argument("--no-sandbox")
    opt.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=opt, desired_capabilities=d)

    driver.get('https://lvr.land.moi.gov.tw/')
    # return 'success'
    sleep(1)    

    try :
        driver._switch_to.frame(0)
        
        # 選縣市
        select_city = Select(driver.find_element_by_xpath("//*[@id='p_city']"))
        select_city.select_by_value('M')
        sleep(1)
        # 選鄉鎮
        select_town = Select(driver.find_element_by_xpath("//*[@id='p_town']"))
        select_town.select_by_value('M03')
        sleep(1)
        # 取消勾選房地
        driver.find_element_by_xpath("//*[@id='main_form']/div/div[3]/div[1]").click()
        # 勾選土地
        # sleep(3)
        driver.find_element_by_xpath("//*[@id='main_form']/div/div[3]/div[2]").click()
        driver.find_element_by_link_text('搜尋').click()
        
    #     sleep(3)
        request_log = driver.get_log('performance')#[1320::]
        print('len', len(request_log))
        for i in range(len(request_log)):
            if request_log[i]['level'] == 'INFO':
                tmp = request_log[i]['message']
                if json.loads(tmp)['message']['params'].get('request') != None:
    #                 print(json.loads(tmp)['message']['params'].get('request'))
                    if json.loads(tmp)['message']['params'].get('request').get('url') != None:
                        if 'https://lvr.land.moi.gov.tw/SERVICE/QueryPrice/' in json.loads(tmp)['message']['params'].get('request').get('url'):
                            print('我要的東西', json.loads(tmp)['message']['params'].get('request').get('url'))
                            # return json.loads(tmp)['message']['params'].get('request').get('url')
        print('success')
    
        driver.close()
        # return json.loads(tmp)['message']['params'].get('request').get('url')
        
    except Exception as e:
        print(e)
        driver.close()


# def request_house_price():
#     res = requests.get('https://lvr.land.moi.gov.tw/SERVICE/QueryPrice/1d61a7800e1d850742c5ecfb2f4d524d?q=VTJGc2RHVmtYMThmVkdnbGs3ajZBU241anA4c0VTbVBuVTBNODU0cFJ6QUZ4UHhEeHk4UzM3bkRCR29acUd1cTc0SjNucnVQakRVQ0RMTFdST3dDSmVkSUtMdDFhRlNmdDJNK3R5SEhhb2VQK0RTSGtVaWZDZUZmTGRENzVNaHJQdEZEQmNvNy9Lc1k0eWh6b2pmK2ZOa0ZhMEVGUXRJSzlmazZJNXRIUmdCTnFZYmZDZVZydkl4cURKdGhMWjIwRXZScWdaejkyV2tsM2JudC9IV3VvRXZGZHFFUnl3VlJ5VlZISlVVanVwTWs5Z0UzYTNyeUhLakVGQm9JZVpKSVloblRXNllOb1c3OG1odi9LMy9XL0JqcFNoYTJ5a3Y2M2VtVDVYT21QTDBRSXBhV1hCUW1kQ2cyQWRBaTRWTHk2Rm1MWUVjcHZ5UmpPeWJXdXd6eFE5WXdKZXZSTXRLZUZMVkpDcnBpZHZFay9zcVlJUzZtYkFTd1U4dlVCNzhjVkNXR0loYWdsVHMwSXVSRTJ4L2h6WVp0aVRWMnN3YzdieGV2eGRoN3Y1R0NmL3lkME9RTTZOL0VyS2R3L29pZllHR3A2cEJUVjZwWjYyWHNrdUViKzBqMTJCRDJjTlo4VFNGTmdDRDl6Tjk4ZWg3dGtxUGJ0VG13a1oxLy9JL2N1clNSczZFQ2U1S1MrU2UwWEdIaEtBb01CVCszUU1BVDlmZDBqUllDeW12RGF4M0dsaHo4TVdPcnlZNDdUMEdq')
#     context = res.json()
    
#     text = ""
#     for i in range(5):
#         text += str(i)+". " + context[i]['a'] + "\t" + context[i]['tp'] + "\n"
#     return text

@handler.add(MessageEvent, message=TextMessage)
def RequestHousePrice(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        if event.message.text == "給我房價":
            text = get_chrom()
            if text == '':
                text = '沒抓到東西'
        else:
            text = "功能尚未開發"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        )