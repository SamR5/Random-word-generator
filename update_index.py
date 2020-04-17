#!/usr/bin/python3
# -*- coding: utf-8 -*-

# generate indexes for the word generator

import itertools as it
import string as s
import pickle as pk
import unidecode
import re


def first_letter(words):
    """
    Return the probability of each letter to be the first of a word
    """
    f = "".join([w[0] for w in words])
    res = {i:float(f.count(i)) / len(f) for i in s.ascii_lowercase}
    # the letters are on a line from 0 to 1 and their length are the proba
    res2 = dict()
    prev = 0.0
    for k, v in sorted(res.items()):
        res2[k] = (prev, prev + v)
        prev += v
    return res2

def two_first_letter(words):
    """
    Return the probability of each couple of letter to be the first of a word
    """
    f = [w[:2] for w in words]
    couples = ["".join(i) for i in it.permutations(s.ascii_lowercase, 2)] +\
              [i*2 for i in s.ascii_lowercase]
    res = {i:float(f.count(i)) / len(f) for i in couples
           if f.count(i) > 10} # less than 10 words is rare
    # the letters are on a line from 0 to 1 and their length are the proba
    res2 = dict()
    prev = 0.0
    for k, v in sorted(res.items()):
        if v == 0.0:
            continue
        res2[k] = (prev, prev + v)
        prev += v
    return res2

def letter_quadruples(words):
    """
    Return the probability of each letter to be after a set of 3 letter
    """
    quadriples = {''.join(perm):{i:float(0) for i in s.ascii_lowercase}
                  for perm in list(it.product(s.ascii_lowercase, repeat=3)) +\
                              [i*3 for i in s.ascii_lowercase]}
    
    for w in words:
        for i in range(len(w) - 2 - 2): # -2 to avoid the two last letter
            quadriples[w[i:i+3]][w[i+3]] += 1
    # delete when less than 10 occurences
    for tri in quadriples.keys():
        for fourthLetter in quadriples[tri].keys():
            if quadriples[tri][fourthLetter] < 10:
                quadriples[tri][fourthLetter] = 0

    for tri in quadriples.keys():
        total = sum(quadriples[tri].values())
        if total == 0:
            continue
        for fourthLetter in quadriples[tri].keys():
            quadriples[tri][fourthLetter] /= total
    # eliminates the impossible triples (probability 0)
    quadriples = {i:j for i, j in quadriples.items() if sum(j.values()) != 0}
    todel = []
    for t in quadriples.keys():
        for k, v in quadriples[t].items():
            if v == 0.0:
                todel.append((t, k))
    for i, j in todel:
        del quadriples[i][j]
    
    # the letters are on a line from 0 to 1 and their length are the proba
    res3 = dict()
    for i, j in quadriples.items():
        res2 = dict()
        prev = 0.0
        for k, v in sorted(j.items()):
            res2[k] = (prev, prev + v)
            prev += v
        res3[i] = res2
    return res3

def two_last_letter(words):
    """
    Return the probability of each letter to be after a set of 2 letter and at the end
    """
    triples = {''.join(perm):{i:float(0) for i in s.ascii_lowercase}
               for perm in list(it.permutations(s.ascii_lowercase, 2)) +\
                           [i*2 for i in s.ascii_lowercase]}
    
    for w in words:
        if len(w) < 3:
            continue
        triples[w[-3:-1]][w[-1]] += 1

    for duo in triples.keys():
        total = sum(triples[duo].values())
        if total == 0:
            continue
        for thirdLetter in triples[duo].keys():
            triples[duo][thirdLetter] /= total
    # eliminates the impossible triples (probability 0)
    triples = {i:j for i, j in triples.items() if sum(j.values()) != 0}
    todel = []
    for t in triples.keys():
        for k, v in triples[t].items():
            if v == 0.0:
                todel.append((t, k))
    for i, j in todel:
        del triples[i][j]
    
    # the letters are on a line from 0 to 1 and their length are the proba
    res3 = dict()
    for i, j in triples.items():
        res2 = dict()
        prev = 0.0
        for k, v in sorted(j.items()):
            res2[k] = (prev, prev + v)
            prev += v
        res3[i] = res2
    return res3

if __name__ == '__main__':
    Liste = []
    with open("lexique.txt", 'r', encoding='latin1') as lexique:
        for l in lexique.readlines():
            l = unidecode.unidecode(l.strip('\n'))
            if re.search(r'[^a-z]', l) is not None:
                continue
            Liste.append(l)
    
    Liste = list(set(Liste))
    
    data = {'firstLetter':first_letter(Liste),
            'firstTwoLetter':two_first_letter(Liste),
            'quadLetter':letter_quadruples(Liste),
            'twoLastLetter':two_last_letter(Liste)}
    
    with open('index', 'wb') as index:
        pk.dump(data, index)
