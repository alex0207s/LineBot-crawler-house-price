from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import requests

#import configparser

app = Flask(__name__)

# 讀取 config
#config = configparser.ConfigParser()
#config.read('config.int')

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi('zM8h0i3xqlOstHiw0pGe5tHcnEc2yvJ6HRg6SRTH3Lg/1SlRdn3TWaZHePzvnhnMKshqAfriS0Hzowg20CzWa8UN+Zdtb+oE/3To/mtAZ0bX9uHXuxV2YB62b9Q45Z57OE9RdLakkeDJrkLQeDjmbgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f0305d1d5dad008c4f5681e28413e4c6')

# 接收 LINE 的資訊
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


def request_house_price():
    res = requests.get('https://lvr.land.moi.gov.tw/SERVICE/QueryPrice/1d61a7800e1d850742c5ecfb2f4d524d?q=VTJGc2RHVmtYMThmVkdnbGs3ajZBU241anA4c0VTbVBuVTBNODU0cFJ6QUZ4UHhEeHk4UzM3bkRCR29acUd1cTc0SjNucnVQakRVQ0RMTFdST3dDSmVkSUtMdDFhRlNmdDJNK3R5SEhhb2VQK0RTSGtVaWZDZUZmTGRENzVNaHJQdEZEQmNvNy9Lc1k0eWh6b2pmK2ZOa0ZhMEVGUXRJSzlmazZJNXRIUmdCTnFZYmZDZVZydkl4cURKdGhMWjIwRXZScWdaejkyV2tsM2JudC9IV3VvRXZGZHFFUnl3VlJ5VlZISlVVanVwTWs5Z0UzYTNyeUhLakVGQm9JZVpKSVloblRXNllOb1c3OG1odi9LMy9XL0JqcFNoYTJ5a3Y2M2VtVDVYT21QTDBRSXBhV1hCUW1kQ2cyQWRBaTRWTHk2Rm1MWUVjcHZ5UmpPeWJXdXd6eFE5WXdKZXZSTXRLZUZMVkpDcnBpZHZFay9zcVlJUzZtYkFTd1U4dlVCNzhjVkNXR0loYWdsVHMwSXVSRTJ4L2h6WVp0aVRWMnN3YzdieGV2eGRoN3Y1R0NmL3lkME9RTTZOL0VyS2R3L29pZllHR3A2cEJUVjZwWjYyWHNrdUViKzBqMTJCRDJjTlo4VFNGTmdDRDl6Tjk4ZWg3dGtxUGJ0VG13a1oxLy9JL2N1clNSczZFQ2U1S1MrU2UwWEdIaEtBb01CVCszUU1BVDlmZDBqUllDeW12RGF4M0dsaHo4TVdPcnlZNDdUMEdq')
    text = ""

    context = res.json()
    for i in range(5):
        text += str(i)+". " + context[i]['a'] + " " + context[i]['tp'] + "\n"

    return text

@handler.add(MessageEvent, message=TextMessage)
def echo(event):
    
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=request_house_price())
        )

if __name__ == "__main__":
    app.run()