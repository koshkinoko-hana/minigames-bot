#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import copy

games = {}

sapper_field = '''🔵🔵🔵🔵🔵
🔵🔵🔵🔵🔵
🔵🔵🔵🔵🔵
🔵🔵🔵🔵🔵
🔵🔵🔵🔵🔵'''

row_names = ['a', 'b', 'c', 'd', 'e']

empty_answer = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

def generate():
    ans_list = random.sample(range(25), 10)
    res = copy.deepcopy(empty_answer)
    for i in ans_list:
        res[i // 5][i % 5] = 1
    print('Generated answer: ')
    print(ans_list)
    print(res)
    return res


def init_sapper(user_id):
    new_game = generate()
    games.get(user_id)
    total = 0
    if user_id in games:
        total = games.get(user_id)['total']
    games.update({
        user_id: {
            'game': new_game,
            'touched_count': 0,
            'total': total,
            'answer': copy.deepcopy(empty_answer)
        }
    })
    print('Game for user ' + str(user_id))
    field = '<CODE>_ 1 2 3 4 5\n'
    rows = sapper_field.split('\n')
    for i in range(len(rows)):
        field += row_names[i] + rows[i] + '\n'
    field += '</CODE>'
    return field


def reformat_answer(user_id, ans):
    game = games.get(user_id)
    answer_list = ans.split(',')
    dif = game['touched_count'] + len(answer_list) - 15
    if dif > 0:
        game['touched_count'] = 15
    else:
        game['touched_count'] += len(answer_list)

    for a in range(len(answer_list) - (dif if dif > 0 else 0)):
        item = answer_list[a].strip().lower()
        i = row_names.index(item[0])
        j = int(item[1]) - 1
        game['answer'][i][j] = 1

        if game['game'][i][j] == 1:
            game['total'] += 1

    print('User answered: ')
    print(ans)
    print(game['answer'])


def clear(user_id):
    game = games.get(user_id)
    if game:
        game['total'] = 0


def answer(user_id, ans):
    game = games.get(user_id)
    if not game:
        return 'Привет! Чтобы начать игру, введи /game .'
    res_field = '<CODE>_ 1 2 3 4 5\n'

    reformat_answer(user_id, ans)
    final = game['touched_count'] == 15
    for i in range(5):
        res_field += row_names[i]
        for j in range(5):
            if game['answer'][i][j] and game['game'][i][j]:
                res_field += '🟢'
            elif game['answer'][i][j]:
                res_field += '⚪️'
            elif final and game['game'][i][j]:
                res_field += '🔴'
            else:
                res_field += '🔵'
        res_field += '\n'
    res_field += '</CODE>'
    before = 'Ходы закончились! Финальное поле:\n' if final \
        else 'осталось {0} ходов:\n'.format(15 - game['touched_count'])
    after = 'у вас {0} очков.'.format(game['total'])
    if game['touched_count'] == 15:
        after += 'Чтобы начать новую игру, введите /game . Чтобы обнулить достижения, введите /clear .'
    return before + res_field + after
