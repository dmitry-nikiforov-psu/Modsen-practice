from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


chrome_driver_path = 'C:/modsen/chromedriver/chromedriver.exe'


chrome_options = Options()
chrome_options.add_argument("--headless")


service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:

    driver.get('https://www.codewars.com/users/dmitry-nikiforov-psu/completed')


    driver.add_cookie({'name': 'myCookie', 'value': 'myValue'})


    cookie = driver.get_cookie('myCookie')
    print(f"Value from Cookie: {cookie['value']}")


    driver.delete_cookie('myCookie')


    cookie = driver.get_cookie('myCookie')
    print(f"Value after removal: {cookie}")

finally:

    driver.quit()
