import discord
from os import environ as env
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from time import sleep

dr = webdriver.Chrome()

class HWbot(discord.Client):
	async def on_ready(self):
		print('Logged on as {0}!'.format(self.user))

	async def on_message(self,message):
		if message.author != "HW_Show#2095":
			channel = message.channel
			print("Message from {0.author}: {0.content}".format(message))
			if message.content == "/help":
				await channel.send("Bot commands:\n - /get_hw - send homework information")
			elif message.content == "/get_hw":
				dr.get("https://www.mos.ru/pgu/ru/services/procedure/0/0/7700000010000187206/")

				el = dr.find_elements_by_xpath("//*[contains(text(), 'Получить услугу')]")
				el[0].click()

				l = dr.find_element_by_id('login')
				l.send_keys(env["MOS_LOGIN"])

				l = dr.find_element_by_id('password')
				l.send_keys(env["MOS_PASSWORD"])

				l = dr.find_element_by_id('bind')
				l.submit()

				sleep(20)

				bs = BS(dr.page_source, "html.parser")

				#homework-description
				allHW = bs.findAll("div", {'class' : "homework-description"})

				lastDate = ""

				for hw in allHW:
					date = hw.parent.parent.parent.parent.parent.findPreviousSibling('div').findChildren("h3")[0].text
					if date != lastDate:
						await channel.send("\n" + date)
						lastDate = date
					else:
						lastDate = date

					await channel.send(hw.parent.parent.parent.parent.findChildren("div", {"class":"subject"})[0].findChildren("div")[0].findChildren("div")[0].findChildren("span")[0].text)
					await channel.send(hw.text)

				l = dr.find_element_by_xpath('//mat-icon[@aria-label="logout"]')
				l.click()



client = HWbot()
client.run(env["DISCORD_BOT_TOKEN"])
	
