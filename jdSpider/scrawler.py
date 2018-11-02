# coding=utf-8
import requests as rq
import random
import time
from bs4 import BeautifulSoup

# get other url from this
def getURLsFromGoodsText(goodsText):
    urlList = []
    urlStartIndex = goodsText.find("//")
    while urlStartIndex > 0:
        goodsText = goodsText[urlStartIndex:]
        urlEndIndex = goodsText.find(".html")

        if urlEndIndex < 0:
            return urlList
        if urlEndIndex > 60:
            goodsText = goodsText[urlEndIndex:]
            urlStartIndex = goodsText.find("//")
            continue
        urlLength = urlEndIndex + 5
        charNext = goodsText[urlLength]
        if charNext == "'" or charNext == "\"" or charNext == "?":
            newURL = "https:" + goodsText[:urlLength]
            urlList.append(newURL)

        goodsText = goodsText[urlLength:]
        urlStartIndex = goodsText.find("//")
    return urlList

# get url source code
def doRequestToURL(url):
    try:
        r = rq.get(url,
               headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'})
    except FileNotFoundError:
        print("can't connect network!")
    r.encoding = r.apparent_encoding
    goodsText = r.text
    return goodsText

def getHostName(url):
    splitUrl = url.split('/')
    return "".join(splitUrl[0] + "//" + splitUrl[2] + "/")

# Analyzing goods Page and fetch goods
def analyzingGoodsPage(goodsText, targetUrl, count):
    print("Analyzing targetUrl....")
    soup = BeautifulSoup(goodsText, 'lxml')
    print(soup.findAll(name='meta', attrs={"name": "keywords"}))
    if soup.findAll(name='meta', attrs={"name": "keywords"}):
        good_Id = targetUrl.split('/')[3].split('.')[0]
        good_Name = soup.findAll(name='meta', attrs={"name": "keywords"})[0].attrs['content']
        pduid = 1540968060261294252031
        pduid += 1
        priceUrl = "https://p.3.cn/prices/mgets?pduid=" + str(pduid) + "&skuIds=J_" + str(good_Id)
        priceInfo = doRequestToURL(priceUrl)
        good_Price = priceInfo.split(":")[1].split(",")[0]
        with open(resultPath + fileName, "a") as goodInfo:
            goodInfo.write("*****************No." + str(count) + "******************\n")
            goodInfo.write("goodId: " + str(good_Id) + "\nname: " +
                           good_Name + "\npriceInfo: " + priceInfo + "price: " + good_Price + "\n")
    else:
        count -= 1
        print("this page is useless.")
        uselessPageURLs.append(targetUrl)

def RunSpider(totalUrlList, goodsPageURLs, uselessPageURLs):
    count = 0
    for targetUrl in totalUrlList:
        print("start in " + targetUrl, end="")
        goodsText = doRequestToURL(targetUrl)
        newUrls = getURLsFromGoodsText(goodsText)
        print(" find " + str(len(newUrls)) + " urls in this url")

        urlHostName = getHostName(targetUrl)
        if urlHostName in goodsPageURLs:
            count = count + 1
            analyzingGoodsPage(goodsText, targetUrl, count)

        for newUrl in newUrls:
            newUrlsHostName = getHostName(newUrl)
            if newUrlsHostName not in uselessPageURLs and newUrl not in totalUrlList:
                totalUrlList.append(newUrl)
        time.sleep((random.uniform(1, 3)))

firstPageURL = "https://item.jd.com/10058164.html"
# firstPageURL = "https://item.jd.com/1470067627.html"  // it's a bad url for test
goodsPageURLs = ["https://item.jd.com/", "https://item.jd.hk/"]
uselessPageURLs = ["https://channel.jd.com/", "https://www.jd.com/", "https://help.jd.com/"]
totalUrlList = [firstPageURL]
resultPath = "/home/user/Desk/Spider/"
fileName = "goodsInfo.txt"

print('Spider running...')
print("====================================")
with open(resultPath + fileName, "w") as f:
    f.write("************** jd goods Spider ******************" + "\n\n")
RunSpider(totalUrlList, goodsPageURLs, uselessPageURLs)
