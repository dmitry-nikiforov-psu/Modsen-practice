import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


chrome_driver_path = 'C:/modsen/chromedriver/chromedriver.exe'


chrome_options = Options()
chrome_options.add_argument("--headless")

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:

    driver.get('https://www.codewars.com/users/dmitry-nikiforov-psu/completed')


    driver.execute_script("window.localStorage.setItem('myKey', 'myValue');")


    value = driver.execute_script("return window.localStorage.getItem('myKey');")
    print(f"Value from LocalStorage: {value}")


    driver.execute_script("window.localStorage.removeItem('myKey');")


    value = driver.execute_script("return window.localStorage.getItem('myKey');")
    print(f"Value after removal: {value}")

finally:

    driver.quit()
