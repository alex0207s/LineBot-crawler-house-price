from flask import Flask
from linebot import LineBotApi, WebhookHandler
import configparser

app = Flask(__name__)

# 讀取 config
config = configparser.ConfigParser()
config.read('config.ini')

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

from app import routes, model_for_line