import discord
import settings
import poll
import hiddenSettings
import asyncio

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!test'):
        msg = "72o > AA".format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await pb_send_message(turned_on_message())

def turned_on_message():
    return "ya boi was just turned on"

async def pb_send_message(message):
    await client.wait_until_ready()
    if client.is_closed:
        return
    for server in client.servers:
        if server.name not in setting.server_names
            continue
        for channel in server.channels:
            if str(channel) in settings.channel_names:
                await client.send_message(channel, message)

client.run(hiddenSettings.token)
