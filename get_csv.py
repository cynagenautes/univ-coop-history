import requests
import urllib
import datetime
from dateutil.relativedelta import relativedelta

USER = "your_member_id"
PASS = "your_password"

url_login = "https://mp.seikyou.jp/mypage/Auth.login.do"
url_csv = "https://mp.seikyou.jp/mypage/AllHistory.csvDownload.do"

# セッション開始(これ使わないとセッションが切れるので絶対いる)
session = requests.session()

login_info = {
    "loginId": USER,
    "password": PASS
}

# ログインはフォームデータにPOSTするだけ
login = session.post(url_login, data=login_info)
login.raise_for_status() # エラーならここで例外を発生させる


def fetch_history(rireki_date):
    csv_post = {
        "rirekiDate": rireki_date
    }

    #SJISで送ってるのでそれ用に変換
    csv_post = urllib.parse.urlencode(csv_post, encoding='shift-jis')

    header = {
        "Content-Type": "application/x-www-form-urlencoded"}

    csv = session.post(url_csv, data=csv_post, headers=header)
    csv.raise_for_status() # エラーならここで例外を発生させる
    print(csv.text)


today = datetime.date.today()

fetch_history(today.strftime('%Y年%m月'))

# Webのほうでは12ヶ月しか履歴出せないけど13ヶ月前の日付送っても500エラーにはならなかった 来年以降、要検証
for i in range (12):
    rireki_date = today + relativedelta(months=-i)
    fetch_history(rireki_date.strftime('%Y年%m月'))