#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
import time
import numpy as np
from random import seed, randint
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

hasztags = ["portraits", "portraitsfromwroclaw", "sesjazdjeciowawroclaw", 'wroclawgirl', 'dolnyslask', 'wroclaw', 'wrocław','polskichlopak', 'fotografwroclaw']
driver = webdriver.Chrome("C:/Users/mkwasnicka/Downloads/chromedriver_win32/chromedriver.exe")
users_omit = ['']

def save(x):
    f = open('photos.txt', 'a')
    f.write(x)
    f.write("\n")
    f.close()

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
#     while driver.find_element_by_xpath("//button[contains(text(), 'Nie teraz')]") == []:
#         time.sleep(sleeptime+1)
#     driver.find_element_by_xpath("//button[contains(text(), 'Nie teraz')]").click()
        
def go_to_hasztag(driver):
    hasztag_link = 'https://www.instagram.com/explore/tags/'+hasztags[randint(0,len(hasztags)-1)]
    print(hasztag_link)
    driver.get(hasztag_link) 
    #pick random photo, not from 'most popular' page
    time.sleep(randint(3, 5))  
    driver.find_elements_by_xpath("//div[contains(@class, '_9AhH0')]")[randint(9, len(driver.find_elements_by_xpath("//div[contains(@class, '_9AhH0')]"))-1)].click()
    time.sleep(randint(5, 8))    
    driver.find_elements_by_xpath("//div[contains(@class, 'QBdPU ')]")[-4].click() #like it
    #Go to profiles that liked that photo
    time.sleep(randint(3,3))
    try:
        driver.find_element_by_class_name('zV_Nj').click() 
        time.sleep(randint(3,4))
        elems = driver.find_elements_by_css_selector("[href]")
        links = [elem.get_attribute('href') for elem in elems]
        profiles = np.unique([i for i in links if re.search(r'^https://www.instagram.com/([\w.]*)(/$)',i) and i!='https://www.instagram.com/explore/' and i!='https://www.instagram.com/developer/' and i!='https://www.instagram.com/marzenakwasnicka.fotografia/'], axis=0).tolist()                  
        go_to_likers(driver, profiles)
    except:
        pass
        
def go_to_likers(driver, profiles):
    if len(profiles)>1:
        profiles = random.sample(profiles, min(10, len(profiles)))
        print(profiles)
        for i in profiles:
            driver.get(i)   #go to its page
            time.sleep(randint(3,5))
            photos = len(driver.find_elements_by_xpath("//div[contains(@class, '_9AhH0')]"))
            if photos>1:
                how_much_like = min(int(photos*0.8), 8)
                which_to_like = random.sample(list(range(min(photos,13))), how_much_like)
                print("Which photo to like:", which_to_like)  
                for j in which_to_like: 
                    driver.find_elements_by_xpath("//div[contains(@class, '_9AhH0')]")[j].click() #click on photo
                    time.sleep(randint(3,5))
                    driver.find_elements_by_xpath("//div[contains(@class, 'QBdPU ')]")[-4].click() #like its photo
                    time.sleep(randint(5,10))
                    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform() #return to last page
                    time.sleep(randint(3,5))
                text = f"{i} : {which_to_like}\n"
                save(text)

InstaBot_login("marzenakwasnicka.fotografia", "Westernblot2449", driver)
while True:
    for i in range(0,5):
        go_to_hasztag(driver)
        time.sleep(randint(10, 12))
    time.sleep(randint(10, 60))
    go_to_hasztag(driver)


# In[ ]:




