from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('SEj0ATQYEE8AwGHW+f8iIX95OTz/Pw9v+H0UdgU+vGdyUjpOFiVT4kQIqOKtejxYFtEc4C5idZSkM7Rru1rui0GlN3sAMx+IAV6Wn33NsZ2Tm8CfU6LebxylXvyHIBcTv1JwbeefU6JJu4CuBYMRogdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('59efc3ed8602bc77ce971ad68561a377')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()