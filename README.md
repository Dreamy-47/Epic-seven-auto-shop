# Epic-seven-auto-shop
自動刷商店腳本
這是基於個人喜好所做出來的
因此,若使用者被封概不負責
#### 原理
以防萬一，還是說明一下此code的原理
簡單來說就是將螢幕截圖->檢查有沒有與書籤相同的圖片->程式控制滑鼠按下按鈕來達成購買書籤->重複執行
### **注意 作者的螢幕是(1920*1080) 若不同者可能無法使用**

##### 下載檔案
cmd執行
```
git clone https://github.com/Dreamy-47/Epic-seven-auto-shop.git
```
或是右上角 code -> zip也行



### 安裝方法
安裝好python
cmd執行以下來安裝package
```
pip install -r requirement.txt
```
config.json用來設定以下
* 刷商店次數
* 顯示本次執行結果, 預設為true
* 是否於刷到10抽聖約時停止, 預設為false
## 執行
請於該資料夾打開cmd並執行

```
python auto_shop.py
```
兩秒內切換為e7完全視窗(如下),就能放給它跑了,要中斷就直接關掉cmd就好

![](https://i.imgur.com/wYteMSY.jpg)

由於是程式操控滑鼠鍵盤,視窗不能切換,建議睡前執行
