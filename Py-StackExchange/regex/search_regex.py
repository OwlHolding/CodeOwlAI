#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import print_function

# a hack so you can run it 'python demo/search.py'
import sys
import sqlite3
sys.path.append('.')
sys.path.append('..')

try:
    get_input = raw_input
except NameError:
    get_input = input

user_api_key = get_input("Please enter an API key if you have one (Return for none):")
if not user_api_key: user_api_key = 'fAEE*hhUg6RZwKnjsGLYng(('

import stackexchange
so = stackexchange.Site(stackexchange.StackOverflow, app_key=user_api_key)
so.be_inclusive()

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        print('Too many args...')
    
    term = 'regex'
    print('Searching for %s...' % term,)
    sys.stdout.flush()

    qs = so.search(tagged=term, sort='votes', filter='_b')

    conn = sqlite3.connect("../data/regex.db")
    print("Open database success...")

    print('\r--- questions with "%s" in title ---' % (term))
    count = 0

    for q in qs:
        print(q.title, " ", q.view_count)
        # if q.view_count < 5000:
        #     continue
        if count > 0:
            break
        
        statement = "INSERT or REPLACE INTO question VALUES(?,?,?,?,?)"
        data = [(q.id, q.title, q.body, q.score, str(q.creation_date))]
        print(q.id , " ", q.title)
        conn.executemany(statement, data)
        conn.commit()
        
        question = so.question(q.id)
        for a in question.answers:
            print(a.body, " ", a.question_id, " ", a.score)
            print('------------\n')
            aStatement = "INSERT or REPLACE INTO answer VALUES(?,?,?,?)"
            aData = [(a.id, a.body, a.score, a.question_id)]
            conn.executemany(aStatement, aData)
            conn.commit()

        count += 1
    print('count: ', count)

