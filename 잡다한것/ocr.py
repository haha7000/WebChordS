from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import urllib.request
import time

# 검색어 입력
keyword = "강아지"

# 이미지 저장 폴더 생성
try:
    if not os.path.exists(keyword):
        os.makedirs(keyword)
except OSError:
    print(f"{keyword} 폴더 생성 실패")
    exit()

# 크롬 드라이버 실행
driver = webdriver.Chrome()

# 구글 이미지 검색 이동
driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")

# 검색어 입력 및 엔터키 누르기
search_box = driver.find_element_by_name("q")
search_box.send_keys(keyword)
search_box.send_keys(Keys.ENTER)

# 이미지 개수 설정 (최대 300장)
image_count = 300

# 이미지 로딩 완료까지 대기
last_height = driver.execute_script("return window.pageYOffset")
while True:
    new_height = driver.execute_script("return window.pageYOffset")
    if last_height == new_height:
        break
    last_height = new_height
    time.sleep(1)

# 이미지 추출 및 다운로드
images = driver.find_elements_by_css_selector(".Q4LuWd")

for i, image in enumerate(images[:image_count]):
    image_url = image.get_attribute("src")
    try:
        urllib.request.urlretrieve(image_url, f"{keyword}/{i+1}.jpg")
        print(f"{i+1}번째 이미지 다운로드 완료: {image_url}")
    except Exception as e:
        print(f"{i+1}번째 이미지 다운로드 실패: {e}")

# 크롬 드라이버 종료
driver.quit()
