import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def get_winnipeg_gas():
    url = "https://www.gasbuddy.com/gasprices/manitoba/winnipeg"
    # 升級 1：加入更多 Header 偽裝成真人瀏覽器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 升級 2：檢查係咪被網站當成機器人阻擋
        page_title = soup.title.string if soup.title else "無標題"
        print(f"網站標題: {page_title}")
        if "Access Denied" in page_title or "Just a moment" in page_title or "Security" in page_title:
            print("❌ 錯誤：GitHub 伺服器被網站嘅防機器人系統 (Cloudflare/Datadome) 阻擋了！")
        
        stations_data = []
        
        # 升級 3：唔再依賴經常變嘅 class，改用網頁結構同正則表達式 (Regex) 搵數字
        for h3 in soup.find_all('h3'):
            station_name = h3.text.strip()
            if not station_name: 
                continue
                
            # 喺 <h3> 附近尋找包含數字及小數點嘅字眼 (例如 "157.9")
            parent = h3.find_parent('div')
            if parent:
                # 尋找類似油價格式嘅字，例如 157.9
                price_element = parent.find(string=re.compile(r'\d{2,3}\.\d'))
                if price_element:
                    price = re.search(r'\d{2,3}\.\d', price_element).group()
                    stations_data.append({
                        "name": station_name,
                        "price": price
                    })
        
        # 移除重複嘅油站
        unique_stations = []
        seen = set()
        for s in stations_data:
            if s['name'] not in seen:
                seen.add(s['name'])
                unique_stations.append(s)

        output_data = {
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "stations": unique_stations
        }
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)
            
        print(f"✅ 成功提取 {len(unique_stations)} 間油站數據！")
        
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    get_winnipeg_gas()
