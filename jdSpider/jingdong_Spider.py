# coding=utf-8
import requests

r = requests.get('https://www.jd.com/')
text = r.text
UrlList = []

UrlStart = text.find('//')
while UrlStart is not -1 and UrlStart is not 0:
    print("下一个url的'//'在剩余文本的初始位置: ", UrlStart)
    UrlEnd = text.find('.com')
    if UrlEnd - UrlStart >= 30:
        print("+++++++++continue++++++++++")
        text = text[UrlEnd + 4 : ]
        continue
    NewUrl = 'http:' + text[UrlStart : UrlEnd] + '.com'
    print('found new url: ', NewUrl)
    UrlList.append(NewUrl);
    text = text[UrlEnd + 4 : ]
    UrlStart = text.find("//")

print(UrlList)