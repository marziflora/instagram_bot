#!/usr/bin/env python
# coding: utf-8

# In[191]:


import instaloader
L = instaloader.Instaloader()

L.login("marzenakwasnicka.fotografia", password)
# Obtain profile metadata
profile = instaloader.Profile.from_username(L.context, "marzenakwasnicka.fotografia")

# Print list of followees
follow_list = []
count=0
for followee in profile.get_followers():
    follow_list.append(followee.username)
    
file = open("marzenafotografia_followers.txt","w")
file.write(" \n".join(follow_list))
file.close()


# In[249]:


from selenium import webdriver
import time
import numpy as np
from random import seed, randint
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import pandas as pd
import re
import random

hasztags = ['portretkobiety', "portraits", "portraitsfromwroclaw", "sesjazdjeciowawroclaw", 'wroclawgirl', 'dolnyslask', 'wroclaw', 'wrocław','polskakobieta', 'fotografwroclaw', 'kobieta', 'sesjazdjeciowa']
driver = webdriver.Chrome("C:/Users/mkwasnicka/Downloads/chromedriver_win32/chromedriver.exe")
follow_list = [i.strip() for i in open("marzenafotografia_followers.txt","r").read().splitlines()]
users_omit = [f'https://www.instagram.com/{i}/' for i in follow_list]
users_omit.append('https://www.instagram.com/marzenakwasnicka.fotografia/')

def InstaBot_login(username, password, driver):
    driver.get("https://instagram.com")      
    time.sleep(randint(3, 5))
    driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(username)
    time.sleep(randint(1, 2))
    driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(password)
    while driver.find_element_by_xpath("//button[contains(text(), 'Akceptuję')]") == []:
        time.sleep(randint(3, 5))   
    driver.find_element_by_xpath("//button[contains(text(), 'Akceptuję')]").click()
    while driver.find_element_by_xpath('//button[@type="submit"]') == []:
        time.sleep(randint(3, 5))
    driver.find_element_by_xpath('//button[@type="submit"]').click()
    time.sleep(randint(3, 5))

def go_to_hasztag(driver, df, df2):
    hasztag_link = 'https://www.instagram.com/explore/tags/'+hasztags[randint(0,len(hasztags)-1)]
    print(hasztag_link)
    driver.get(hasztag_link) 
    #pick random photo, not from 'most popular' page
    time.sleep(randint(3, 5))  
    if len(driver.find_elements_by_xpath("//div[contains(@class, '_9AhH0')]"))>13:
        driver.find_elements_by_xpath("//div[contains(@class, '_9AhH0')]")[randint(13, len(driver.find_elements_by_xpath("//div[contains(@class, '_9AhH0')]"))-1)].click()
        time.sleep(randint(5, 8))    
        driver.find_elements_by_xpath("//div[contains(@class, 'QBdPU ')]")[-4].click() #like it
        #Go to profiles that liked that photo
        time.sleep(randint(3,4))
        try:
            driver.find_element_by_class_name('zV_Nj').click() #who like it?
        except:
            pass
        else:
            time.sleep(randint(3,4))
            elems = driver.find_elements_by_css_selector("[href]")
            links = [elem.get_attribute('href') for elem in elems]
            profiles = np.unique([i for i in links if re.search(r'^https://www.instagram.com/([\w.]*)(/$)',i) and i!='https://www.instagram.com/explore/' and i!='https://www.instagram.com/developer/'], axis=0).tolist()  
            new_tags = [i.split("/")[-2] for i in np.unique([i for i in links if re.search(r'^https://www.instagram.com/explore/tags/([\w.]*)(/$)',i)], axis=0).tolist()]
            if len(profiles)>1:
                selected_profiles = random.sample(profiles, min(10, len(profiles)))
                df = pd.read_csv("like.csv", sep=';')
                for i in selected_profiles:
                    if i not in users_omit and i not in df.profil.values.tolist(): #omit special users and already liked user:
                        driver.get(i)   #go to its page
                        time.sleep(randint(3,5))
                        photos = len(driver.find_elements_by_xpath("//div[contains(@class, '_9AhH0')]"))
                        if photos>0:
                            how_much_like = min(int(photos*0.8), randint(1, 6))
                            which_to_like = random.sample(list(range(min(photos,13))), how_much_like)
                            print(i, which_to_like)
                            for j in which_to_like: 
                                driver.find_elements_by_xpath("//div[contains(@class, '_9AhH0')]")[j].click() #click on photo
                                time.sleep(randint(3,5))
                                driver.find_elements_by_xpath("//div[contains(@class, 'QBdPU ')]")[-4].click() #like its photo
                                time.sleep(randint(1,3))
                                webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform() #return to last page
                                time.sleep(randint(2,3))
                            df = pd.read_csv("like.csv", sep=';')
                            df = df.append(pd.DataFrame([[i.split("/")[-2],str(which_to_like)]], columns=['profil', 'zdjecia']))
                            df.to_csv("like.csv", index=False,  sep=';')
                            f = open("hasztag.txt", 'r+')
                            read = f.read()
                            f = open("hasztag.txt", 'w+')
                            x = set(read.split(" "))
                            x = "\n".join(x) + "\n".join(set(new_tags))
                            f.write(x)
                            f.close()
        
password = open('instagrampassword.txt').read()
InstaBot_login("marzenakwasnicka.fotografia", password, driver)
while True:
    for i in range(0,5):
        go_to_hasztag(driver, df, df2)
        time.sleep(randint(3, 6))
    time.sleep(randint(10, 60))
    go_to_hasztag(driver,df, df2)


# In[ ]:





# In[ ]:




