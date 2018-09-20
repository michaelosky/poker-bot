import asyncio

from bot import get_channel_to_send_on
from data import get_skill_config, set_skill_config, save_config

from collections import defaultdict, OrderedDict

import skills

global poker_msg, poker_state
poker_msg = None
poker_state = None

class PokerPollState(object):
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

    emoji_table_inverted = {v:k for k,v in emoji_table.items()}

    def __init__(self):
        self.current_tally = defaultdict(int)
        self.current_tally_to_user = defaultdict(set)
        self.poll_active = True
    
    def build_updated_msg(self):
        unique_users = set([user for _, unique_users in self.current_tally_to_user.items() for user in unique_users])
        
        updated_msg = "Select your preferred day to play poker:\n"
        updated_msg += " | ".join(["%s: %d" % (key, max(0, self.current_tally[key] - 1)) for key in PokerPollState.day_order])
        
        updated_msg += " (%d people voted)" % len(unique_users)
        
        if not self.poll_active:
            updated_msg += " [Ended]"
        
        return updated_msg
    
    def add_raw_reaction(self, client, reaction, user):
        if reaction.message.author.id != client.user.id:
            print("ignoring non-bot reaction")
            return
        
        if reaction.message.id != poker_msg.id:
            print("ignoring non-correct msg reaction")
            return
        
        print("{0:02x}".format(ord(reaction.emoji)))
        
        
        day_letter = PokerPollState.emoji_table_inverted.get(reaction.emoji, None)
        if not day_letter:
            print("Invalid emoji - returning")
            return
        
        self.current_tally[PokerPollState.emoji_day_to_full_day[day_letter]] += 1
        
        if str(user.id) != str(client.user.id):
            self.current_tally_to_user[PokerPollState.emoji_day_to_full_day[day_letter]].add(user.id)
        
        #print(self.current_tally)
        #print(self.current_tally_to_user)
        
        updated_msg = self.build_updated_msg()
        
        return updated_msg
    
    def remove_raw_reaction(self, client, reaction, user):
        if reaction.message.author.id != client.user.id:
            print("ignoring non-bot reaction")
            return
        
        if reaction.message.id != poker_msg.id:
            print("ignoring non-correct msg reaction")
            return
        
        print("{0:02x}".format(ord(reaction.emoji)))
        
        day_letter = PokerPollState.emoji_table_inverted.get(reaction.emoji, None)
        if not day_letter:
            print("Invalid emoji - returning")
            return
        
        self.current_tally[PokerPollState.emoji_day_to_full_day[day_letter]] -= 1
        
        if str(user.id) != str(client.user.id):
            self.current_tally_to_user[PokerPollState.emoji_day_to_full_day[day_letter]].remove(user.id)
        
        updated_msg = self.build_updated_msg()
        
        return updated_msg
    
    def end_poll(self):
        self.poll_active = False
        return self.build_updated_msg()


async def on_reaction_add(client, reaction, user):
    global poker_msg, poker_state
    
    # updated_msg = ...
    
    updated_msg = poker_state.add_raw_reaction(client, reaction, user)
    
    await client.edit_message(poker_msg, updated_msg)
    #client.delete_message(reaction.message)

async def on_reaction_remove(client, reaction, user):
    global poker_msg, poker_state
    
    updated_msg = poker_state.remove_raw_reaction(client, reaction, user)
    await client.edit_message(poker_msg, updated_msg)
    
    #client.delete_message(reaction.message)

async def save_poker_poll_cfg(channel, message):
    global poker_msg
    await set_skill_config("pokerpoll", "channel_id", channel.id if channel else None)
    await set_skill_config("pokerpoll", "message_id", message.id if channel else None)
    await save_config()

async def post_poker_poll(client):
    global poker_msg, poker_state
    
    print("post_poker_poll called")
    
    await client.wait_until_ready()
    counter = 0
    channel = await get_channel_to_send_on(client)
    
    if poker_msg is None:
        print("making new poker_msg")
        poker_msg = await client.send_message(channel, "Select your preferred day to play poker:")
        try:
            await client.pin_message(poker_msg)
        except:
            print("Could not pin message.")
        poker_state = PokerPollState()
        for emoji_step in PokerPollState.emoji_add_order:
            await client.add_reaction(poker_msg, PokerPollState.emoji_table[emoji_step])
        await save_poker_poll_cfg(channel, poker_msg)
    else:
        print("poker_msg already exists: "+str(poker_msg))
        await client.send_message(channel, "Poker poll already exists. Try !poll end.")
    
    #await asyncio.sleep(60) # task runs every 60 seconds


async def on_message(client, in_message):
    global poker_msg, poker_state
    content = in_message.content
    print("Content: " + content)
    
    args = content.split(" ")[1:]
    
    if not len(args):
        print("No args found...?")
        await client.send_message(in_message.channel, "Create a poll for poker! !poll start - start a poll; !poll end - end a poll")
    elif args[0] == "start":
        print("Start")
        if not poker_state:
            await client.send_message(in_message.channel, "Creating poker poll.")
            client.loop.create_task(post_poker_poll(client))
        else:
            await client.send_message(in_message.channel, "Poker polls active. Close a poll for poker: !poll end.")
    elif args[0] == "end":
        print("End")
        if poker_state:
            updated_msg = poker_state.end_poll()
            await client.edit_message(poker_msg, updated_msg)
            try:
                await client.unpin_message(poker_msg)
            except:
                print("Could not unpin message.")
            poker_msg = None
            poker_state = None
            await save_poker_poll_cfg(None, None)
            await client.send_message(in_message.channel, "Poker poll ended.")
        else:
            await client.send_message(in_message.channel, "No poker polls active. Create a poll for poker: !poll start.")

async def on_startup(client):
    global poker_msg, poker_state
    
    print("pokerpoll is starting up...")
    
    channel_id = await get_skill_config("pokerpoll", "channel_id")
    message_id = await get_skill_config("pokerpoll", "message_id")
    
    if channel_id and message_id:
        print("Loading original channel_id=%s and message_id=%s..." % (channel_id, message_id))
        channel = client.get_channel(channel_id)
        if not channel:
            print("  Failed to load channel: %s" % channel_id)
        else:
            poker_msg = await client.get_message(channel, message_id)
            
            # HACK: https://github.com/Rapptz/discord.py/issues/895
            client.messages.appendleft(poker_msg)
            poker_state = PokerPollState()
            
            for reaction in poker_msg.reactions:
                for user in await client.get_reaction_users(reaction):
                    poker_state.add_raw_reaction(client, reaction, user)
            
            updated_msg = poker_state.build_updated_msg()
            await client.edit_message(poker_msg, updated_msg)
    return True
