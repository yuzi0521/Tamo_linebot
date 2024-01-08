import random
from flask import Flask,request,abort
import requests
from bs4 import BeautifulSoup
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage,ImageSendMessage,TemplateSendMessage,ButtonsTemplate,URIAction

app = Flask(__name__)

line_bot_api = LineBotApi('b6Yr6ImGsgJoygWCAGbZmXUlD9iwxq4kCMK5LNp9uzHman2sTrmGcQg9WZjeTxE6ZI88OV3WCbY1TvfN+lBUhjII2Sa+8CE5uClDEMB3lO3yTlcj264aCAv1qhxn8zdzzIrx/FO6GcxiQWixcrikCwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('8b112654e7d0697aef4197483b03ab96')

@app.route("/callback",methods=['POST'])
def callback():
    signature = request.headers['X-Line_Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent,message=TextMessage)
def handle_massage(event):
    sendString=""

    if "擲筊" in event.message.text:
        sendString = divinationBlocks()
    elif "抽簽" in event.message.text or "抽" in event.message.text:
        sendString = drawStraws()

    elif "天氣" in event.message.text:
        sendString = winter()
    else:
       sendString = event.message.text 

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=sendString)
    )

def divinationBlocks():
    divinationBlocksList = ["笑杯", "正杯", "正杯", "笑杯"] 
    return divinationBlocksList[random.randint(0, len(divinationBlocksList) - 1)]

def drawStraws():
    drawStrawsList = ["大吉", "中吉", "小吉", "吉", "凶", "小凶", "中凶", "大凶"]
    return drawStrawsList[random.randint(0, len(drawStrawsList) - 1)]

def winter():

    token = 'CWA-C29C9217-F9F1-40E9-8C7F-B5B03FF2018E'

    url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=' + token + '&format=JSON'
    data = requests.get(url)
    data_json = data.json()
    location = data_json['records']['location']
    for i in location:
      name = i['locationName']                    # 測站地點
   
      print(name)

if __name__ == '__main__':
    app.run()