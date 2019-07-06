import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class details():
    def __init__(self):
        self.id = ""
        self.title = ""
        self.link = ""
        self.des = ""

'''Gives the Video link and Category and Webdriver as input
And it return the Video Details like Video Id, Title, Description and Also add the category'''
def get_video_details(u_link,v_category,driver):
    dataframe = pd.DataFrame(columns = ['link','title', 'description', 'category'])
    wait_driver = WebDriverWait(driver, 10)
    for i in u_link:
        driver.get(i)
        new_user = details()

        new_user.id = i.strip(r'https://www.youtube.com/watch?v=')
        new_user.title = wait_driver.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
        new_user.des = wait_driver.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,'div#description yt-formatted-string' 
        ))).text
        dataframe.loc[len(dataframe)] = [new_user.id, new_user.title, new_user.des, v_category]
    return dataframe
