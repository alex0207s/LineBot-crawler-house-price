from app import line_bot_api, handler
from handle_house_price_data import get_house_price_data
from linebot.models import MessageEvent, TextMessage, TextSendMessage

@handler.add(MessageEvent, message=TextMessage)
def RequestHousePrice(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        if event.message.text == "給我房價":
            text = get_house_price_data()
            if text == '':
                text = '目前沒有最新的資料!'
        else:
            text = "目前尚未開發 「" + event.message.text + "」 相關功能！\n敬請期待！"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        )