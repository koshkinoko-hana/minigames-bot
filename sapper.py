#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

games = {}

sapper_field = '''🔵🔵🔵🔵🔵
🔵🔵🔵🔵🔵
🔵🔵🔵🔵🔵
🔵🔵🔵🔵🔵
🔵🔵🔵🔵🔵'''


def generate():
    return random.sample(range(25), 10)


def init_sapper(user_id):
    new_game = generate()
    games.update({user_id: new_game})
    return sapper_field


def answer(user_id, ans):
    game = games.get(user_id)
    gamer_field = sapper_field

    return sapper_field
