from urllib import parse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
import time
import requests
import os

def down_load_paper(title, url):
    response = requests.get(url, stream=True)
    #title = "./output/paper/" + title
    # 检查响应状态码是否为200，表示请求成功
    time.sleep(5)
    if response.status_code == 200:
        # 以二进制写入模式打开文件
        with open("./output/paper/" + title, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
            print('PDF 文件已下载到本地')
    else:
        print('请求失败')


def paperUrl(name):
    q = name
    params = {
        'q':q
    }
    params = parse.urlencode(params)
    url = "https://scholar.google.com/scholar?" + params
    return url


def getBib(url):
    options = Options()
    options.add_argument('-headless')
    desired_capabilities = DesiredCapabilities.FIREFOX
    desired_capabilities["pageLoadStrategy"] = "none"
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    time.sleep(5)
    driver.find_element(By.CLASS_NAME, 'gs_or_cit.gs_nph').click()
    time.sleep(5)
    pdf_url = ""
    # check for pdf 
    for link in driver.find_elements(By.XPATH, "//*[@href]"):
        len_href = len(link.get_attribute('href'))
        if link.text.find("PDF") != -1:
            print("success")
            pdf_url = link.get_attribute('href')
            print(link.get_attribute('href'))
            break
       # if link.get_attribute('href').lower().find("pdf") != -1:
       #     print(link.text)
       #     print(link.find_element(By.CLASS_NAME, "gs_ctg2").text)
       #     print(link.find_element(By.CLASS_NAME, "gs_ctg2").text == "[PDF]")
       #     pdf_url = link.get_attribute('href')
       #     print(link.get_attribute('href'))
       #     break

    # search for document
    if pdf_url == "":
        for link in driver.find_elements(By.XPATH, "//*[@href]"):
            len_href = len(link.get_attribute('href'))
            if link.get_attribute('href').lower().find("document") != -1:
                pdf_url = link.get_attribute('href')
                print(link.get_attribute('href'))
                break
    s = driver.find_element(By.CLASS_NAME, 'gs_citi')
    if s.text == 'BibTeX':
        hr = s.get_attribute('href')
    driver.get(hr)
    bib = driver.find_element(By.XPATH, "//*").text
    driver.quit()
    return bib, pdf_url


def down_reference(q):

    url = paperUrl(q)
    bib, pdf_url = getBib(url)
    title = ""
    cur = 0
    while cur + 4 < len(bib):
        if (bib[cur: cur + 5].lower() == "title"):
            head = cur
            while bib[head] != "{":
                head += 1
            tail = head + 1
            while bib[tail] != "}":
                tail += 1
            title = bib[head + 1: tail]
            break
        cur += 1
    down_load_paper(title + ".pdf", pdf_url)
    return bib