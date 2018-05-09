import discord
import re
import cards

skill_code_regex = re.compile('^!\S+(\s.*)?$')

skill_code_poll = '!poll'
skill_code_quiz = '!quiz'
skill_code_test = '!test'

async def invoke_skill(client, in_message):
    skill_code_regex_match = skill_code_regex.match(in_message.content)
    if not skill_code_regex_match:
        return False

    skill_code = skill_code_regex_match.group()
    if skill_code == skill_code_test:
        return await skill_test(client, in_message)
    elif skill_code == skill_code_poll:
        return await skill_poll(client, in_message)
    elif skill_code == skill_code_quiz:
        return await skill_quiz(client, in_message)


async def skill_test(client, in_message):
    out_message = "test: 72o > AA"
    await client.send_message(in_message.channel, out_message)
    return True

async def skill_poll(client, in_message):
    out_message = "poll"
    await client.send_message(in_message.channel, out_message)
    return True

async def skill_quiz(client, in_message):
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