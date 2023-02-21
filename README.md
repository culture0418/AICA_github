# AICA_github
修習人工智慧運算與應用課程的資料，包含作業與期末專題：唇語辨識密碼鎖

## demo video link
https://drive.google.com/drive/folders/1oY8JbZw8eovWDnsYh-BMLD646ZBO6mVH?fbclid=IwAR0Bl97tOvkGqflLM5jgwxegTgRVQuerzDJlL4gBlU_rTri-K0AL2wFhVBE

## Team members
| Name         | School ID | Email                     |
| ------------ | --------- | ------------------------- |
| 陳慕丞        | E94096097 | e94096097@gs.ncku.edu.tw  |
| 陳玟樺        | E44081042 | nicole6328@gmail.com      |
| 黃任廷        | E64064052 |  tim506877@gmail.com      |
| 宋方瑜        | E94094045 |  e94094045@gs.ncku.edu.tw |


## Preface

- 題目:唇語辨識密碼鎖
- 動機:想要解鎖時在有人的情況下能降低暴露密碼的風險，且能免除按密碼的不便利性。


## Project Overview



### Project Scope 

- 紅外線偵測與臉部辨識
- 辨識唇形
- 轉成文字檔
- 利用樹莓Pi辨識文字檔，若符合密碼則開鎖
- 固定位置
- 單一人臉

### Target Audience
- 對於密碼的隱蔽性有高要求與強調便利開鎖的使用者



### Constraints 
- 英文(特定的語句順序)  {bin, lay,place, set}, {blue, green, red, white}, {at, by, in, with}, {A, . . . , Z}\{W}, {zero, . . . , nine}, and {again, now, please, soon}
- 正面對著鏡頭
- 固定距離
- 一句話講完


## Project Decomposition and Planning
- 偵測臉部是否在正確位置
- 錄影使用者的唇形
- 模型辨識唇形是哪些字
- 樹莓Pi辨識文字檔與密碼是否相符
- 若相符則通電使電子鎖開啟
- ( 建立字彙資料庫, 訓練LipNet模型 ) - 如果需要training model的話

## Project Expectation

1. Project Focus
- 偵測臉部位置盡量精準
- 脣形辨識準確率盡量提高
- LipNet在RPi的implementation (by docker)
- 辨識文字檔與儲存文字檔系統 
- 正確implement電路

2. What does your application look like? 

- 紅外線偵測是否有人在前面，開啟RPI人臉辨識，偵測臉部停留幾秒，打開Pi-camera錄影功能，並固定在一個位置(**實際操作後會決定固定的位置**)，以筆電連線RPi並再使用該功能時能顯示camera的即時影像，講完密碼後人臉離開表示錄影結束，將影片檔input到LipNet並辨識，若成功顯示成功並開鎖，若失敗則顯示密碼不正確。

3. How are you going to test your application?
- 辨識率, 確認唇語符合使用者的語意，辨識正確的字數比例(or CER,WER)
- 紅外線正確辨識距離
- 人臉辨識程式正確辨識
- 電路正確通電開鎖


## Solution Proposals
- 利用樹莓pi辨識人臉以及脣形並辨識密碼是否正確，如正確則開鎖。


## ALGORITM

- 使用字彙資料庫 LRW

- 使用LipNet作為我們的AI辨識

- 查看論文以最佳化LipNet model

### Workflow
![image](https://user-images.githubusercontent.com/95466200/220358565-ea058f53-e74a-4707-97d1-0e918f65fbe0.png)

- 1.紅外線偵測使用者站到固定位置

- 2.開啟臉部辨識程式(此時mobaxterm開啟Pi-camera偵測影像)

- 3.若辨識臉部在正確範圍數秒則開始錄影(此時mobaxterm顯示開始錄影)

- 4.使用者在講完密碼後將臉部移開鏡頭

- 5.臉部辨識程式此時偵測到臉部不在正確範圍內時則關閉此程式並停止錄影

- 6.紅外線停止偵測到門鎖解開後數秒或辨識密碼錯誤

- 7.將影片檔input進LipNet辨識

- 8.辨識出的文字檔若 (1)與密碼相符合則mobaxterm顯示密碼正確並通電開鎖 (2)不符合則mobaxterm顯示密碼錯誤

- 9.將影片檔刪除

- 10.紅外線重新開啟偵測功能

## 困難點
- 影片前處理
![image](https://user-images.githubusercontent.com/95466200/220359107-99405a5a-f282-4de2-bb62-dd8c4ffc6f37.png)

- 問題改善
![image](https://user-images.githubusercontent.com/95466200/220359396-b4f5e8cb-b75a-415a-9167-aca15fdd486b.png)

![image](https://user-images.githubusercontent.com/95466200/220359517-7e59fc36-e4e3-40a5-b9a8-a1b44a7a574c.png)

- 延遲問題
![](https://i.imgur.com/ee6Ovr2.gif)

![](https://i.imgur.com/SaAmiDY.gif)


## Literature Survey and Related Work

1. English lipread

- LIPNET: END-TO-END SENTENCE-LEVEL LIPREADING 
https://arxiv.org/pdf/1611.01599.pdf
- Hearing Lips: Improving Lip Reading by Distilling Speech Recognizers
https://arxiv.org/pdf/1911.11502v1.pdf
- LEARN AN EFFECTIVE LIP READING MODEL WITHOUT PAINS
https://arxiv.org/pdf/2011.07557.pdf
- Paper with code
https://paperswithcode.com/task/lipreading/codeless?page=2
https://github.com/rizkiarm/LipNet/blob/master/setup.py

2. Chinese lipread

- data set 
https://www.vipazoo.cn/CMLR.html
- VSR、LRW1000
https://arxiv.org/pdf/2003.03206v2.pdf
- Chinese lip reads model
https://github.com/Fengdalu/Lipreading-DenseNet3D
http://jos.org.cn/html/2020/6/5709.htm
https://arxiv.org/pdf/1908.04917v2.pdf
- A Cascade Sequence-to-Sequence Model for Chinese Mandarin Lip Reading
https://arxiv.org/pdf/1908.04917v2.pdf

3. Face recognition 
https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/







