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

試験PDFは公式入口の更新版を取得し、各エントリに出典ページを記録しています。時限はPDFの割当（例: 3-4）で、正確な開始・終了時刻は推測していません。

試験データではPDFに記載された英語科目名を `label.en` にそのまま収録しています。試験PDFに開始・終了時刻の記載がないため、`periods` のみを使用しています。

入学案内の推薦科目は、2025年度・2026年度とも CS（情報理工学院系）の39科目を実データとして収録済みです。次の学系は公式入学案内の存在を確認していますが、推薦科目一覧の構造化抽出は未完了です：math、physics、chemistry、eps、mech、sc、ee、ict、ie、mat、chem-eng、mcs、life、arch、civil、transdisciplinary。空配列は「推薦科目なし」を意味しません。
