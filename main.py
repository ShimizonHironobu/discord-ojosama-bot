# coding: utf-8

import discord
import random
import sys
import os
import json
import re

from discord.ext import commands

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
from lib import (
    config,
    shindan_client,
    log,
    markov
)

bot = commands.Bot(command_prefix="/")

@bot.event
async def on_ready():
    print('{0.user}がログインいたしましたわ'.format(bot))

@bot.event
async def on_message(message):
    log.info('message: ' + message.content)
    log.info('author: ' + str(message.author))
    log.info('id: ' + str(message.author.id))
    log.info('----------------------------')

    #botがメッセージ送信したものは無視
    if message.author.id != bot.user.id :
        if message.content.startswith('ごきげんよう'):
            await message.channel.send('くたばりなさい ' + message.author.mention)
            return
        if message.content.startswith('なんとかいってくださいまし'):
            await message.channel.send(markov.make_markov_sentence())
            return
            
        # マルコフ連鎖のモデル生成用にメッセージを保存する。
        markov.add_raw_message_data(message.content)
    
    if message.content.startswith('診断して'):
        shindan_list = shindan_client.get_list()
        random_index = random.randrange(0, len(shindan_list)-1, 1)
        shindan_id = shindan_list[random_index]["id"]
        await message.channel.send(shindan_client.request(shindan_id, name=str(random.random())))

    await bot.process_commands(message)
    

@bot.command()
async def shindan_add(ctx, url):
    result = shindan_client.add(url)
    message = "登録に成功しましたわ！"
    if (result == 2):
        message = "既に登録されておりますわ！"
    if (result == 0):
        message = "登録に失敗しましたの～～～～"
    await ctx.send(message)



@bot.command()
async def shindan_list(ctx, page=1):

    # 診断リストを取得
    shindan_list = shindan_client.get_list()
    # 登録された診断の数を取得
    shindan_len = len(shindan_list)
    #リストの開始Noを決定
    shindan_no = int(str(page - 1) + "1")
    # ページ中の最大診断Noを決定
    max_shindan_no = page * 10
    # 総ページ数を計算
    last_page = (shindan_len // 10) + (1 if shindan_len % 10 != 0 else 0)
    # embed を作成
    embed = discord.Embed(title="診断リスト",description="")

    # チャットに表示するリストを生成
    list_text = ''
    if shindan_len != 0 :
        while shindan_no <= max_shindan_no :
            if shindan_no > shindan_len :
                break
            shindan_data = shindan_list[shindan_no-1]
            list_text += str(shindan_no) + '.  [' + shindan_data['name'] + '](' + shindan_client.SHINDAN_MAKER_BASE_URL + shindan_data['id'] + ')    \n\n'
            shindan_no+=1
    else : 
        list_text += 'なんの診断も登録されておりませんですのよ！！！！ \n'

    # リストをセット
    embed.add_field(name="登録された診断の一覧なのですわ～～～！！！！",  value=list_text, inline=True)
    embed.set_footer(text='page ' + str(page) + '/' + str(last_page))
    await ctx.send(embed=embed)


@bot.command()
async def shindan(ctx, shindan_no, name="おじょうさま"):
    shindan_list = shindan_client.get_list()
    if not str.isdecimal(shindan_no) :  
        await ctx.send("どの診断か分かりませんわ！")
        return 

    if len(shindan_list) < int(shindan_no) :  
        await ctx.send("どの診断か分かりませんわ！")
        return 

    shindan_id = shindan_list[int(shindan_no) - 1]["id"]
    await ctx.send(shindan_client.request(shindan_id, name))

bot.run(config.get('app.discord.bot_token'))
