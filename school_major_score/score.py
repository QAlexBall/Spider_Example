import re
import time
import json
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
import warnings 
warnings.filterwarnings('ignore')

def get_response(url):
    session = requests.session()
    body = requests.get(url, timeout=5)
    body.encoding = body.apparent_encoding
    text = body.text

def get_detail(url, f, id):
    print('downloading...', url)
    try:
        driver = webdriver.PhantomJS()
        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        driver.get(url)
    except:
        print('can not connect url!')

    result = dict()
    result['id'] = id
    time.sleep(random.randint(1, 2))
    try:
        result['province'] = driver.find_element_by_xpath("//span[@class='line-value td2']").text
        result['school_name'] = driver.find_element_by_xpath("//span[@class='line1-schoolName']").text
        result['marjors'] = list()
        print(result)
    except:
        print("school not exist!")
    
    # for next page score
    try:
        pages_text = driver.find_element_by_xpath("//div[@class='fypages']/ul").text
        pages = re.findall('\d', pages_text)
    
        for page in range(len(pages)):
            print("get page ", page + 1)
            score_xpath = "//tbody"
            page_xpath = "//div[@class='fypages']/ul/li[" + str(page + 3) + "]"
            next_page_path = driver.find_element_by_xpath(page_xpath)
            next_page_path.click()
            time.sleep(1)
            score = driver.find_element_by_xpath(score_xpath).text
        
            majors = score.split('\n')
            for major in majors:
                major_res = dict()
                major_split = major.split(' ')
                major_res['major'] = major_split[0]
                major_res['score_1'] = major_split[1]
                major_res['score_2'] = major_split[2]
                major_res['score_3'] = major_split[3]
                major_res['arrange'] = major_split[4]
                major_res['section'] = major_split[5]
                result['marjors'].append(major_res)
                print(major_res)
    except:
        print("major not exist!")
    driver.quit()
    json.dump(result, f, indent=4, ensure_ascii=False)

def write_detail(html, name):
    print('write to ./score/' + name)
    f = open('./score/' + name, 'w')
    f.write(html)
    f.close()
    soup = BeautifulSoup(html, 'lxml')
    print(soup.findAll(name='span', attrs={"class":"line-value td2"}))
    print(soup.find_all(name='span', attrs={'class':'line1-schoolName'}))
    print(soup.find_all(name='tr'))

def anaylize():
    html = open('./score/114.html', 'r', encoding='utf-8')
    soup = BeautifulSoup(html.read(), 'lxml')
    print(soup.findAll(name='span', attrs={"class":"line1-schoolName"}))
    print(soup.findAll(name='span', attrs={"class":"line-value td2"}))
    print(soup.findAll(name='td'))
    html.close()


def start():

    f = open('./result.json', 'a')
    for i in range(782, 4000):
        print("in " + str(i))
        url =  'https://gkcx.eol.cn/school/' + str(i) + '/specialtyline?cid=0'
        html = get_detail(url, f, i)
    f.close()

        #  if html != False:
            #  write_detail(html, str(i) + '.html')
        #  if i % 10 == 0:
            #  sleep_time = random.randint(1, 30)
            #  print('sleep ' +  str(sleep_time) + ' second! \n')
            #  time.sleep(sleep_time)

start()
#  anaylize()
'''
url =  'https://gkcx.eol.cn/school/1364/specialtyline?cid=0'
html = get_detail(url)
write_detail(html)
anaylize(html)
print('ok')
'''
