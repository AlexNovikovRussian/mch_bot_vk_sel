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
                today = datetime.datetime.today().strftime("%d")
                print(today)
                
                dates = bs.find_all(text=re.compile(today))

                date = dates[0].parent.parent
                print(date)

                l = dr.find_element_by_xpath('//mat-icon[@aria-label="logout"]')
                l.click()

                send_message(event.user_id, "done")
            else:
                send_message(event.user_id, "Ты ввёл что-то не то! Попробуй ещё раз.")

