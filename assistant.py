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

AIRTABLE_SERVICE_URL = os.getenv("AIRTABLE_SERVICE_URL")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")


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


# input：Watson - Message
# Output：WatsonとairtableApiのどちらかを出力(airtableがあれば、airtableを出力)
#  [{
#  'intent' : string,
#  'comment': string,
#  'UMember': string
#  }]
def utan_message_Switcher(watson_message):
    intents = watson_message["intents"][0]
    message = watson_message["generic"][0]
    utan_message = []

    # URLの整理・Airtable-APIからメッセージを取得
    url = AIRTABLE_SERVICE_URL
    intent_words = intents["intent"]
    filterByFormula_words = 'AND(intent="' + intent_words + '")'
    req_header = {
        "api_key": AIRTABLE_API_KEY,
        "filterByFormula": filterByFormula_words,
        "Content-Type": "application/json",
    }

    req = urllib.request.Request(
        "{}?{}".format(url, urllib.parse.urlencode(req_header))
    )
    try:
        with urllib.request.urlopen(req) as response:
            body = json.loads(response.read())

    except urllib.error.URLError as e:
        print(e.reason)

    # airtableのデータがあるかどうかで、watsonかairtableどちらを使用するか選定
    records = body["records"]
    if not records:
        utan_message.append(
            {"intent": intents["intent"], "comment": message["text"], "UMember": "うーたん"}
        )

    else:
        fields = []
        group_no_max = 0
        for i in range(len(records)):
            fields.append(records[i]["fields"])
            if fields[i]["group_no"] > group_no_max:
                group_no_max = fields[i]["group_no"]

        # ID順に整理
        fields = sorted(fields, key=lambda x: x["ID"])

        # Group-Noでランダムに選定
        fields_group = []
        group_no = random.randint(1, group_no_max)
        for i in range(len(fields)):
            if fields[i]["group_no"] == group_no:
                fields_group.append(fields[i])
                utan_message.append(
                    {
                        "intent": fields[i]["intent"],
                        "comment": fields[i]["comment"],
                        "UMember": fields[i]["UMember"],
                    }
                )

    return utan_message


if __name__ == "__main__":
    main()
