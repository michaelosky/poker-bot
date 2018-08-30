import discord
import settings
import hiddenSettings
import asyncio

from collections import defaultdict, OrderedDict

import skills

client = discord.Client()

global poker_msg
poker_msg = None

day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Not Available"]

emoji_table = {
    "M": "\U0001f1f2",
    "T": "\U0001f1f9",
    "W": "\U0001f1fc",
    "H": "\U0001f1ed",
    "F": "\U0001f1eb",
    "NA": "\U000026d4"
}

emoji_add_order = ["M", "T", "W", "H", "F", "NA"]

emoji_day_to_full_day = {
    "M": "Monday",
    "T": "Tuesday",
    "W": "Wednesday",
    "H": "Thursday",
    "F": "Friday",
    "NA": "Not Available"
}

current_tally = defaultdict(int)

current_tally_to_user = defaultdict(set)

unique_users_voted = set()

emoji_table_inverted = {v:k for k,v in emoji_table.items()}

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
    #await pb_send_message(turned_on_message())

@client.event
async def on_reaction_add(reaction, user):
    global poker_msg
    
    if reaction.message.author.id != client.user.id:
        print("ignoring non-bot reaction")
        return
    
    if reaction.message.id != poker_msg.id:
        print("ignoring non-correct msg reaction")
        return
    
    print("{0:02x}".format(ord(reaction.emoji)))
    
    day_letter = emoji_table_inverted.get(reaction.emoji, None)
    if not day_letter:
        print("Invalid emoji - returning")
        return
    
    current_tally[emoji_day_to_full_day[day_letter]] += 1
    
    if str(user.id) != str(client.user.id):
        current_tally_to_user[emoji_day_to_full_day[day_letter]].add(user.id)
    
    print(current_tally)
    print(current_tally_to_user)
    
    unique_users = set([user for _, unique_users in current_tally_to_user.items() for user in unique_users])
    print(unique_users)
    
    updated_msg = "Select your preferred day to play poker:\n"
    updated_msg += " | ".join(["%s: %d" % (key, max(0, current_tally[key] - 1)) for key in day_order])
    
    updated_msg += " (%d people voted)" % len(unique_users)
    
    print(updated_msg)
    await client.edit_message(poker_msg, updated_msg)
    #client.delete_message(reaction.message)

@client.event
async def on_reaction_remove(reaction, user):
    global poker_msg
    
    if reaction.message.author.id != client.user.id:
        print("ignoring non-bot reaction")
        return
    
    if reaction.message.id != poker_msg.id:
        print("ignoring non-correct msg reaction")
        return
    
    print("{0:02x}".format(ord(reaction.emoji)))
    
    day_letter = emoji_table_inverted.get(reaction.emoji, None)
    if not day_letter:
        print("Invalid emoji - returning")
        return
    
    current_tally[emoji_day_to_full_day[day_letter]] -= 1
    
    if str(user.id) != str(client.user.id):
        current_tally_to_user[emoji_day_to_full_day[day_letter]].remove(user.id)
    
    print(current_tally)
    print(current_tally_to_user)
    
    unique_users = set([user for _, unique_users in current_tally_to_user.items() for user in unique_users])
    print(unique_users)
    
    updated_msg = "Select your preferred day to play poker:\n"
    updated_msg += " | ".join(["%s: %d" % (key, max(0, current_tally[key] - 1)) for key in day_order])
    
    updated_msg += " (%d people voted)" % len(unique_users)
    
    print(updated_msg)
    await client.edit_message(poker_msg, updated_msg)
    
    #client.delete_message(reaction.message)

def get_channel_to_send_on():
    for server in client.servers:
        if server.name not in settings.server_names:
            continue
        for channel in server.channels:
            if str(channel) in settings.channel_names:
                return channel

async def post_poker_poll():
    global poker_msg
    await client.wait_until_ready()
    counter = 0
    channel = get_channel_to_send_on()
    
    while not client.is_closed:
        counter += 1
        if poker_msg is None:
            poker_msg = await client.send_message(channel, "Select your preferred day to play poker:")
            for emoji_step in emoji_add_order:
                await client.add_reaction(poker_msg, emoji_table[emoji_step])
        await asyncio.sleep(60) # task runs every 60 seconds

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

client.loop.create_task(post_poker_poll())
client.run(hiddenSettings.token)
