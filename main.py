import discord
import random
import sys
import os
from discord.ext import commands

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
from lib import (
    config,
    shindan_client,
    log
)

bot = commands.Bot(command_prefix="$")

@bot.event
async def on_ready():
    print('{0.user}がログインいたしましたわ'.format(bot))

@bot.event
async def on_message(message):
    # print('message: ' + message.content)
    # print('author: ' + str(message.author))
    # print('id: ' + str(message.author.id))
    # print('----------------------------')

    if message.content.startswith('ごきげんよう'):
        print(str(message.author.id))
        await message.channel.send('くたばりなさい ' + str(message.author))

    # if message.author.id == 700335402736680982:
    #     await message.channel.send('....あなたのことを愛していますわ❤️ ' + str(message.author))

    # if message.content.startswith('おぱんつみせて'):
    #     if message.author.id == 700335402736680982:
    #         await message.channel.send('もう、恥ずかしいですわ❤️ ' + str(message.author))
    #     else:
    #         await message.channel.send('しね' + str(message.author))

    # if message.content.startswith('おっぱいおおきいね'):
    #     await message.channel.send('Zカップですわ')

    
    if message.content.startswith('診断して'):
        shindan_list = shindan_client.get_list()
        random_index = random.randrange(0, len(shindan_list)-1, 1)
        shindan_id = shindan_list[random_index]["id"]
        await message.channel.send(shindan_client.request(shindan_id, name=str(random.random())))


@bot.command
async def shindan_add(ctx, url):
    result = shindan_client.add(url)
    message = "登録に成功しましたわ！"
    if (result == "2"):
        message = "既に登録に成功されておりますわ！"
    if (result == "0"):
        message = "登録にしっぱいしましたの～～～～"
    await ctx.send(message)

bot.run(config.get('app.discord.bot_token'))
