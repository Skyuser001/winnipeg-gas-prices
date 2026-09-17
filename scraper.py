import requests
import re

def test_chrisd():
    url = "https://www.chrisd.ca/winnipeg-gas-prices/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        # 去 ChrisD.ca 攞網頁原始碼
        response = requests.get(url, headers=headers)
        print(f"連線狀態: {response.status_code} (200 代表成功入到網站)")
        
        # 用正則表達式，嘗試喺幾萬行代碼入面，搜尋類似「157.9」嘅溫尼伯常見油價數字
        prices = re.findall(r'1[4-9]\d\.\d', response.text)
        
        if prices:
            print(f"🎉 恭喜！網頁原始碼入面真係有油價數字！")
            print(f"搵到嘅部分數字：{prices[:10]}")
            print("結論：我哋絕對可以寫程式喺呢度攞資料！")
        else:
            print("❌ 原始碼入面完全搵唔到油價數字...")
            print("結論：ChrisD.ca 係用咗動態載入。簡單爬蟲睇唔到背後嘅 GasBuddy 數據。")
            
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    test_chrisd()
