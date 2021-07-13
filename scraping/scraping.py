import csv
import requests
import bs4
 
RACE_ID = "202005021211"
CSV_DIR = "./csv/"
URL_BASE = "https://db.netkeiba.com/race/"
 
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36   '
}
 
# htmlソース取得
def get_text_from_page(url):
     
    try:
        res = requests.get(url, headers=HEADERS)
        res.encoding = res.apparent_encoding  
        text = res.text
         
        return text
    except:
        return None
     
# info取得
def get_info_from_text(header_flg, text):
     
    try:  
         
        # データ
        info = []
        soup = bs4.BeautifulSoup(text, features='lxml')
         
        # レース結果表示用のtable
        base_elem = soup.find(class_="race_table_01 nk_tb_common")
         
        # 行取得
        elems = base_elem.find_all("tr")
         
        for elem in elems:
             
            row_info = []
             
            # ヘッダーを除外するための情報
            r_class = elem.get("class")
            r_cols = None
             
            if r_class==None:
                # 列取得
                r_cols = elem.find_all("td")
                 
            else:
                # ヘッダー(先頭行)
                if header_flg:
                    r_cols = elem.find_all("th")
             
            if not r_cols==None:
                 
                for r_col in r_cols:
                    tmp_text = r_col.text
                    tmp_text = tmp_text.replace("\n", "")
                    row_info.append(tmp_text.strip())
                     
                info.append(row_info)
         
        return info
    except:
        print("err")
        return None
     
if __name__ == '__main__':
     
    url = URL_BASE + RACE_ID
     
    text = get_text_from_page(url)
     
    info = get_info_from_text(False, text)
     
    # csvファイル
    file_path = CSV_DIR + RACE_ID + ".csv"
     
    with open(file_path, "w", encoding='utf8', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(info)