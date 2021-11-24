import sys
import os
from selenium import webdriver
import pandas
import time

#スクレイピング最大ページ数
max_page = 3


#Googleにアクセスして、タイトルをとってこれるかテスト
browser = webdriver.Chrome(executable_path=r"C:\tools\chromedriver.exe")

args = sys.argv
df = pandas.read_csv('default.csv', index_col=0)

#引数を取得
#取得したいキーワードを引数設定
if len(args) == 1:
    #ダミー
    query = "p30 lite 本体 simフリー"
else:
    query = args[1]

browser.get("https://www.mercari.com/jp/search/?sort_order=price_desc&keyword={}&category_root=&brand_name=&brand_id=&size_group=&price_min=&price_max=".format(query))

#レンダリング待ち
time.sleep(3)

#「新しいメルカリへ」ポップアップが表示されていたら閉じる
if len(browser.find_elements_by_css_selector("mer-button.mer-spacing-b-24 button")) > 0:
    print("ポップアップがあるためClose")
    browser.find_elements_by_css_selector("mer-button.mer-spacing-b-24 button")[0].click()


page = 1
while True: #continue until getting the last page

    print("######################page: {} ########################".format(page))
    print("Starting to get posts...")

    # 商品リスト取得
    posts = browser.find_elements_by_css_selector(".ItemGrid__ItemGridCell-sc-14pfel3-1")

    
    #アイテムごとにループ
    for post in posts:

        info_tag = post.find_element_by_css_selector("mer-item-thumbnail")

        title = info_tag.get_attribute("item-name")

        price = info_tag.get_attribute("price")
        price = price.replace('¥', '')

        #売り切れ判定
        sold = "売切" if info_tag.get_attribute("sticker-label") == "売り切れ" else "あり"

        url = post.find_element_by_css_selector(".ItemGrid__StyledThumbnailLink-sc-14pfel3-2").get_attribute("href")
        se = pandas.Series([title, price, sold,url],['title','price','sold','url'])
        df = df.append(se, ignore_index=True)


    #処理最大ページ数判定
    if max_page == page:
        print("its max page!!")
        break


    #ページ移動
    page_area = browser.find_elements_by_css_selector(".Pagination__PaginationControlsContainer-sc-17at9ov-0")
    if len(page_area) > 0:
        page+=1

        if len(page_area[0].find_elements_by_css_selector("mer-button")) > 1 :
            page_area[0].find_elements_by_css_selector("mer-button")[1].click()
        else:
            page_area[0].find_elements_by_css_selector("mer-button")[0].click()

        print("Moving to next page......")
        
        #レンダリング待ち
        time.sleep(3)

    else:
        print("no pager exist anymore")
        break
#6
df.to_csv("{}.csv".format(query))
print("DONE")