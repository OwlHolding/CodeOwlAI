#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import print_function

import sys
import os
import re
sys.path.append('.')
sys.path.append('..')
import utils.file_util as fu
from xml.dom.minidom import Document

try:
    get_input = raw_input
except NameError:
    get_input = input

user_api_key = get_input(
    "Please enter an API key if you have one (Return for none):")
if not user_api_key:
    user_api_key = 'fAEE*hhUg6RZwKnjsGLYng(('

import stackexchange
import json
site = stackexchange.Site(stackexchange.StackOverflow, app_key=user_api_key)
site.be_inclusive()
xmlfile = 'code.xml'
xml_doc = Document()
post_list = xml_doc.createElement('postlist')
xml_doc.appendChild(post_list)

'''
  fetch SO codes & save in xml file
'''

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


if __name__ == '__main__':
    doc = fu.read_info('../data/android-2000/security_java_info.csv')
    # new_doc = open('../data/security_java_info.csv', 'w')
    index = 0
    fu.remove_file(xmlfile)
    for line in doc:
        # if index > 10:
        #     break

        id = line.split(',')[0]
        question = site.question(int(id))
        print('question: ' + str(question.id))
        code_pat_str = r'(<pre.*?><code>.*?</code></pre>)'
        add_xml_code(question.body, question.id, 0)

        a_has_code = False
        for answer in question.answers:
            code = add_xml_code(answer.body, answer.question_id, answer.id)
            if len(code) > 0:
                a_has_code = True

        line = line + ',' + str(a_has_code) + '\n'
        # new_doc.write(line)
        print(a_has_code)
        index += 1
    with open(xmlfile, 'a+') as f:
        f.write(xml_doc.toprettyxml(indent="\t"))
        f.close()
    # new_doc.close()
