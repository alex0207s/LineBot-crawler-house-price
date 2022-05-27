from app import line_bot_api, handler
from crawler import get_house_pirce_data
from handle_house_price_data import handle_house_price_data
from linebot.models import MessageEvent, TextMessage, TextSendMessage

def request_house_price():
    context = get_house_pirce_data()
    return handle_house_price_data(context)

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