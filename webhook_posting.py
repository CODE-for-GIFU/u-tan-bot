import json
import os
import random
import time
from enum import Enum

import requests

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    print(__file__ + r":環境変数の読込にdotenvを使用せず続行します。")


class WebhookPosting:
    class ScriptKeys(Enum):
        Comment = r"comment"
        UMember = r"UMember"

    class UMember(Enum):
        Utan = r"うーたん"
        Utako = r"うたこ"
        Urun = r"うーるん"
        Utaro = r"うーたろ"

    __UTAN_WEBHOOK = os.getenv(r"UTAN_INCOMING_WEBHOOK")
    __UTAKO_WEBHOOK = os.getenv(r"UTAKO_INCOMING_WEBHOOK")
    __URUN_WEBHOOK = os.getenv(r"URUN_INCOMING_WEBHOOK")
    __UTARO_WEBHOOK = os.getenv(r"UTARO_INCOMING_WEBHOOK")

    def __get_umember_type(self, member_name: str) -> UMember:
        assert isinstance(member_name, str)

        if self.UMember.Utan.value == member_name:
            return self.UMember.Utan
        elif self.UMember.Utako.value == member_name:
            return self.UMember.Utako
        elif self.UMember.Urun.value == member_name:
            return self.UMember.Urun
        elif self.UMember.Utako.value == member_name:
            return self.UMember.Utaro
        else:
            AssertionError(r"Unknown UMember Name: " + member_name)

    def __get_webhook_url(self, member: UMember):
        if member == self.UMember.Utan:
            return self.__UTAN_WEBHOOK
        elif member == self.UMember.Utako:
            return self.__UTAKO_WEBHOOK
        elif member == self.UMember.Urun:
            return self.__URUN_WEBHOOK
        elif member == self.UMember.Utaro:
            return self.__UTARO_WEBHOOK
        else:
            AssertionError(r"Undefined UMember Type" + member)

    def __call__(self, script: list):
        assert isinstance(script, list)

        for item in script:
            assert isinstance(item, dict)

            umember = item[self.ScriptKeys.UMember.value]
            comment = item[self.ScriptKeys.Comment.value]

            webhook = self.__get_webhook_url(self.__get_umember_type(umember))

            self.__post_incoming_webhook(url=webhook, comment=comment)

            time.sleep(1 + random.randint(0, 5) * 0.1)

    def __post_incoming_webhook(self, url: str, comment: str):
        requests.post(url=url, data=json.dumps({r"text": comment}))
