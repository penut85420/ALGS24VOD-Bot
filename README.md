# ALGS 24HR VOD

## 使用方法
1. 使用 `Run.ps1` 啟動程式

## 設定說明
+ 相關的參數設定放在 `Config.json` 裡面
+ 即便程式在執行中也可以直接修改設定，不用重新啟動
+ `client_id`, `client_secret`, `access_token` 與 `cookie` 屬於登入用的機密資訊，切勿外漏
+ `target_dir` 是放置 VOD 的目錄路徑，路徑中的反斜線必須重複兩次
+ `broadcaster_id` 是想要修改標題的頻道 ID
+ `timer` 是指程式多久檢查一次 PotPlayer 的播放檔案，單位為秒
+ `message_timer` 在聊天室推播訊息的時間間隔，單位為秒
+ `title_fmt` 是標題格式，使用 `%s` 代表檔案名稱要擺的位置
+ `message_fmt` 要推播到聊天室的訊息格式，使用 `%s` 代表檔案名稱要擺的位置

## 授權
本軟體使用 MIT 授權條款
