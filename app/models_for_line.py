from app import line_bot_api, handler

from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests

def request_house_price():
    res = requests.get('https://lvr.land.moi.gov.tw/SERVICE/QueryPrice/1d61a7800e1d850742c5ecfb2f4d524d?q=VTJGc2RHVmtYMThmVkdnbGs3ajZBU241anA4c0VTbVBuVTBNODU0cFJ6QUZ4UHhEeHk4UzM3bkRCR29acUd1cTc0SjNucnVQakRVQ0RMTFdST3dDSmVkSUtMdDFhRlNmdDJNK3R5SEhhb2VQK0RTSGtVaWZDZUZmTGRENzVNaHJQdEZEQmNvNy9Lc1k0eWh6b2pmK2ZOa0ZhMEVGUXRJSzlmazZJNXRIUmdCTnFZYmZDZVZydkl4cURKdGhMWjIwRXZScWdaejkyV2tsM2JudC9IV3VvRXZGZHFFUnl3VlJ5VlZISlVVanVwTWs5Z0UzYTNyeUhLakVGQm9JZVpKSVloblRXNllOb1c3OG1odi9LMy9XL0JqcFNoYTJ5a3Y2M2VtVDVYT21QTDBRSXBhV1hCUW1kQ2cyQWRBaTRWTHk2Rm1MWUVjcHZ5UmpPeWJXdXd6eFE5WXdKZXZSTXRLZUZMVkpDcnBpZHZFay9zcVlJUzZtYkFTd1U4dlVCNzhjVkNXR0loYWdsVHMwSXVSRTJ4L2h6WVp0aVRWMnN3YzdieGV2eGRoN3Y1R0NmL3lkME9RTTZOL0VyS2R3L29pZllHR3A2cEJUVjZwWjYyWHNrdUViKzBqMTJCRDJjTlo4VFNGTmdDRDl6Tjk4ZWg3dGtxUGJ0VG13a1oxLy9JL2N1clNSczZFQ2U1S1MrU2UwWEdIaEtBb01CVCszUU1BVDlmZDBqUllDeW12RGF4M0dsaHo4TVdPcnlZNDdUMEdq')
    context = res.json()
    
    text = ""
    for i in range(5):
        text += str(i)+". " + context[i]['a'] + " " + context[i]['tp'] + "\n"
    return text

@handler.add(MessageEvent, message=TextMessage)
def RequestHousePrice(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        if event.message.text == "給我房價":
            text = request_house_price()
        else:
            text = "功能尚未開發"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        )