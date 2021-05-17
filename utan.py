import os

import assistant
from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    print(__file__ + r":環境変数の読込にdotenvを使用せず続行します。")

utan = App(
    token=os.getenv(r"UTAN_BOT_TOKEN"), signing_secret=os.getenv(r"UTAN_SIGNING_SECRET")
)

# utanに関連づけられたbotに対するメンションイベントを処理します
@utan.event(r"app_mention")
def read_mention_message(event, say):
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します

    text: str = event[r"text"]

    # ユーザーの入力テキストから、@メンション文を削除
    text = text.replace(text[text.find(r"<@") : (text.find(r">") + 1)], r"")

    # ユーザーの入力テキストから、改行を削除（対 Watson入力エラー）
    text = text.replace("\n", r"")

    # Watson APIに渡して、解析
    res_output = assistant.message_less(text)

    # 確信度が一番高い、意図を取得
    intent, error = assistant.get_top_intent(res_output)

    # 意図が取得できない場合、エラーを通知
    if intent is None:
        say(r"解析エラーやで、あかんわ。:" + error)
        return

    # 意図を返事する
    say(r"{0}".format(intent))


app = Flask(__name__)
handler = SlackRequestHandler(utan)


@app.route(r"/")
def index():
    return r"I am うーたん bot."


@app.route(r"/slack/events", methods=[r"POST"])
def slack_events():
    return handler.handle(request)


# アプリを起動します
if __name__ == r"__main__":
    utan.start(port=int(os.environ.get(r"PORT", 3000)))
