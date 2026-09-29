# 東建多度CC・名古屋 1番ホール 10秒PR動画 — Google Vids 用 素材とプロンプト

## 構成（推奨：A案）

| 案 | 内容 | 使う画像 | 向いている場合 |
|---|---|---|---|
| **A. 1カット（推奨）** | フェアウェイ上空からグリーンへ向かって前進する1本の空撮 | `05_mid_wide.png`（別案：`02_tee_rise.png`） | 画像1枚から1本の動画を生成する場合。つなぎ目がなく、形が崩れにくい |
| B. 3カット | ティー（約3秒）→ FWバンカー（約3秒）→ グリーン（約4秒） | `01_tee.png` / `04_fw_bunker.png` / `07_green.png` | 1本10秒の中に複数のクリップを並べられる場合 |

※ Google Vids の機能名・画像入力の可否・生成できる長さ・商用利用条件はプランや時期で変わります。使用前に最新の画面と規約を確認してください（未確認）。

---

## A案：1カット 10秒

**画像**：`05_mid_wide.png`（フェアウェイ・バンカー・池・グリーンが1枚に収まり、いちばん見栄えがよい）

別案：ティーから始めたい場合は `02_tee_rise.png`（手前の木が多く、フェアウェイが狭く見える）

**プロンプト（英語のまま貼り付け）**
```
Cinematic 10-second drone shot of a long par-5 golf hole in Japan on a clear summer morning. The camera starts high above the fairway and glides smoothly forward toward the green, over a wide fairway with light-and-dark mowing stripes, white sand bunkers, a calm pond with a winding cart path on the right, and the green ahead, framed by lush broadleaf and cedar forest and rolling hills with soft haze. Keep the exact layout from the input image: the positions and shapes of the fairway, bunkers, green and cart path must not change. Photorealistic, vivid green turf, blue sky with a few cumulus clouds, soft natural sunlight and shadows. Stable, smooth camera motion. No people, no golf carts, no text, no logos, no watermarks.
```

**日本語の意味**：夏の晴れた朝、フェアウェイ上空からグリーンへ滑らかに前進する10秒の空撮。縞模様のフェアウェイ、白いバンカー、右手の池とカート道、奥のグリーン、周りの森と丘。入力画像のレイアウト（フェアウェイ・バンカー・グリーン・カート道の位置と形）は変えない。人・カート・文字・ロゴなし。

**テロップ（2行、全編表示）**
```
東建多度カントリークラブ・名古屋
1番ホール　PAR5　540Y
```

---

## B案：3カット（約3秒＋3秒＋4秒）

共通の末尾（各プロンプトの最後に付ける）
```
Keep the exact layout from the input image. Photorealistic summer morning, blue sky, vivid green turf with mowing stripes. Smooth, stable drone motion. No people, no golf carts, no text, no logos, no watermarks.
```

**カット1（約3秒）** `01_tee.png`
```
A drone slowly glides forward at eye level from the tee box, revealing a wide striped fairway bending gently to the right, a small green-roofed gazebo and clipped hedges on the left.
```
テロップ：`1番ホール　PAR5　540Y`

**カット2（約3秒）** `04_fw_bunker.png`
```
The drone flies forward past a large clover-shaped white sand bunker on the right side of the fairway, trees scattered in the rough.
```
テロップ：`右のバンカー越えは250ヤード超`（公式サイトの記述に基づく）

**カット3（約4秒）** `07_green.png`
```
Slow forward drone shot toward an oval putting green guarded by white bunkers on the left and right, the red flag moving slightly in the breeze, forest behind.
```
テロップ：`東建多度カントリークラブ・名古屋`

---

## 画像一覧（すべて 1920×1080）

| ファイル | 場面 |
|---|---|
| `01_tee.png` | ティー（目線の高さ） |
| `02_tee_rise.png` | ティー上空 |
| `03_fairway_low.png` | フェアウェイ低空 |
| `04_fw_bunker.png` | FW右バンカー |
| `05_mid_wide.png` | 高所からの全景（A案推奨） |
| `06_approach.png` | アプローチ（右に池） |
| `07_green.png` | グリーン |
| `08_pin.png` | ピン |

画像は3Dの素材そのままで、鉄塔・竹林はまだ入っていません。植え込みは暗い塊に見えます。生成AIが補う前提です。

## 出典・注意書き（動画の概要欄、または最後の1秒に表示）

```
国土地理院の基盤地図情報 数値標高モデル（5mメッシュ・10mメッシュ）および地理院タイル（全国最新写真・シームレス）を加工して作成した3Dデータをもとに、AIで生成したイメージ映像です。実際のコースとは異なる部分があります。
出典：国土地理院／コース情報：東建多度カントリークラブ・名古屋 公式サイト
```
10秒の中に入れにくい場合は、動画の説明文（概要欄）に記載してください。

## 公開前の確認事項

- ゴルフ場名・コース情報を使ったPR動画の公開：ゴルフ場側の許諾の要否
- AI生成映像であることの明示
- Google Vids・生成AI機能の利用規約（商用利用の可否）
- 国土地理院コンテンツの利用条件（出典の明示、加工した旨の記載）
