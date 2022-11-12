######### Documentation #########
# Author:        Zachary Averbach
# Creation Date: August 27th, 2020
# Description: This program runs 
# a bot on discord that uses user inputed keywords to grab
# news articles related to said keywords using Selenium 
# WebDriver for Google Chrome.
######### Documentation #########

import os
import discord
import random
import time

from discord.ext import commands
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from pathlib import Path

#########--CONSTANTS--#########
MY_ANIME_LIST_URL='https://myanimelist.net/'
#########--PATHS--#########
path_to_here = Path(__file__).parent
#data folder path
dfp = path_to_here / r'data'
#Chrome driver path
CHROME_DRIVER_PATH = r'chromedriver_win32/chromedriver.exe'
#########--PATHS--#########

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    print('Type away.')

@bot.command(name='grab...anime',help='Grabs specified anime link from "My Anime-List"')
async def get_Anime(ctx,anime_name):
    options = Options()
    #Set headless mode to true.
    options.headless = False
    options.add_argument("window-size=1920x1080")

    #Launches an instance of webdriver
    print('Initializing webdriver...')

    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH,options=options)
    driver.maximize_window()
    #driver.get(MY_ANIME_LIST_URL)
    driver.get('https://www.google.com/')
    await ctx.send('Grabbing '+ anime_name + ' from My Anime-List')

    driver.implicitly_wait(5)
     #search_anime = driver.find_element_by_xpath(Xpath)
    search_anime = driver.find_elements_by_name('q')
    search_anime[0].click().send_keys(anime_name)
    #search_anime.send_keys(anime_name)
    #print(str(search_anime))
    #driver.find_element_by_xpath(Xpath).click()
    
    #search_anime.send_keys(str(anime_name))
    #search_anime.send_keys(Keys.ENTER)

bot.run(TOKEN)

