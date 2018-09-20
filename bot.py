import discord
import settings
import hiddenSettings
import asyncio

import skills
import data

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    await skills.invoke_skill(client, skills.SkillInvokation.MESSAGE, message)

@client.event
async def on_reaction_add(reaction, user):
    await skills.invoke_skill(client, skills.SkillInvokation.REACTION_ADD, reaction, user)

@client.event
async def on_reaction_remove(reaction, user):
    await skills.invoke_skill(client, skills.SkillInvokation.REACTION_REMOVE, reaction, user)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await pb_send_message(turned_on_message())
    await data.read_config()
    await skills.invoke_skill(client, skills.SkillInvokation.STARTUP)

async def get_channel_to_send_on(client):
    print("run get_channel_to_send_on")
    for server in client.servers:
        print("loop through server=" + str(server))
        if server.name not in settings.server_names:
            print(" server skip")
            continue
        for channel in server.channels:
            print(" loop through channel=" + str(channel))
            if str(channel) in settings.channel_names:
                print("  found channel")
                return channel

def turned_on_message():
    return "ya boi was just turned on"

async def pb_send_message(message):
    await client.wait_until_ready()
    if client.is_closed:
        return
    for server in client.servers:
        if server.name not in settings.server_names:
            continue
        for channel in server.channels:
            if str(channel) in settings.channel_names:
                await client.send_message(channel, message)

if __name__ == "__main__":
    client.run(hiddenSettings.token)
