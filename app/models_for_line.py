from app import line_bot_api, handler
from crawler import get_house_pirce_data
from linebot.models import MessageEvent, TextMessage, TextSendMessage
 
import requests

def request_house_price():
    # url = get_url_from_connection_log()
    # res = requests.get(url)
    # context = res.json()
    # print(context)
    
    context = get_house_pirce_data()
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