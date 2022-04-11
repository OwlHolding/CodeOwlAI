#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import jieba
import jieba.analyse
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def count_tag(filename):
    f =open(filename,'r')
    tag_dict = {}
    for line in f.readlines():
        tags = line.strip().split(';')
        if len(tags) > 0 and '-----' not in line:
            for t in tags:
                if t != '':
                    if t not in tag_dict:
                        tag_dict[t] = 1
                    else:
                        old = tag_dict[t]
                        tag_dict[t] = old+1
    f.close()
    return tag_dict

def read_doc(filename):
    documents = []
    temp = ''
    f =open(filename,'r')
    for line in f.readlines():
        if '---------------------' in line:
            documents.append(temp)
            temp = ''
            continue
        temp += line.strip()
    return documents

def count_word(docs):
    word_dict = {}
    for line in docs:
        for w in line:
            if w != '' and "'" not in w and '`' not in w:
                if w not in word_dict:
                    word_dict[w] = 1
                else:
                    old = word_dict[w]
                    word_dict[w] = old+1
    return word_dict

def filter_dict(data):
    return {k: v for k, v in data.items() if v > 1}

javatag_filename = '../data/security_java_tag.txt'
java_tags = count_tag(javatag_filename)
sort_java_tags = sorted(java_tags.iteritems(), key = lambda asd:asd[1], reverse = False)[-40:]
data = []
label = []
for pair in sort_java_tags:
    label.append(pair[0])
    data.append(pair[1])
print data
x_bar=np.arange(len(data))
fig = plt.figure(figsize=(9,9))
plt.barh(x_bar, data, color='lightblue',alpha=0.6)
plt.yticks(x_bar+0.4,label)
plt.grid(axis='x')
plt.show()

androidtag_filename = '../data/security_android_tag.txt'
android_tags = count_tag(androidtag_filename)
sort_android_tags = sorted(android_tags.iteritems(), key = lambda asd:asd[1], reverse = False)[-40:]
data1 = []
label1 = []
for pair in sort_android_tags:
    label1.append(pair[0])
    data1.append(pair[1])
print data1
x_bar=np.arange(len(data1))
fig = plt.figure(figsize=(9,9))
plt.barh(x_bar, data1, color='lightblue',alpha=0.6)
plt.yticks(x_bar+0.4,label1)
plt.grid(axis='x')
plt.show()

java_filename = '../data/security_java.txt'
# java_filename = '../data/security_android.txt'
java_document = read_doc(java_filename)
gen_docs = [[w.lower() for w in word_tokenize(text)] 
            for text in java_document]
stop_words = list(set(stopwords.words('english')))
filter_java_docs = [[w for w in text if not w in stop_words and len(w) > 1]
            for text in gen_docs]

# 所有单词统计
java_words = count_word(filter_java_docs)
java_filter_words = filter_dict(java_words)
sort_java_words = sorted(java_filter_words.iteritems(), key = lambda asd:asd[1], reverse = False)
print sort_java_words
data1 = []
label1 = []
for pair in sort_java_words[-40:]:
    label1.append(pair[0])
    data1.append(pair[1])
x_bar=np.arange(len(data1))
fig = plt.figure(figsize=(9,9))
plt.barh(x_bar, data1, color='lightblue',alpha=0.6)
plt.yticks(x_bar+0.1,label1)
plt.grid(axis='x')
plt.show()

