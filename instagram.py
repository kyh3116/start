#-*- coding: utf-8 -*-
import time
import datetime
import random
from selenium import webdriver
from urllib.parse import quote
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
import requests
import json

options = webdriver.ChromeOptions()
# Chrome을 안 띄우고 수행하고 싶으면 아래 주석을 해제합니다.(리눅스 서버에서 작업시 headless 추천합니다.)
# options.add_argument("headless")

# Chrome 설정 : 진짜 유저가 작업하는 것처럼 보이도록 설정합니다.
options.add_argument("window-size=1920x1080")
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 \
                      (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("lang=ko_KR")

# ======= 2. Setting id, password, hashtag ======
id = ''
password = ''
url = 'https://www.instagram.com/accounts/login/?source=auth_switcher'
timeline_like_count = 120

# hash_tags : 좋아요할 전체 해시태그 리스트
# important_hash_tags : 중요해서 더 많이 like할 해시태그 리스트
important_hash_tags = ['아기간식']
important_hash_tags_count = 120
hash_tags = ['아기간식', '다이어트식단', '건강식']
hash_tags_count = 60


# ======== 3. AutoInsta Class ======
class AutoInsta:
    @classmethod
    def run(cls, start_index=1, end_index=2):
        print('browser loading..')
        # display = Display(visible=0, size=(800,600))
        # display.start()
        #browser 전에 display 선언해주기 ubuntu는 가상의 display
        global browser
        browser = webdriver.Chrome('C:\\Users\\samsung\\python\\chromedriver', chrome_options=options)
        browser.get(url)

        start_text = "{id} Insta Auto Like Start : {time}".format(id=id, time=datetime.datetime.now())
        print(start_text)
        cls.login()
        for i in range(start_index, end_index):
            
            
            # cls.timeline_like()
            cls.hash_tags_like()
        end_text = "{id} Insta Auto Like End : {time}".format(id=id, time=datetime.datetime.now())
        print(end_text)

    @classmethod
    def login(cls):
        """
        인스타그램 메인에서 로그인하는 함수
        """
        
        
        username_input = browser.find_element_by_name('username')
        username_input.send_keys(id)
        time.sleep(2 + random.random() * 0.3)
        password_input = browser.find_element_by_name('password')
        password_input.send_keys(password)
        time.sleep(1)
        password_input.submit()
        time.sleep(5)
        print("login success")

    @classmethod
    def timeline_like(cls):
        """
        timeline_likg_count만큼 타임라인의 좋아요를 누름
        이 부분에 not clickable at point라고 error가 발생되고 있습니다. 추후 수정 필요
        """
        print('timeline like start')
        time.sleep(5)
        # browser.findelements_by_class_name("HoLwm")[0].click()

        dic = {}
        like_count = 10
        h = 1
        try:
            while like_count > 0:
                soup = BeautifulSoup(browser.page_source, 'html.parser')
                all_divs = soup.select(".c-Yi7")
                #select 는 아름다운수프에서 제공하는 건데, 조건과 일치하는 모든 객체들을 List로 반환해준다.
                print(len(all_divs))
                for i in range(len(all_divs)):
                    print(all_divs[i].get("href"))
                    if(dic.get(all_divs[i].get("href"))):
                        print("already is")
                    else:
                        print("already is not")
                        dic[all_divs[i].get("href")] = 1
                        browser.get("https://www.instagram.com"+all_divs[i].get("href"))
                        soup = BeautifulSoup(browser.page_source, 'html.parser')
                        islike = soup.select(".glyphsSpriteHeart__filled__24__red_5")
                        print(str(len(islike)) + " " + str(islike))
                        if(len(islike)>0):
                            continue
                        like_count -= 1
                        print(len(browser.find_elements_by_class_name("coreSpriteHeartOpen")))
                        element = browser.find_elements_by_class_name("coreSpriteHeartOpen")[0]
                        time.sleep(3)
                        wait = WebDriverWait(browser, 10)
                        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'coreSpriteHeartOpen')))
                        element.click()

                browser.get("https://www.instagram.com")

                for j in range(h+1):
                    time.sleep(3)
                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                h += 1

        except Exception as e:
            print("Error! ", e)
            pass

    @classmethod
    def hash_tags_like(cls):
        """
        hash_tags_like
        위에서 설정한 important_hash_tags와 hash_tags들을 각 횟수만큼 좋아요
        만약 컨텐츠가 중간에 삭제되거나 페이지가 없으면
        다음 해시태그로 이동되도록 예외처리
        """
        print('hash_tags like start')
        for hash_tag in hash_tags:
            try:
                print(hash_tag + " 좋아요 작업을 시작합니다")
                browser.get("https://www.instagram.com/explore/tags/" + quote(hash_tag))
                time.sleep(5 + random.random() * 1.2)
                element = browser.find_elements_by_css_selector("div._9AhH0")[9]
                element.click()
                time.sleep(5)

                if any(e in hash_tag for e in important_hash_tags):
                    count_number = important_hash_tags_count
                else:
                    count_number = hash_tags_count
## 셀레니움: 동적페이지를 제어,크롤링하고자 할때만 사용,단점: 브라우저를 직접 돌리기때문에 무거움
## beautifulsoup, requests: 일반적으로 크롤링 할때 사용
                for i in range(1, count_number):
                    try:
                        if browser.find_element_by_css_selector("span.fr66n > button > span").get_attribute('aria-label') == "좋아요":
                            time.sleep(1.2 + random.random() * 1.3)
                            browser.find_element_by_css_selector("span.fr66n > button").click()
                            time.sleep(1 + random.random() * 1.2)
                            time.sleep(1.2 + random.random() * 1.3)
                        else:
                            pass
                        time.sleep(1.2 + random.random() * 1.3)
                        browser.find_element_by_css_selector("a.HBoOv.coreSpriteRightPaginationArrow").click()
                        time.sleep(1 + random.random() * 1.2)
                    except NoSuchElementException as e:
                        print("NoSuch Error", e)
                        pass


            except Exception as e:
                print("Error! ", e)

if __name__ == '__main__':
    import instagram
    instagram.AutoInsta.run()


    ##ubuntu 에서 selenium 쓸 때 주의사항
    # -*- coding : utf-8 -*-
    # pip3 install (selenium이거 빼니까 됨) pyvirtualdisplay
    # 코드에서 상단부분에 from pyvirtualdisplay import Display
    
    # display = Display(visible=0, size=(800,600))
    # display.start()
    # browser 전에 display 선언해주기 ubuntu는 가상의 display
    # drive = webdriver.chrom() 