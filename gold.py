"""!gold <command> <user> <arguments> is a praise tracking system

Commands:

* `meet`: Add someone new to track

* `star`: Give a coworker a gold star!

* `goodjob`: Reward a coworker for a job well done!

* `remember`: Tell me something to remember about your coworker

* `whois`: Ask me about your coworker

"""
import argparse
import json
import os
import re
import requests


def create_database(server):
    server.query('''
        CREATE TABLE IF NOT EXISTS gold_users (
            id text PRIMARY KEY,
            main integer,
            secondary integer,
            drawer text)
    ''')


ARGPARSE = argparse.ArgumentParser()
ARGPARSE.add_argument('command', nargs=1)
ARGPARSE.add_argument('body', nargs='*')

MENTION_REGEX = "<@(|[WU].+?)>(.*)"
MAIN_EMOJI = ":star2:"
SECONDARY_EMOJI = ":confetti_ball:"


def parse_mentions(body):
    """ Finds username mentions in message text and returns User ID"""
    user = re.search(MENTION_REGEX, body)
    return (user.group(1), user.group(2).strip()) if user else (None, None)


def get_count(server, user, category):
    count = str(server.query('''
        SELECT ? FROM gold_users WHERE id = ?
        ''', category, user))
    return count


def increment_count(server, user, category):
    server.query('''
        UPDATE gold_users SET ? = ? + 1 WHERE id = ?
        ''', category, category, user)


def add_user(server, msg, body):
    user, body = parse_mentions(body)
    server.query('''
        INSERT INTO gold_users(id, main, secondary, drawer)
        VALUES (?, ?, ?, ?)''', user, 0, 0, "someone I know")
    return (f"Got it - I now know <@{user}>. Hi!")


def oneup(server, msg, body):
    user, body = parse_mentions(body)
    increment_count(server, user, "main")
    count = get_count(server, user, "main")
    return (f"Woooooo, <@{user}> has {count} {MAIN_EMOJI}")


def good_job(server, msg, body):
    user, body = parse_mentions(body)
    increment_count(server, user, "secondary")
    count = get_count(server, user, "secondary")
    return (f"<@{user} is up to {count} {SECONDARY_EMOJI} :bananadance:")


def remember(server, msg, body):
    user, body = parse_mentions(body)
    drawer = get_count(server, user, "drawer")
    drawer = f"{drawer}, {body}"
    server.query('''
        UPDATE gold_users SET drawer = ? WHERE id = ?
        ''', drawer, user)
    return (f"Okay, <@{user}> {drawer}")


def whois(server, msg, body):
    user, body = parse_mentions(body)
    drawer = get_count(server, user, "drawer")
    main = get_count(server, user, "main")
    secondary = get_count(server, user, "secondary")
    return (f"<@{user}> is {drawer} with {main} {MAIN_EMOJI} and {secondary} {SECONDARY_EMOJI}")


COMMANDS = {
    "meet": add_user,
    "star": oneup,
    "goodjob": good_job,
    "remember": remember,
    "whois": whois
}


def gold(server, msg, cmd, body):
    try:
        command_func = COMMANDS.get(cmd)
        return command_func(server, msg, body)
    except KeyError:
        return


def on_message(msg, server):
    create_database(server)

    text = msg.get("text", "")
    match = re.findall(r"!gold\s*(.*)", text)
    if not match:
        return

    # github.py: If given -h or -v, argparse will try to quit. Don't let it.
    try:
        ns = ARGPARSE.parse_args(match[0].split(' '))
    except SystemExit:
        return __doc__
    command = ns.command[0]

    # no arguments, print help
    if not len(command):
        return __doc__

    return gold(server, msg, command, msg["text"])
