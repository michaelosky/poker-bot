import discord
import re

skill_code_regex = re.compile('^!\S+(\s.*)?$')

skill_code_poll = '!poll'
skill_code_poll_done = '!polldone'
skill_code_quiz = '!quiz'
skill_code_test = '!test'

def reply_message(in_message):
    skill_code_regex_match = skill_code_regex.match(in_message.content)
    if not skill_code_regex_match:
        return

    skill_code = skill_code_regex_match.group()
    if skill_code == skill_code_test:
        return skill_test(in_message)
    elif skill_code == skill_code_poll:
        return skill_poll(in_message)
    elif skill_code == skill_code_poll_done:
        return skill_poll_done(in_message)
    elif skill_code == skill_code_quiz:
        return skill_quiz(in_message)


def skill_test(in_message):
    out_message = "test: 72o > AA"
    return out_message

def skill_poll(in_message):
    out_message = "poll"
    return out_message

def skill_quiz(in_message):
    out_message = "quiz"
    return out_message
