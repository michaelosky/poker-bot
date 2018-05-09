import discord
import settings

import skills

TOKEN = settings.token

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    out_message = skills.reply_message(message)
    if not out_message:
        return

    await client.send_message(message.channel, out_message)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
