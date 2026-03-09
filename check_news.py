import requests
from bs4 import BeautifulSoup
import json
import os

URL = "https://law.gzu.edu.cn/2874/list1.htm"
DATA_FILE = "last_news.json"


def get_latest_news():
    """Fetch the latest news from website"""

    r = requests.get(URL, timeout=20)
    r.encoding = "utf-8"

    soup = BeautifulSoup(r.text, "html.parser")

    links = soup.find_all("a")

    for a in links:

        title = a.get_text(strip=True)
        link = a.get("href")

        if not title or not link:
            continue

        if ".htm" in link and len(title) > 5:

            if not link.startswith("http"):
                link = "https://law.gzu.edu.cn" + link

            return {
                "title": title,
                "link": link
            }

    raise Exception("No news found")


def load_last():
    """Load last stored news"""

    if not os.path.exists(DATA_FILE):
        return None

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:

            text = f.read().strip()

            if not text:
                return None

            return json.loads(text)

    except:
        return None


def save_last(news):
    """Save latest news to json"""

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(news, f, ensure_ascii=False)


def send_bark(title, body, url):
    """Send Bark notification"""

    bark_key = os.environ.get("BARK_KEY")

    if not bark_key:
        print("No Bark key found")
        return

    bark_url = f"https://api.day.app/{bark_key}/{title}/{body}?url={url}"

    try:
        requests.get(bark_url, timeout=10)
        print("Bark notification sent")

    except Exception as e:
        print("Bark failed:", e)


def main():

    latest = get_latest_news()

    print("Latest news:", latest)

    last = load_last()

    # First run or corrupted json
    if not last or "title" not in last:
        print("First run, initializing...")
        save_last(latest)
        return

    if latest["title"] != last["title"]:

        print("New news detected!")

        send_bark(
            "贵州大学法学院网站更新",
            latest["title"],
            latest["link"]
        )

        save_last(latest)

    else:
        print("No update")


if __name__ == "__main__":
    main()
