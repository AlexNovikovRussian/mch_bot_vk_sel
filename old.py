import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from time import sleep
from os import environ as env
import datetime
import re

dr = webdriver.Chrome()
token = env["VK_TOKEN"]

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)

def send_message(id, message):
    print("send "+message)
    vk.method('messages.send', {'user_id': id, 'message': message, "v":'5.69'})

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text
            if(request == "/get"):
                dr.get("https://www.mos.ru/pgu/ru/services/procedure/0/0/7700000010000187206/")

                el = dr.find_elements_by_xpath("//*[contains(text(), 'Получить услугу')]")
                el[0].click()

                l = dr.find_element_by_id('login')
                l.send_keys(env["MOS_LOGIN"])

                l = dr.find_element_by_id('password')
                l.send_keys(env["MOS_PASSWORD"])

                l = dr.find_element_by_id('bind')
                l.submit()

                sleep(15)

                bs = BS(dr.page_source, "html.parser")
                # today = datetime.datetime.today().strftime("%d")
                
                # todayWd = ""
                
                # etwd = datetime.datetime.today().strftime("%a")
                
                # if etwd == "Sun":
                # 	todayWd = "вс"
                # elif etwd == "Fri":
                # 	todayWd = ""
                
                # todayFull = today + ", " + todayWd
                # print(todayFull)
                
                #homework-description
                allHW = bs.findAll("div", {'class' : "homework-description"})
                #day e.parent.parent.parent.parent.parent.findPreviousSibling('div').findChildren("h3")[0].text
                #subject e.parent.parent.parent.parent.findChildren("div", {"class":"subject"})[0].findChildren("div")[0].findChildren("div")[0].findChildren("span")[0].text

                for hw in allHW:
                	print(hw.parent.parent.parent.parent.parent.findPreviousSibling('div').findChildren("h3")[0].text)
                	print(hw.parent.parent.parent.parent.findChildren("div", {"class":"subject"})[0].findChildren("div")[0].findChildren("div")[0].findChildren("span")[0].text)
                	print(hw.text)

                #logout
                l = dr.find_element_by_xpath('//mat-icon[@aria-label="logout"]')
                l.click()

                #send message to user
                send_message(event.user_id, "done")
            else:
            	# in case when user sends something wrong
                send_message(event.user_id, "Ты ввёл что-то не то! Попробуй ещё раз.")

