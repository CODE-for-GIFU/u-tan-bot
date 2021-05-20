# うーたんbot

## 1. 用途

　岐阜市のぎふ長良川鵜飼のマスコットキャラクター、<br>
うーたんとその家族とのおしゃべりを楽しむCode for Gifu内限定のチャットBotです。

[岐阜市のうーたん紹介ページ](https://www.city.gifu.lg.jp/18104.htm)

## 2. 動作環境

### Webサーバー環境

[Heroku: u-tan-bot](https://dashboard.heroku.com/apps/u-tan-bot)<br>
言語：Python

### ユーザー環境

[Slack: CODE for Gifu](code4gifu.slack.com)

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

### 4. 読みやすいコードのために

#### Python Linter/Formatter

##### [pysen](https://github.com/pfnet/pysen)

[requirements.txt](./requirements.txt)にpysenを含めています。
以下のコマンドで誰でも簡単にpythonコードファイル(\*.py)の整形ができます。

```cmd
pysen run format
```

設定内容は、[pyproject.toml](./pyproject.toml)で確認できます。

### 5. デプロイ

当リポジトリのmainブランチを、herokuのAutoDeployに設定しています。
mainブランチへのcommitは、本番環境に即時展開されます。
