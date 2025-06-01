# Sukebei スクレイパー & クリック式ダッシュボード

## 概要
- **`scrape.py`** が Sukebei RSS を取得し、`data/latest.json` に保存  
- **`build_dashboard.py`** が JSON から **静的 HTML** (`data/dashboard.html`) を生成  
- ブラウザで `dashboard.html` を開き、上部ボタンをクリックすると  
  登録キーワードごとにライブフィルタリングできる

## フォルダ構成

```text
scraper/
├─ data/                         # 自動生成ファイル置き場
│   └─ .gitkeep
├─ .github/
│   └─ workflows/
│       └─ scrape.yml            # GitHub Actions (自動実行)
├─ scrape.py                     # RSS → JSON
├─ build_dashboard.py            # JSON → HTML
├─ tasks.json                    # RSS URL & キーワード定義
├─ requirements.txt              # 依存ライブラリ
├─ .gitignore
├─ LICENSE                       # MIT
└─ README.md                     # このファイル
```

## ファイル詳細

| ファイル / ディレクトリ | 役割 |
|------------------------|------|
| **tasks.json** | RSS 取得先とボタン化するキーワードを定義。<br>`"rules"` でキーワード別 Seeders 下限も設定可能 |
| **scrape.py** | RSS をパースし、タイトル・Seeders・サイズ・リンクを JSON で保存 |
| **build_dashboard.py** | Jinja2 + Bootstrap + vanilla-DataTables を用いてダッシュボードを生成 |
| **data/latest.json** | スクレイピング生データ（自動生成） |
| **data/dashboard.html** | クリック式ダッシュボード（自動生成） |
| **scrape.yml** | GitHub Actions で 1 日 1 回自動実行し、ダッシュボードを更新・コミット |

## セットアップ

```bash
# 1. 仮想環境を作成 (任意)
python -m venv env
source env/bin/activate       # Windows は .\env\Scripts\activate

# 2. 依存ライブラリをインストール
pip install -r requirements.txt

# 3. 手動テスト
python scrape.py
python build_dashboard.py
open data/dashboard.html       # macOS。Windows は start, Linux は xdg-open
```

## cron 例（ローカル）

```bash
# 毎日 05:05 JST にジョブを実行
5 5 * * *  /usr/bin/python3 /path/to/scraper/scrape.py && \
           /usr/bin/python3 /path/to/scraper/build_dashboard.py >> /path/to/scraper/cron.log 2>&1
```

## GitHub Actions 設定

`.github/workflows/scrape.yml` により、次の処理が自動化されます。

1. `ubuntu-latest` ランナーを起動  
2. 依存ライブラリをインストール  
3. `scrape.py` → `build_dashboard.py` を順に実行  
4. `data/dashboard.html` をコミットし、GitHub Pages へ公開

### GitHub Pages 公開手順

1. **Settings → Pages** を開く  
2. *Source* を `main` ブランチ、*Folder* を `/data` に設定  
3. 数十秒後に `https://<ユーザー名>.github.io/scraper/dashboard.html` で公開

## 拡張ポイント

| 要望 | 変更点 |
|------|--------|
| キーワード追加 | `tasks.json` の `"keywords"` 配列に新語を追加 |
| Seeders 下限 | `tasks.json` の `"rules"` に `{ "Keyword": 下限値 }` を追加 |
| 公開場所変更 | `gh-pages` ブランチを使う場合は `scrape.yml` を修正 |
| モバイル最適化 | DataTables のレスポンシブ CSS を読み込むことで対応可能 |

## ライセンス

MIT License – 自己責任でご利用ください。
