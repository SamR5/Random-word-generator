#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Word generator

# todo : proba to 0 if less than 5 occurences ?

import random as r
import re
import pickle as pk


def initialize():
    """"""
    global firstLetter, firstTwoLetter, quadLetter, twoLastLetter
    
    with open('index', 'rb') as index:
        data = pk.load(index)
    firstLetter = data['firstLetter'].items()
    firstTwoLetter = data['firstTwoLetter'].items()
    quadLetter = data['quadLetter']
    twoLastLetter = data['twoLastLetter']

def generate_word(length=5):
    """
    
    """
    w = ""
    # first letter
    while w == "":
        r1 = r.random()
        for k, v in firstTwoLetter:
            if r1 <= v[1] and r1 >= v[0]:
                w += k
    # 3rd letter
    pos = [i[-1] for i in quadLetter.keys() if i.startswith(w)]
    if pos: #i.e not empty
        w += r.choice(pos)
    else:
        return
    # middle
    for i in range(length - 3):
        prevLetter = w[-3:]
        try:
            choices = quadLetter[prevLetter]
        except:
            return
        r2 = r.random()
        for k, v in choices.items():
            if r2 <= v[1] and r2 >= v[0]:
                w += k
    # two last letters
    try:
        lasts = twoLastLetter[w[-2:]]
    except:
        return
    r3 = r.random()
    for k, v in lasts.items():
        if r3 <= v[1] and r3 >= v[0]:
            w += k
    return w

def filtrated_generator(length=5, words=10):
    """"""
    global w
    res = []
    trash = []
    while words > 0:
        words -= 1
        w = generate_word(length)
        if w is None:
            words += 1
            continue
        res.append(w)
        """ never happens
        # 4+ vowels or consonants joined
        if re.search(r'[aeiouy]{4}$|[zrtpqsdfghjklmwxcvbn]{4}$', w) is not None:
            words += 1
            print(1)
            trash.append(res.pop())"""
    return res


if __name__ == '__main__':
    initialize()
    for i in filtrated_generator(8, 20):
        print(i)
