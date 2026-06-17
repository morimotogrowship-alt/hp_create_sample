# LUXIA HAIR — 静的サイト

ヘアサロン「LUXIA HAIR」の静的ウェブサイトです。HTML / CSS / JavaScript のみで構成され、ビルド不要・サーバー不要でそのまま公開できます。

## フォルダ構成

```
luxia-hair-site/
├── index.html        トップページ
├── concept.html      コンセプト
├── style.html        ヘアスタイルギャラリー
├── salon.html        サロン一覧
├── menu.html         メニュー・料金
├── campaign.html     キャンペーン
├── news.html         お知らせ
├── reserve.html      ご予約フォーム
├── contact.html      お問い合わせ + FAQ
├── css/
│   └── style.css     全ページ共通スタイル
├── js/
│   └── main.js       ヘッダー/フッター生成・スライダー・フォーム・モバイルメニュー
└── assets/           画像（ロゴ・モデル・店舗・バッジ など）
```

ヘッダーとフッターは `js/main.js` が全ページに自動で挿入します（1か所を直せば全ページに反映されます）。

## ローカルで確認する

JavaScript がページを読み込むため、`index.html` をダブルクリックするだけでは一部が表示されない場合があります。簡易サーバーで開いてください。

```bash
# Python が入っている場合
cd luxia-hair-site
python3 -m http.server 8000
# ブラウザで http://localhost:8000 を開く
```

## GitHub で公開する（GitHub Pages）

1. GitHub で新しいリポジトリを作成（例: `luxia-hair`）。
2. このフォルダの中身（`index.html` などが直下に来るように）をアップロード／push。
   ```bash
   cd luxia-hair-site
   git init
   git add .
   git commit -m "Initial commit: LUXIA HAIR site"
   git branch -M main
   git remote add origin https://github.com/<ユーザー名>/<リポジトリ名>.git
   git push -u origin main
   ```
3. リポジトリの **Settings → Pages** を開く。
4. **Source** で `Deploy from a branch` を選び、Branch を `main` / `/ (root)` に設定して保存。
5. 数分後、`https://<ユーザー名>.github.io/<リポジトリ名>/` で公開されます。

## 注意事項（このサイトでできること / できないこと）

- フォーム（ご予約・お問い合わせ）は**画面上の動作のみ**で、送信ボタンを押すと完了画面が出ますが、実際のメール送信やデータ保存は行いません。実運用には Formspree などの外部フォームサービスや、サーバー側の処理が別途必要です。
- 写真はすべて `assets/` 内の画像を使用しています。差し替える場合は同名で上書きするか、各HTMLの `src` を変更してください。
- 日本語フォント（Shippori Mincho / Noto Sans JP）と欧文フォント（Cormorant Garamond）は Google Fonts から読み込んでいます（インターネット接続が必要）。

## カスタマイズの目安

- 色・余白・フォント → `css/style.css` 冒頭の `:root` 変数
- メニュー項目・リンク先 → `js/main.js` の `NAV` / `buildFooter`
- 各ページの本文 → 各 `*.html`
