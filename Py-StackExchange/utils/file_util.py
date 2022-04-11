#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

def read_data(filename):
    documents = []
    temp = ''
    f =open(filename,'r')
    for line in f.readlines():
        if '---------------------' in line:
            documents.append(temp)
            temp = ''
            continue
        temp += line.strip() + ' '
        if line.strip().endswith('##end##'):
            documents.append(temp.replace('##end##',''))
            temp = ''
            continue
    return documents

def read_info(filename):
    documents = []
    
    f =open(filename,'r')
    for line in f.readlines():
        if line.strip() != '' and '---------------------' not in line:
            documents.append(line.strip())
    f.close()
    # print(documents)
    return documents

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
    # string += '---------------------------------------------\n'
    f = open(filename, 'a+')
    f.write(string)
    f.close()

def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

def file_exist(filename):
    print('search file: '+filename)
    return os.path.exists(filename)
