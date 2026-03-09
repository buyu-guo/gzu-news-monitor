import requests
from bs4 import BeautifulSoup
import json
import os

URL = "https://law.gzu.edu.cn/2874/list1.htm"
DATA_FILE = "last_news.json"

def get_latest_news():
    r = requests.get(URL)
    r.encoding = "utf-8"

    soup = BeautifulSoup(r.text, "html.parser")

    first = soup.select("li a")[0]

    title = first.text.strip()
    link = first["href"]

    if not link.startswith("http"):
        link = "https://law.gzu.edu.cn" + link

    return {
        "title": title,
        "link": link
    }

def load_last():
    if not os.path.exists(DATA_FILE):
        return None

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_last(news):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(news, f, ensure_ascii=False)

def send_bark(title, body):

    bark_key = os.environ["BARK_KEY"]

    url = f"https://api.day.app/{bark_key}/{title}/{body}"

    requests.get(url)

def main():

    latest = get_latest_news()
    last = load_last()

    if last is None:
        save_last(latest)
        print("initialized")
        return

    if latest["title"] != last["title"]:

        print("new news detected")

        send_bark(
            "贵州大学法学院网站更新",
            latest["title"]
        )

        save_last(latest)

if __name__ == "__main__":
    main()
