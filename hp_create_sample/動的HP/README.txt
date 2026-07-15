growship スクロール航海サイト（4クリップ版プロトタイプ）

■ 動かし方（ローカルサーバー推奨）
  このフォルダで:
    python -m http.server 8000   →  http://localhost:8000
  ※直接ダブルクリックでも動くことが多いですが、画像読込がブロックされる場合はサーバー経由で。

■ 構成
  index.html   … 本体（canvas + GSAP ScrollTrigger）
  frames/      … 4クリップを航海順につなぎフレーム化した連番画像 297枚
  voyage.mp4   … つないだ元動画（参考）

■ 航海順（左から右へスクロールで進行）
  ①正面・日中 → ②巡航・日中 → ④港へ接近・黄金 → ③港で夕日（クロスフェード接続）

■ 差し替え
  ・テキスト: index.html の各 <section class="panel"> を編集。
  ・映像: 新クリップを voyage 順につなぎ、frames/ を再生成。FRAME_COUNT も合わせる。
      ffmpeg -i voyage.mp4 -vf "fps=16" -q:v 4 frames/f_%03d.jpg
