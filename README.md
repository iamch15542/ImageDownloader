# CYYImageDownloader


## 使用說明
1. 在terminal 輸入 python3 CYYImageDownloader.py 開啟
2. 開啟後直接輸入網址即可
3. 若要結束程式，```請輸入 'q' 再按開始下載```或是```直接點選結束程式```

## 輸入網址範例
* PTT
   * 文章網址即可
	* https://www.ptt.cc/bbs/Beauty/M.1625575802.A.266.html
* Dcard
	* 文章網址即可
	* https://www.dcard.tw/f/relationship/p/236435574
* Instagram
	* 要用 Post 的網址才行，會是 `https://www.instagram.com/p/????????/` 這樣
	* EX: https://www.instagram.com/p/CQ5l1VWMJEd/

## 版本
Version 7.0.1

## 更新內容
Version6.3.1: 修正 Dcard 留言 bug, 修正 pixnet 檔名錯誤問題

Version6.3.2: 修正 imgur 圖片下載

Version6.3.3: 使用 imghdr 判斷圖片類型，修正小問題

Version6.3.4: 修正圖片下載問題

Version7.0.1: 修復 Instagram 下載問題, Ptt word 輸出錯誤


## 注意事項
1. 僅支援 PTT, Dcard, Instagram, Pixnet 網址，其餘網址皆會視為無效網址
2. 請勿拿來做非法事項
3. 若有任何 bug，歡迎告知

## TODO List
1. 下載 gif 圖片的功能
2. 輸出不同的 Error Code，來辨識出錯項目

## 需求
* 以下為我使用的 package 的版本
	* Python 3.7.6
	* python-docx: 0.8.10
	* bs4: 0.0.1
	* requests: 2.23.0
	* Pillow: 6.1.0
	* beautifulsoup4: 4.6.3

## 免責聲明
此程式為本人寫來自用的，若有發生任何問題，本人一概不負責

## 參考
[Imgur album 正則表達式](https://github.com/alexgisby/imgur-album-downloader/blob/master/imguralbum.py)
[使用 imghdr 判斷圖片](https://docs.python.org/3/library/imghdr.html)