import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from pathlib import Path
import time
import urllib.request

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--ignore-certificate-errors')

i = 1
file = open("list.txt", 'r', encoding='utf-8')
keyWords = file.readlines()
#keyWord = ""
#folder = ""
file.close()
imageAmount = int(keyWords[0])
while i < len(keyWords):
    keyWord = keyWords[i].replace("\n", "")
    directory = "./data/" + keyWord + "/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    print('[Info] crawling "' + keyWord + '" images')

    driver = webdriver.Chrome()
    driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")
    elem = driver.find_element_by_name("q")
    elem.send_keys(keyWord)
    time.sleep(2)
    elem.send_keys(Keys.RETURN)

    SCROLL_PAUSE_TIME = 1
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(2)
    
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                driver.find_element_by_css_selector(".mye4qd").click()
            except:
                break
        last_height = new_height
    

    images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
    count = 1
    for image in images:
        try:
            # image click
            image.click()
            time.sleep(2)
            # image url copy
            imgUrl = driver.find_element_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img").get_attribute("src")
            opener=urllib.request.build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            urllib.request.install_opener(opener)
            #image save
            urllib.request.urlretrieve(imgUrl, directory + keyWord + str(count) + ".jpg")
            print("[Info] picture(" + keyWord + str(count) + ".jpg) saved")
            if count >= imageAmount:
                break
            else:
                count = count + 1
        except:
            pass
    driver.close()
    i += 1