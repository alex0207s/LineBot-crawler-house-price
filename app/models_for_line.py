from app import line_bot_api, handler

from linebot.models import MessageEvent, TextMessage, TextSendMessage
 
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from time import sleep

import os
import json
import requests

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
  
    
    try :
        sleep(1)    
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
        driver.execute_script("document.getElementById('customCheck1').click()")
        # 勾選土地
        driver.execute_script("document.getElementById('customCheck2').click()")
        driver.find_element_by_link_text('搜尋').click()

        sleep(1)
        request_log = driver.get_log('performance')[1000::]
        print('len', len(request_log))
        for i in range(len(request_log)):
            if request_log[i]['level'] == 'INFO':
                tmp = request_log[i]['message']
                if json.loads(tmp)['message']['params'].get('request') != None:
    #                 print(json.loads(tmp)['message']['params'].get('request'))
                    if json.loads(tmp)['message']['params'].get('request').get('url') != None:
                        if 'https://lvr.land.moi.gov.tw/SERVICE/QueryPrice/' in json.loads(tmp)['message']['params'].get('request').get('url'):
                            print('我要的東西', json.loads(tmp)['message']['params'].get('request').get('url'))
                            driver.close()
                            return json.loads(tmp)['message']['params'].get('request').get('url')

        return 'fail'
        
    except Exception as e:
        print(e)
        driver.close()


def request_house_price():
    url = get_chrom()
    # if url == 'fail':
    #     text = '網路壅塞，請重新嘗試!'
    #     print(text)
    # url = 'https://lvr.land.moi.gov.tw/SERVICE/QueryPrice/b7fb44997bae9fc9ef32ee06dcdf18cb?q=VTJGc2RHVmtYMThJRkFXYmRNRG9hNThiVExMMUtZdDNZUWtZcEY1VjJwRkJiVFNQeVhVaytuWkd5VlJqYTdLZVYxRWMyY2NGOHlFaG9sdFdFTGFYaE1vbWU0Q2xwejBLK0NmWjVHSnZiRW1aZ0xlY1Y0VWdDa0p3Z2k5OWxZd2JCcXBYb0l3eUlvYVZUclVIZnRNM1phSXV1NlVaWFFZU3BKTzhtYjVwQUdXQm5WMnBNVnNnL3RPZ2pFNTRvbldaTVZtZ1dodFB1NFYyV1NDVzRSZzFZSTN0QlFDUDkvTmtQVHVJcDFvc2ZhbFJ4UWpoUFZYQTFjUlFSZndxazByZDJ5Zi9zWVdvYXBzUm8ySmhEV3dHSE8vTmc5RUpEcjZncllNV0RoUHY0VDNHOVNINjU4OFZSeEJMNUVwdmVVYkNkVWVTOUY1SmZsOXV3SklFQklWcTBVLzhXdExKT2JOUkJ3eWt1TFhjclZDVU9RK3RRelE4V2hRazhraStjSUdNa01XbEdJZC8vQWlRRHFRRjdMeVR6alozZ0o5eDZ5VkV4U096WENoRGFaWG1YcDZvR0lQRDFTeXJCV0cyRnBySWlKMitIdDY1K1lNay9JSjVnVUR1MUxFelNacmd3bWVCcUZSQmVkV3ZCb0thZTBoUGRtMW1QazV2dDJVZzRzcnlwRDdaK3czTitxR2ZyUTRQMFM0QjhISkJQMWQ4dFRST1pBS1V6MHVxLzNwQkJXNFNPeFpRdUFGNnBEbWFUalgxcURhcG0wOVpTdTFXcFROdmRUczNnVERZdG93c1Zqc1R3RE4vUnhhcmZWVFpGODZUczBTZkEybDQrdklDbDlvb1d2eFJkRjlWRXlEQWhjSTNOcEY4YXA0cUZmT3ZnZGlhbEdCUStiUGFEWENvQ2ozYVZqbjUvS3lRUHhuMTJZVGM='
    res = requests.get(url)
    context = res.json()
    print(context)
    text = ""
    for i in range(5):
        text += str(i)+". " + context[i]['a'] + "\t" + context[i]['tp'] + "\n"
    return text

@handler.add(MessageEvent, message=TextMessage)
def RequestHousePrice(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        if event.message.text == "給我房價":
            text = request_house_price()
            if text == '':
                text = '沒抓到東西'
        else:
            text = "功能尚未開發"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        )