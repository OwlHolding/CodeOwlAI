#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import print_function
import os
import sys
import sqlite3
import re

reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append('.')
sys.path.append('..')


def write_data(filename, *contents):
    # if not os.path.exists(filename):
    #     os.system(r"touch {}".format(filename))
    string = ''
    if len(contents) > 1:
        for s in contents:
            string = string + s + ','
    else:
        string = contents[0]
    string += '\n'
    string += '---------------------------------------------\n'
    f = open(filename, 'a+')
    f.write(string)
    f.close()

# 清理body中html标签

def clean_html(html_text):
    pat = re.compile('<[^>]+>', re.S)
    code_pat_str = r'(<pre.*?><code>.*?</code></pre>)'
    body = re.sub('\n', '', html_text)
    code_pat = re.compile(code_pat_str)
    # body = re.sub('\n', '', html_text)
    code = re.findall(code_pat_str, body)
    print('code: ')
    print(code)
    body = code_pat.sub('', body)
    body = pat.sub('', body)
    return body


def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)


def delete_comma(contents):
    return contents.replace(",", ";")


try:
    get_input = raw_input
except NameError:
    get_input = input

user_api_key = get_input(
    "Please enter an API key if you have one (Return for none):")
if not user_api_key:
    user_api_key = 'fAEE*hhUg6RZwKnjsGLYng(('

import stackexchange
so = stackexchange.Site(stackexchange.StackOverflow, app_key=user_api_key)
so.be_inclusive()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        term = get_input('Please provide a search tag:')
    else:
        term = ','.join(sys.argv[1:])

    print('Searching for %s...' % term,)
    sys.stdout.flush()

    qs = so.search(tagged=term, sort='votes', filter='_b')

    android_count = 0
    java_count = 0
    # pat = re.compile('(?<=\>).*?(?=\<)')
    pat = re.compile('<[^>]+>', re.S)
    codePat = r'(<pre><code>.*?</code></pre>)'
    '''
       body_filename : SO question body
       tag_filename : SO question tags
       info_filename : SO all needed info (id, title, views, score, create_date)
    '''
    for q in qs:
        print(q.title, " ", q.view_count)
        # if q.view_count < 5000:
        #     continue
        if android_count > 2000:
            break
        body_filename = ''
        tag_filename = ''
        info_filename = ''
        body = ''
        tag = ''
        q_has_code = '<pre><code>' in q.body

        if 'android' in q.tags:
            # body = re.sub('\n', '', q.body)
            # body = pat.sub('', body)
            body = clean_html(q.body)
            body_filename = '../data/' + term + '_android' + '.txt'
            tag_filename = '../data/' + term + '_android_tag' + '.txt'
            info_filename = '../data/' + term + '_android_info' + '.csv'
            for t in q.tags:
                tag = tag + t + ";"

            if android_count == 0:
                remove_file(body_filename)
                remove_file(tag_filename)
                remove_file(info_filename)
            write_data(info_filename, str(q.id) + ',' + delete_comma(q.title) + ',' +
                       str(q.view_count) + ',' + str(q.score) + ',' + str(q.creation_date) + ',' + str(q_has_code))
            android_count += 1
        if body != '':
            write_data(body_filename, q.title + '\n' + body)
            print(q.id, " ", q.title)
        if tag != '':
            write_data(tag_filename, tag)

        body = ''
        tag = ''
        if 'java' in q.tags:
            # body = pat.sub('', q.body)
            body = clean_html(q.body)
            body_filename = '../data/' + term + '_java' + '.txt'
            tag_filename = '../data/' + term + '_java_tag' + '.txt'
            info_filename = '../data/' + term + '_java_info' + '.csv'
            for t in q.tags:
                tag = tag + t + ";"

            if java_count == 0:
                remove_file(body_filename)
                remove_file(tag_filename)
                remove_file(info_filename)
            write_data(info_filename, str(q.id) + ',' + delete_comma(q.title) + ',' +
                       str(q.view_count) + ',' + str(q.score) + ',' + str(q.creation_date) + ',' + str(q_has_code))
            java_count += 1

        if body != '':
            write_data(body_filename, q.title + '\n' + body)
            print(q.id, " ", q.title)
        if tag != '':
            write_data(tag_filename, tag)
            # question = so.question(q.id)
            # for a in question.answers:
            #     print(a.body, " ", a.question_id, " ", a.score)
            #     print('------------\n')

    print('android_count: ', android_count)
    print('java_count:', java_count)
