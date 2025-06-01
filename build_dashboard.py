#!/usr/bin/env python3
"""
build_dashboard.py

JSON で保存された最新フィード (data/latest.json) から
クリック式 HTML ダッシュボード (data/dashboard.html) を生成するスクリプト。

- Bootstrap 5 & vanilla‑DataTables (CDN) を使用
- 上部ボタンでキーワードごとのライブフィルタ
- tasks.json に "keywords" 配列と任意で "rules" {kw: min_seeders} を定義
"""

import json
import pathlib
import datetime
from jinja2 import Template

# --- 設定読み込み -------------------------------------------------------------

BASE   = pathlib.Path(__file__).parent
CONF   = json.loads((BASE / "tasks.json").read_text(encoding="utf-8"))
DATA   = json.loads((BASE / "data" / "latest.json").read_text(encoding="utf-8"))
KW     = CONF["keywords"]
RULES  = CONF.get("rules", {})        # 例: {"VR": 50, "無修正": 20}

# --- HTML テンプレート ---------------------------------------------------------

template = Template(r"""
<!doctype html>
<html lang="ja">
<meta charset="utf-8">
<title>Torrent Dashboard</title>

<link rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
<script src="https://cdn.jsdelivr.net/npm/vanilla-datatables@1.8.4/dist/vanilla-dataTables.min.js"></script>
<link rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/vanilla-datatables@1.8.4/dist/vanilla-dataTables.min.css">

<div class="container my-4">
  <h1 class="mb-3">
    Sukebei 最新フィード <small class="text-muted">{{ today }}</small>
  </h1>

  <!-- キーワードボタン -->
  <div class="btn-group mb-3" role="group">
    <button class="btn btn-outline-secondary active" data-kw="ALL">ALL</button>
    {% for kw in keywords %}
      <button class="btn btn-outline-primary" data-kw="{{ kw }}">{{ kw }}</button>
    {% endfor %}
  </div>

  <!-- データテーブル -->
  <table id="tbl" class="table table-striped table-sm">
    <thead>
      <tr><th>タイトル</th><th>Seeders</th><th>サイズ</th><th>DL</th></tr>
    </thead>
    <tbody>
    {% for r in data %}
      <tr data-title="{{ r.title | e }}"
          data-seeders="{{ r.seeders }}"
          data-tags="{{ ' '.join(tags(r.title)) }}">
        <td>{{ r.title }}</td>
        <td data-sort="{{ r.seeders }}">{{ r.seeders }}</td>
        <td>{{ r.size }}</td>
        <td><a href="{{ r.link }}" target="_blank">DL</a></td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
</div>

<script>
const kwBtns = document.querySelectorAll('[data-kw]');
const table  = new DataTable("#tbl", {perPage:50, perPageSelect:[10,25,50,100]});

kwBtns.forEach(btn=>{
  btn.addEventListener('click', ()=>{
    kwBtns.forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    const kw = btn.dataset.kw;
    const rows = document.querySelectorAll('#tbl tbody tr');
    rows.forEach(row => {
      if (kw === 'ALL') {
        row.style.display = '';
      } else {
        const tags = row.getAttribute('data-tags') || '';
        row.style.display = tags.split(' ').includes(kw) ? '' : 'none';
      }
    });
  });
});
</script>
</html>
""", autoescape=True)

# --- メイン処理 ----------------------------------------------------------------

def main() -> None:
    """
    JSON → HTML 変換を実行してファイルを出力する。
    """
    out_html = BASE / "docs" / "dashboard.html"
    out_html.parent.mkdir(exist_ok=True)

    out_html.write_text(
        template.render(
            today=datetime.date.today().isoformat(),
            keywords=KW,
            data=DATA,
            tags=lambda t: [kw for kw in KW if kw.lower() in t.lower()]
        ),
        encoding="utf-8"
    )
    print(f"dashboard updated → {out_html}")

if __name__ == "__main__":
    main()