# Isct-Data

公開データは Science Tokyo（旧・東京工業大学）の公式ページと公式PDFから抽出しています。日付は JST です。

## 公式入口

- 授業日程（2026）: https://www.titech.ac.jp/student/students/life/schedules
- 授業日程（2025）: https://www.titech.ac.jp/student/students/life/schedules/2025
- 学士課程補講・期末試験: https://www.titech.ac.jp/student/students/life/undergraduate-exam
- 大学院補講・期末試験: https://www.titech.ac.jp/student/students/life/graduate-exam

## カバレッジ

- 2025: 校暦と学部入学者用学科データ。公式の年度別試験時間割アーカイブは確認できなかったため、試験データは未収録です。未掲載は試験が存在しないことを意味しません。
- 2026: 校暦、学部・大学院の公式 2Q 期末試験時間割（授業行を除外し、視覚確認で取り消し線の旧行を除外）。

重要日程（入学式、学位記授与式、ホームカミングデイ、大学祭、入試等）は `important-dates/` に独立収録しています。重要日程は休講を意味せず、休講情報は校暦の `days` に記録します。

公開ファイルは年度単位のフラットなパス（`academic-calendar/2025.json`、`departments/2025.json`、`important-dates/2025.json`）です。試験は `exam/undergraduate/2026-2q.json` と `exam/graduate/2026-2q.json` に収録しています。

試験PDFは公式入口の更新版を取得し、各エントリに出典ページを記録しています。時限はPDFの割当（例: 3-4）で、正確な開始・終了時刻は推測していません。

試験データではPDFに記載された英語科目名を `label.en` にそのまま収録しています。試験PDFに開始・終了時刻の記載がないため、`periods` のみを使用しています。

入学案内の付表・標準履修例からコースコードを抽出し、2025/2026 の全学系ファイルへ収録しています。コード差集で他系科目・共通科目の参照が混在する箇所は `scripts/review_course_coverage.py` の出力を人手確認中です。2025化学系はPDF固有のASCIIフォント符号を復号済み、2025融合理工学系は公式OCRとページ画像を照合済みです。空配列は「推薦科目なし」を意味しません。
2025化学系は47コード、2025融合理工学系はOCR確認した公式付表行を収録済みです。PDF変換不能・文字化け・画像表は、公式PNG/OCRを照合してから登録します。空配列は「推薦科目なし」を意味しません。
