import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_winnipeg_gas():
    url = "https://www.gasbuddy.com/gasprices/manitoba/winnipeg"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 尋找油站同價錢 (注意：GasBuddy 嘅 class 名可能會變，以下為概念代碼)
        prices_elements = soup.find_all('span', class_='text__xl___2MzIB') 
        stations_elements = soup.find_all('h3', class_='header__header3___1b1iq')
        
        stations_data = []
        # 將攞到嘅資料放入一個 List
        for station, price in zip(stations_elements, prices_elements):
            stations_data.append({
                "name": station.text.strip(),
                "price": price.text.strip()
            })
        
        # 準備寫入 JSON 嘅資料
        output_data = {
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "stations": stations_data
        }
        
        # 儲存成 data.json
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)
            
        print("數據更新成功！")
        
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    get_winnipeg_gas()
