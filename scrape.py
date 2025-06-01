

#!/usr/bin/env python3
"""
scrape.py

Sukebei RSS を取得して `data/latest.json` に保存するスクリプト。

- 取得先 URL は tasks.json の "rss_url" で指定
- フィード要素: title / link / size / seeders / published
- ネットワーク失敗時は最大 3 回リトライ (3 秒間隔)
"""

import json
import pathlib
import datetime
import time
import logging
from typing import List, Dict

import feedparser

# --------------------------------------------------------------------------- #
# 設定読み込み
# --------------------------------------------------------------------------- #

BASE      = pathlib.Path(__file__).parent
CONF_PATH = BASE / "tasks.json"
DATA_DIR  = BASE / "data"
DATA_DIR.mkdir(exist_ok=True)

CONF      = json.loads(CONF_PATH.read_text(encoding="utf-8"))
RSS_URL   = CONF["rss_url"]
OUT_JSON  = DATA_DIR / "latest.json"

# --------------------------------------------------------------------------- #
# RSS 取得関数
# --------------------------------------------------------------------------- #

def fetch_rss(url: str, retries: int = 3, delay: float = 3.0) -> List[Dict]:
    """
    RSS フィードを取得し、辞書のリスト形式で返す。

    Args:
        url (str): RSS フィード URL
        retries (int): リトライ回数
        delay (float): 失敗時の待機秒数

    Returns:
        List[Dict]: 取得結果
    """
    for attempt in range(1, retries + 1):
        try:
            feed = feedparser.parse(url)
            rows: List[Dict] = []
            for e in feed.entries:
                rows.append({
                    "title":     e.title,
                    "link":      e.link,
                    "size":      e.get("nyaa_size", ""),
                    "seeders":   int(e.get("nyaa_seeders", 0)),
                    "published": e.published
                })
            return rows
        except Exception as exc:
            logging.error("RSS fetch failed (%s/%s): %s", attempt, retries, exc)
            if attempt < retries:
                time.sleep(delay)
    raise RuntimeError("RSS fetch failed after retries")

# --------------------------------------------------------------------------- #
# メイン処理
# --------------------------------------------------------------------------- #

def main() -> None:
    rows = fetch_rss(RSS_URL)
    OUT_JSON.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"[{datetime.date.today().isoformat()}] fetched → {OUT_JSON}")

if __name__ == "__main__":
    main()