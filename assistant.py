import json
import os

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import AssistantV2

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    print(__file__ + r":環境変数の読込にdotenvを使用せず続行します。")

API_KEY = os.getenv("WATSON_API_KEY")
SERVICE_URL = os.getenv("WATSON_SERVICE_URL")
ASSISTANT_ID = os.getenv("WATSON_ASSISTANT_ID")

authenticator = IAMAuthenticator(API_KEY)
assistant = AssistantV2(version="2020-09-24", authenticator=authenticator)
assistant.set_service_url(SERVICE_URL)


def main():
    print("start")
    # セッションフルな会話　セッションの保持はWatson側。クライアントはsession_idのみ渡す
    session_id = create_session()
    print(session_id)
    print(message(session_id, "ペア"))
    print(message(session_id, "あいこ"))
    delete_session(session_id)

    # セッションレスな会話
    print(message_less("ペア"))
    print(message_less("あいこ"))

    print("end")


def create_session():
    session_id = assistant.create_session(assistant_id=ASSISTANT_ID).get_result()[
        "session_id"
    ]
    return session_id


def delete_session(session_id):
    response = assistant.delete_session(
        assistant_id=ASSISTANT_ID, session_id=session_id
    ).get_result()


def message(session_id, msg, context={}):
    response = assistant.message(
        assistant_id=ASSISTANT_ID,
        session_id=session_id,
        input={"message_type": "text", "text": msg},
        context=context,
    ).get_result()
    return response["output"]


def message_less(msg):
    response = assistant.message_stateless(
        assistant_id=ASSISTANT_ID, input={"message_type": "text", "text": msg}
    ).get_result()
    return response["output"]


def get_top_intent(response_output: dict):
    if not r"intents" in response_output.keys():
        return None, r"No intents key in dict."

    if len(response_output[r"intents"]) <= 0:
        return None, r"No intent list."

    top_intent = response_output[r"intents"][0][r"intent"]

    return top_intent, r""


if __name__ == "__main__":
    main()
