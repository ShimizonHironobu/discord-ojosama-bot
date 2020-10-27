import discord
import config
import random
import shindan_client
client = discord.Client()

@client.event
async def on_ready():
    print('{0.user}がログインいたしましたわ'.format(client))

@client.event
async def on_message(message):
    print('message: ' + message.content)
    print('author: ' + str(message.author))
    print('id: ' + str(message.author.id))
    print('----------------------------')

    if message.content.startswith('ごきげんよう'):
        print(str(message.author.id))
        await message.channel.send('くたばりなさい ' + str(message.author))

    if message.author.id == 700335402736680982:
        await message.channel.send('....あなたのことを愛していますわ❤️ ' + str(message.author))

    if message.content.startswith('おぱんつみせて'):
        if message.author.id == 700335402736680982:
            await message.channel.send('もう、恥ずかしいですわ❤️ ' + str(message.author))
        else:
            await message.channel.send('しね' + str(message.author))

    if message.content.startswith('おっぱいおおきいね'):
        await message.channel.send('Zカップですわ')

    
    if message.content.startswith('診断して'):
        shindan_id_list = config.get('app.shindan.id')
        random_index = random.randrange(0, len(shindan_id_list)-1, 1)
        shindan_id = shindan_id_list[random_index]
        await message.channel.send(shindan_client.request(shindan_id, str(message.author)))

client.run(config.get('app.discord.bot_token'))
