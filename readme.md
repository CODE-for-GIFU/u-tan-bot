# うーたんbot

## 1. 用途

　岐阜市のぎふ長良川鵜飼のマスコットキャラクター、<br>
うーたんとその家族とのおしゃべりを楽しむCODE for Gifu内限定のチャットBotです。

[岐阜市のうーたん紹介ページ](https://www.city.gifu.lg.jp/18104.htm)

## 2. 動作環境

### Webサーバー環境

[Heroku: u-tan-bot](https://dashboard.heroku.com/apps/u-tan-bot)<br>
言語：Python
#### Heroku App スリープ解除Bot

Herokuのフリープランでホストする場合、30分毎にAppがスリープ状態になる。<br>
うーたんBotの動作の妨げになるため、
[@tetsuji1122](https://github.com/tetsuji1122)氏の個人アカウントから、[UptimeRobot](http://uptimerobot.com/)を設定している。

### ユーザー環境

[Slack: CODE for Gifu](https://code4gifu.slack.com)

## 3. 開発環境

### 3-1. ローカル環境 構築手順

1.  Pythonインストール<br>
    バージョンは、[runtime.txt](./runtime.txt)と合わせる。

2.  仮想環境の作成(任意)<br>
    ・Windows

    ```cmd
    cd workspace
    py -3.8 -m venv venv 
    .\venv\Script\activate
    ```

    ・Linux

    ```bash
    cd workspace
    python3 -m venv venv
    source ./venv/bin/activate
    ```

3.  pipパッケージのインストール

    ```cmd
    pip3 install -r requirements.txt
    ```

### 3-2. 読みやすいコードのために

#### Python Linter/Formatter

##### [pysen](https://github.com/pfnet/pysen)

[requirements.txt](./requirements.txt)にpysenを含めています。
以下のコマンドで誰でも簡単にpythonコードファイル(\*.py)の整形ができます。

```cmd
pysen run format
```

設定内容は、[pyproject.toml](./pyproject.toml)で確認できます。

### 3-3. デプロイ

当リポジトリのmainブランチを、herokuのAutoDeployに設定しています。<br>
mainブランチへのcommitは、本番環境に即時展開されます。<br>
herokuでの環境構築後の起動については、[Procfile](./Procfile)に記載があります。<br>
