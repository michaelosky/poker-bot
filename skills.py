import discord
import re
import cards
import pokerpoll

from collections import defaultdict

from enum import Enum, unique

@unique
class SkillInvokation(Enum):
    STARTUP = -1
    MESSAGE = 0
    REACTION_ADD = 1
    REACTION_REMOVE = 2

invokations = defaultdict(set)

def invokation_support(invokes):
    def invokation_support_dec(func):
        for invoke in invokes:
            invokations[invoke].add(func)
        def invokation_support_f(*args, **kwargs):
            return func(*args, **kwargs)
        return invokation_support_f
    return invokation_support_dec

## Begin

skill_code_regex = re.compile('^!\S+(\s.*)?$')

skill_code_poll = '!poll'
skill_code_quiz = '!quiz'
skill_code_test = '!test'

async def invoke_skill(client, invokation, *args, **kwargs):
    if invokation == SkillInvokation.MESSAGE:
        in_message = args[0]
        skill_code_regex_match = skill_code_regex.match(in_message.content)
        if not skill_code_regex_match:
            return False

        skill_code = skill_code_regex_match.group()
        skill_code_cmd = skill_code.split(" ")[0]
        if skill_code_cmd == skill_code_test:
            return await skill_test(client, invokation, *args, **kwargs)
        elif skill_code_cmd == skill_code_poll:
            return await skill_poll(client, invokation, *args, **kwargs)
        elif skill_code_cmd == skill_code_quiz:
            return await skill_quiz(client, invokation, *args, **kwargs)
    else:
        # Call all callbacks that support the invokation
        #print(invokation)
        invokation_callbacks = invokations.get(invokation, [])
        #print(invokation_callbacks)
        
        for invokation_callback in invokation_callbacks:
            await invokation_callback(client, invokation, *args, **kwargs)

@invokation_support([SkillInvokation.MESSAGE])
async def skill_test(client, invokation, in_message):
    out_message = "test: 72o > AA"
    await client.send_message(in_message.channel, out_message)
    return True

@invokation_support([SkillInvokation.MESSAGE, SkillInvokation.REACTION_ADD, SkillInvokation.REACTION_REMOVE, SkillInvokation.STARTUP])
async def skill_poll(client, invokation, *args, **kwargs):
    if invokation == SkillInvokation.STARTUP:
        await pokerpoll.on_startup(client, *args, **kwargs)
    elif invokation == SkillInvokation.MESSAGE:
        await pokerpoll.on_message(client, *args, **kwargs)
    elif invokation == SkillInvokation.REACTION_ADD:
        await pokerpoll.on_reaction_add(client, *args, **kwargs)
    elif invokation == SkillInvokation.REACTION_REMOVE:
        await pokerpoll.on_reaction_remove(client, *args, **kwargs)
    return True

@invokation_support([SkillInvokation.MESSAGE])
async def skill_quiz(client, invokation, in_message):
    card_one, card_two = cards.deal_two_cards()
    chen_points, chen_formula_text = cards.chen_formula(card_one, card_two)

    out_message = 'Pre-flop: ' + cards.card_number_to_text(card_one) + ' ' + cards.card_number_to_text(card_two) + \
                  '\nChen Formula: ' + chen_formula_text + str(chen_points) + \
                  '\nPosition: ' + cards.get_random_position_text() + \
                  '\nCheck   Bet   Raise   AllIn   Fold'
    sent_message = await client.send_message(in_message.channel, out_message)

    reaction_list = ['\U0001F1E8', '\U0001F1E7', '\U0001F1F7', '\U0001F1E6', '\U0001F1EB']
    for reaction in reaction_list:
        await client.add_reaction(sent_message, reaction)
    return True
