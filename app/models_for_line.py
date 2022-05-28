from app import line_bot_api, handler
from crawler import get_house_pirce_data
from handle_house_price_data import handle_house_price_data
from linebot.models import MessageEvent, TextMessage, TextSendMessage

def request_house_price():
    context = get_house_pirce_data()
    result = sorted(context.items(), key=lambda x:x[1], reverse=True)[:5]
    
    text = ''
    for index, record in enumerate(result):
        text += str(index+1) + '. \n交易日期: ' + record[1][0] + '\n地址: ' + record[0] + '\n總價: ' + str(int(record[1][2].replace(',', ''))/10000) + ' 萬\n總面積: ' + record[1][1] + '\n\n'   
        if len(text) >= 300:
            break

    return text
    # return handle_house_price_data(context)
    # return context

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