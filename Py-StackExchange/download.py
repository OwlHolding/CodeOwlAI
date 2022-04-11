#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import print_function
import os
import sys
import re
import utils.file_util as fu
from common import Config
from xml.dom.minidom import Document
import argparse
global code
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append('.')
sys.path.append('..')
try:
    get_input = raw_input
except NameError:
    get_input = input
user_api_key = get_input(
    "Please enter an API key if you have one (Return for none):")

import stackexchange
so = stackexchange.Site(stackexchange.StackOverflow, app_key=user_api_key)
so.be_inclusive()
xml_doc = Document()
post_list = xml_doc.createElement('postlist')

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


def add_xml_code(body, qid, aid):
    code_pat_str = r'(<pre.*?><code>[\s\S]*?</code></pre>)'
    pat = re.compile('<[^>]+>', re.S)
    code = re.findall(code_pat_str, body)
    post = xml_doc.createElement('post')
    post.setAttribute('qid', str(qid))
    post.setAttribute('aid', str(aid))
    post_list.appendChild(post)

    index = 0
    for c in code:
        code_node = xml_doc.createElement('code')
        code_node.setAttribute('id', str(index))

        c = pat.sub('', c)
        code_text = xml_doc.createTextNode(c)
        print(c)
        code_node.appendChild(code_text)
        post.appendChild(code_node)
        index += 1
    return code


def download_question(config):
    qs = so.search(tagged=config.TERM, sort='votes', filter='_b')
    count = 0
    for q in qs:
        if count > 10:
            break
        print(q.title, " ", q.view_count)
        tag = ''
        for t in q.tags:
            tag = tag + t + ";"
        fu.write_data(config.T_OUTPUT_FILE, tag)
        body = q.body
        # One Question is endwith ‘##end##’
        fu.write_data(config.Q_OUTPUT_FILE, q.title + '\n' + body + '##end##')
        q_has_code = '<pre><code>' in q.body
        fu.write_data(config.QINFO_OUTPUT_FILE, str(q.id) + ',' + q.title.replace(",", ";") + ',' +
                      str(q.view_count) + ',' + str(q.score) + ',' + str(q.creation_date) + ',' + str(q_has_code))
        count += 1
    print('question number: ' + str(count))


'''
    Fetch Answers based on the question info file
    1. get codes in answers currently and save in .xml
'''


def download_answer(config):
    doc = fu.read_info(config.QINFO_OUTPUT_FILE)
    fu.remove_file(config.CODE_XML)
    xml_doc.appendChild(post_list)
    code = ''
    for line in doc:
        id = line.split(',')[0]
        question = so.question(int(id))
        print('question: ' + str(question.id))
        add_xml_code(question.body, question.id, 0)
        for answer in question.answers:
            code += str(answer.body) + '##splitID##' + str(answer.question_id) + '##splitAnswer##'
    with open(config.A_OUTPUT_FILE, 'w') as f:
        f.write(code)
        f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("term", help="your search tag")
    parser.add_argument(
        "--type", help="choose download type: 1 - only questions; 2 - questions & answers)", type=int)
    args = parser.parse_args()

    if args.type != '1' and args.type != '2':
        print('\nDownload_type is wrong...')

    config = Config.get_default_config(args.term)
    fu.remove_file(config.Q_OUTPUT_FILE)
    fu.remove_file(config.T_OUTPUT_FILE)
    fu.remove_file(config.A_OUTPUT_FILE)
    print('Searching for %s...' % args.term,)
    sys.stdout.flush()

    download_question(config)
    
    download_answer(config)
