from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi('zM8h0i3xqlOstHiw0pGe5tHcnEc2yvJ6HRg6SRTH3Lg/1SlRdn3TWaZHePzvnhnMKshqAfriS0Hzowg20CzWa8UN+Zdtb+oE/3To/mtAZ0bX9uHXuxV2YB62b9Q45Z57OE9RdLakkeDJrkLQeDjmbgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f0305d1d5dad008c4f5681e28413e4c6')

# 接收 LINE 平台送來的通知
@app.route("/callback", methods=['POST'])

def callback():
    signature = request.headers['X-Line-Signature']
    
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

if __name__ == "__main__":
    app.run()