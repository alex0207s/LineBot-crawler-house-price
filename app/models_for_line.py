from app import line_bot_api, handler, Me
from handle_house_price_data import load_old_data, display_message
from linebot.models import MessageEvent, TextMessage, TextSendMessage

@handler.add(MessageEvent, message=TextMessage)
def RequestHousePrice(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        if event.source.user_id != Me:
            line_bot_api.push_message(Me, 
                TextSendMessage(text=event.source.user_id))
        
        if event.message.text == "最新資料":
            old_data = load_old_data('/app/old_data.json')
            text = display_message(old_data)
        else:
            text = "目前尚未開發 「" + event.message.text + "」 相關功能！\n敬請期待！"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        )