#!/usr/bin/env python
# encoding: utf-8

import sqlite3, string, sys, operator
def connect():
    conn = sqlite3.connect('spam.db')
    c = conn.cursor()
    return c


def tokenize(str):
    """ Split text string (comment) into words"""
    return str.split()

def sanitize(wl):
    """Sanitize wordlist, i.e. decapatilize and such"""
    s = []
    for word in wl:
        for symbol in ['.', '!', ',', '\n', '\r', '?']:
            if symbol in word:
                s.append(symbol)
                word = word.replace(symbol, '')
            
        s.append(word)
    return s

def get_words(c, spam):
    """ Generates a wordlist """
    if spam:
        include_spam = "1"
    else: 
        include_spam = "0"

    wordlist = []

    for row in c.execute("SELECT comment FROM comments WHERE spam=?", (include_spam)):
         new_words = tokenize(row[0])
         wordlist += sanitize(new_words)
    return wordlist

def word_nbr_map(wl):
    """Counts the occurense of every word in a wordlist"""
    wf = dict()
    for word in wl:
        try:
            wf[word] = wf[word] + 1
        except KeyError:
            wf[word] = 1
    return wf

def spamrisk_map(spam_wc, not_spam_wc, total_wc):
    """ Bayes theorem kickin' it"""
    risk_map = dict()
    spam_length = 0
    for w, v in spam_wc.iteritems():
        spam_length += v
    not_spam_length = 0
    for w, v in not_spam_wc.iteritems():
        not_spam_length += v
    total_length = not_spam_length + spam_length

    for word, value in total_wc.iteritems():

        if word not in spam_wc and word in not_spam_wc:
            risk_map[word] = 0.01
        elif word in spam_wc and word not in not_spam_wc:
            risk_map[word] = 0.99
        else:
            g = float(not_spam_wc[word] * 2)
            b = float(spam_wc[word])
            risk_map[word] = ( b / spam_length ) / ( ( g / not_spam_length) +(b / spam_length) ) 

    return risk_map

def spam_prob(comment, word_spamrisk_map):
    """ Calculates the probability that the inputed comment map is spam """
    sc = tokenize(comment)
    l = sanitize(sc)
    cost = dict()
    for word in l: 
        if not word in word_spamrisk_map:
            cost[word] = 0.4
        else:
            cost[word] = abs(0.5 - word_spamrisk_map[word])

    sort_cost_list = sorted(cost.items(), key=lambda x: -x[1])[:15]

    return reduce(operator.mul, [i[1] / (i[1] + reduce(operator.mul, [1 - i[1] for i in sort_cost_list])) for i in sort_cost_list])


def print_wc(wc, length):
    for wp in sorted(wc.items(), key=lambda x: -x[1])[:length]:
        print wp

if __name__ == "__main__":
    c = connect()
    #tokenize words and add to db
    spam_wordlist = get_words(c, spam=True)
    not_spam_wordlist = get_words(c, spam=False)

    spam_wc = word_nbr_map(spam_wordlist)
    not_spam_wc = word_nbr_map(not_spam_wordlist)
    total_wc = word_nbr_map(spam_wordlist + not_spam_wordlist)
    word_spamrisk_map = spamrisk_map(spam_wc, not_spam_wc, total_wc)
    #print_wc(word_spamrisk_map, 100)

    if len(sys.argv) > 1:
        print spam_prob(sys.argv[1], word_spamrisk_map)