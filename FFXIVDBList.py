from time import sleep
import browser as b
import sys
import urllib.parse
import csvDriver as csv

def action(url:str, pearent:str, d:int=0):
    d+=1
    if b.jumpURL(url):
        # アイテムタイプ読み取り
        iType = b.getXPathText('//*[@id="breadcrumb"]/ul/li[4]',False)
        if iType == '製作手帳':
            # クラフター読み取り
            crafter = b.getXPathText(f'//*[@id="eorzea_db"]/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/p')
            # テーブル要素数
            n = len(b.getXPathArray('//*[@id="eorzea_db"]/div[2]/div[2]/div/div[1]/div[3]/div[3]/div/div',False))
            for i in range(n):
                if b.getXPath(f'//*[@id="eorzea_db"]/div[2]/div[2]/div/div[1]/div[3]/div[3]/div/div[{i+1}]/div[3]/div/div[1]/div/p/a',False) != None:
                    # 製作の時 -> ツリー深化
                    # 表示
                    itemName = b.getXPathAttribute(f'//*[@id="eorzea_db"]/div[2]/div[2]/div/div[1]/div[3]/div[3]/div/div[{i+1}]','data-name')
                    itemNum = b.getXPathAttribute(f'//*[@id="eorzea_db"]/div[2]/div[2]/div/div[1]/div[3]/div[3]/div/div[{i+1}]','data-num')
                    # リンク
                    b.getXPathText(f'/html/body/div[3]/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[3]/div/div[{i+1}]/div[3]/div/div[1]/div/p/a')
                    nextURL = b.getXPathAttribute(f'/html/body/div[3]/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[3]/div[3]/div/div[{i+1}]/div[3]/div/div[1]/div/p/a','href')
                    csv.fileAppend(sys.argv[1], f'{pearent},{itemName},{itemNum},{crafter}',False)
                    action(nextURL, itemName, d)
                else:
                    # 製作ではない -> 名前・個数を記録
                    itemName = b.getXPathAttribute(f'//*[@id="eorzea_db"]/div[2]/div[2]/div/div[1]/div[3]/div[3]/div/div[{i+1}]','data-name')
                    itemNum = b.getXPathAttribute(f'//*[@id="eorzea_db"]/div[2]/div[2]/div/div[1]/div[3]/div[3]/div/div[{i+1}]','data-num')
                    nextURL = b.getXPathAttribute(f'//*[@id="eorzea_db"]/div[2]/div[2]/div/div[1]/div[3]/div[3]/div/div[{i+1}]/div[2]/div/a','href')
                    csv.fileAppend(sys.argv[1], f'{pearent},{itemName},{itemNum},{crafter}',False)
                    action(nextURL, itemName, d)
        elif iType == 'アイテム':
            crafter = b.getXPathText('//*[@id="eorzea_db"]/div[2]/div[2]/div[1]/div[1]/div[2]/div/p')
            csv.fileAppend(sys.argv[1], f'{pearent},末端,0,{crafter}',False)
        elif iType == '採集手帳':
            pass
        else:
            print(f'iType:{iType} type:{type(iType)}')
            pass
        b.back()

# main
if not b.headlessSetup('./chromedriver', headless=True, visible=False):
    exit()

for l in range(2,len(sys.argv)):
    line = sys.argv[l]
    # エオルゼアデータベース
    b.jumpURL(f'https://jp.finalfantasyxiv.com/lodestone/playguide/db/recipe/?patch=&db_search_category=recipe&category2=&item_ui_category=&min_craft_lv=&max_craft_lv=&min_item_lv=&max_item_lv=&q={urllib.parse.quote(line)}')
    for i in range(len(b.getXPathArray('//*[@id="character"]/tbody/tr'))):
        itemName = b.getXPathText(f'//*[@id="character"]/tbody/tr[{i+1}]/td[1]/div[2]/a')
        print(itemName)
        crafter = b.getXPathText(f'//*[@id="character"]/tbody/tr[{i+1}]/td[1]/div[2]/span/a')
        action(b.getXPathAttribute(f'//*[@id="character"]/tbody/tr[{i+1}]/td[1]/div[2]/a','href'), itemName)

b.browserQuit()