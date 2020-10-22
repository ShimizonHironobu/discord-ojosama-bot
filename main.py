import discord

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

    if message.author.id == 401738155159584769:
        return 

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

client.run('NzY4ODgwNzA1NzUyNzkzMTMw.X5G59Q.tzr60B2M5biFgIPxsTds42SbbRI')
