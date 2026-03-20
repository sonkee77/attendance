"""
출퇴근 자동화 스크립트 (GitHub Actions용)
사용: python attendance.py checkin
      python attendance.py checkout
"""
import sys
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# GitHub Secrets에서 환경변수로 받음
USER_ID = os.environ['ATTEND_ID']
USER_PW = os.environ['ATTEND_PW']
URL     = "https://gw.catenoid.net/gw/uat/uia/egovLoginUsr.do"


def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1024,800')
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def login(driver):
    driver.implicitly_wait(3)
    driver.get(URL)
    driver.find_element(By.XPATH, '//*[@id="userId"]').send_keys(USER_ID)
    driver.find_element(By.XPATH, '//*[@id="userPw"]').send_keys(USER_PW)
    driver.find_element(By.XPATH,
        '/html/body/div[1]/div[2]/div[2]/span[1]/form/fieldset/div[2]/a').click()
    driver.implicitly_wait(3)
    print("로그인 완료")


def checkin():
    driver = get_driver()
    try:
        login(driver)
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="inBtn"]').click()
        time.sleep(1)
        driver.find_element(By.XPATH,
            '/html/body/div[9]/div[1]/div[3]/div[1]/input').click()
        time.sleep(1)
        driver.find_element(By.XPATH,
            '/html/body/div[9]/div[1]/div[2]/div/input').click()
        time.sleep(2)
        print("✅ 출근 완료")
    finally:
        driver.quit()


def checkout():
    driver = get_driver()
    try:
        login(driver)
        time.sleep(2)
        driver.find_element(By.XPATH,
            '/html/body/div[4]/div[1]/div/div[6]/div/div/div[2]/div/ul/li[2]').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//*[@id="outBtn"]').click()
        time.sleep(1)
        driver.find_element(By.XPATH,
            '/html/body/div[9]/div[1]/div[3]/div[1]/input').click()
        time.sleep(2)
        print("✅ 퇴근 완료")
    finally:
        driver.quit()


if __name__ == '__main__':
    action = sys.argv[1] if len(sys.argv) > 1 else ''
    if action == 'checkin':
        checkin()
    elif action == 'checkout':
        checkout()
    else:
        print("사용법: python attendance.py checkin|checkout")
        sys.exit(1)
