import os
from dotenv import load_dotenv

import assistant
from slack_bolt import App

load_dotenv()

BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")

app = App(
    token = BOT_TOKEN,
    signing_secret = SIGNING_SECRET
)

# 'hello' を含むメッセージをリッスンします
@app.message("debug-code")
def message_hello(message, say):
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    #rst_message_text = assistant.message_less("ペア")["generic"][0]
    #print(rst_message_text)
    say("debug-code" +f"<@{message['user']}>!")

@app.message("")
def message_session(message, say):
    print(message)
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    session_id = assistant.create_session()
    rst_message_text = assistant.message(session_id,message["text"])
    print(rst_message_text)
    say(rst_message_text["generic"][0]["text"]+f"<@{message['user']}>!")

    assistant.delete_session(session_id)   

    # appに関連づけられたbotに対するメンションイベントを処理します
@app.event(r"app_mention")
def read_mention_message(event, say):
    text = event[r"text"]
    say("{0}".format(text))

# アプリを起動します
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
