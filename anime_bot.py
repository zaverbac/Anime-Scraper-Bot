######### Documentation #########
# Author:        Zachary Averbach
# Creation Date: August 27th, 2020
# Description: This program runs 
# a bot on discord that uses user inputed keywords to grab
# anime from Anime Planet using Selenium 
# WebDriver for Google Chrome.
######### Documentation #########


#########NEED TO ADD#########
#Need to add SQLite to use as 
#database to allow users to create
#and edit list that they created.
#########NEED TO ADD#########

#Imports OS
import os
#Imports time packages
import time
#Imports discords API
import discord
#Imports couchdb packages
import couchdb
import sqlite3

from sqlite3 import Error
from discord.ext import commands
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from selenium.common.exceptions import NoSuchElementException


#########CONSTANTS#########
SITE_URL='https://www.anime-planet.com'
HEADLESS=True
NO_RESULTS='//*[@id="siteContainer"]/div[3]/p'
#########CONSTANTS#########
path_to_here = Path(__file__).parent
#data folder path

#Chrome driver path
CHROME_DRIVER_PATH = path_to_here / r'chromedriver_win32/chromedriver.exe'
USER_LISTS_PATH = path_to_here / r'User_Anime_List'
#########--PATHS--#########

print(CHROME_DRIVER_PATH)
#Grabs .env from external location
load_dotenv()
TOKEN=os.getenv('DISCORD_TOKEN')


#########COUCHDB TUTORIAL#########
#SITE: javatpoint
#URL: https://www.javatpoint.com/python-couchdb
#########CLOUDDB TUTORIAL#########


#NEED TO MAKE SELF SERVER ADMIN FOR COUCHDB

#Prefix for every bot command.
bot = commands.Bot(command_prefix='$')

#Shows that the bot is ready
@bot.event
async def on_ready():
     print(f'{bot.user.name} has connected to Discord!')
     print('Type away.')

#Grabs the anime user provides.
@bot.command(name='grabanime',help='Provides link to anime specified by user. Must be specific.')
#Multiple agument if user needs 
async def grab_anime(ctx,*args):
     num_args = len(list(args))
     #Empty String for initialization.
     combine = ""

     if(num_args > 50):
          ctx.send("No anime has a name that long")
          return

     #Combines the Strings together into the full name.
     #Python doesn't recognize discords arguments being passed
     #as a single String.
     for i in args:
          combine += " " + i

     #Removes leading and trailing whitespaces.
     full_anime_name = combine.strip()

     options = Options()
     #Hides generated Chrome browser
     options.headless=HEADLESS
        
     print("Starting up webdriver...")
     driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH,options=options)

     if(driver.get_window_size() != 'window-size=1920x1080'):
          options.add_argument('window-size=1920x1080')

     #Maximizes chrome window
     driver.maximize_window()
     #Navigates to given URL
     driver.get(SITE_URL)

     await ctx.send('Grabbing: ' + full_anime_name + ' from Anime Planet')

     #Allows webpage to fully load.
     driver.implicitly_wait(3)

     #Goes to searchbar and searches all related titles
     search = driver.find_element_by_xpath('//*[@id="siteSearch-input"]')
     search.click()
     search.send_keys(full_anime_name); search.send_keys(Keys.ENTER)

     #Need to make it so bot send 'No results found
     #if given xpath exist and have it continue if 
     #xpath doesn't exist.      
     
     await ctx.send(driver.current_url)
     driver.close()

#########TO DO#########
#Need to make sure people can't delete
#other peoples lists.
#
#Need to implement SQLite so users
#can add and edit lists.
#########TO DO#########

#Creates custom list by user that will be added to sqlite database.
@bot.command(name='ccl',help=':Creates a custom list that the user can add or remove anime from.')
async def create_list(ctx,list_name):
     print()
#Adds anime to list in sqlite database
@bot.command(name='addAnime',help=':Adds anime to user designated list.')
async def addAnime(ctx,anime_name):
     print()
#Removes anime from list in sqlite database
@bot.command(name='removeAnime',help=':Removes anime from user designated list.')
async def removeAnime(ctx,anime_name):
     print()
#Deletes list in sqlite database
@bot.command(name='dellist',help=':Deletes users list if user is the one that created the list')
async def deleteList(ctx,list_name):
     #
     print()

#Runs the bot with the corresponding token.
bot.run(TOKEN)