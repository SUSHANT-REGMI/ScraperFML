from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import json

with open('content.json') as f:
    data = json.load(f)

for keys, values in data['tags'].items():

        os.mkdir("C:\\Users\\susha\\OneDrive\\Desktop\\Automation Project\\Content Images\\"+keys+" Images\\")
        for value in values:
            os.environ['PATH'] += r"C:/Users/susha/OneDrive/Desktop/Automation Project"

            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome(options=options)

            driver.get('https://www.google.ca/imghp?hl=en&tab=ri&authuser=0&ogbl')
            # *[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img
            my_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
            my_element.send_keys(value)
            my_element.send_keys(Keys.ENTER)
            xpath = '//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img'
            last_height = driver.execute_script('return document.body.scrollHeight')

            for i in range(1,3):
                sc_content = "C:\\Users\\susha\\OneDrive\\Desktop\\Automation Project\\Content Images\\"+keys+" Images\\"+value+" ("+ str(i)+ ").png"
                driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div['+str(i)+']/a[1]/div[1]/img').screenshot(sc_content)
            












