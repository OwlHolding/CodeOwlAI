#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from gensim.models import word2vec
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import gensim
import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import TSNE
import sys
import re
# 引入日志配置
import logging

reload(sys)
sys.setdefaultencoding('utf-8')

def read_doc_2_sen(filename):
    documents = []
    temp = ''
    f =open(filename,'r')
    for line in f.readlines():
        if '---------------------' in line:
            continue
        temp += line.strip()
    with open('./w2v_sentence.txt', 'w') as f2:
        f2.write(temp)
    f.close()
    f2.close()

def read_data(filename):
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

def display_closestwords_tsnescatterplot(model, word):
    
    arr = np.empty((0,200), dtype='f')
    word_labels = [word]

    # get close words
    close_words = model.similar_by_word(word,topn=20)
    
    # add the vector for each of the closest words to the array
    arr = np.append(arr, np.array([model[word]]), axis=0)
    for wrd_score in close_words:
        wrd_vector = model[wrd_score[0]]
        word_labels.append(wrd_score[0])
        arr = np.append(arr, np.array([wrd_vector]), axis=0)
        
    # find tsne coords for 2 dimensions
    tsne = TSNE(n_components=2, random_state=0)
    np.set_printoptions(suppress=True)
    Y = tsne.fit_transform(arr)

    x_coords = Y[:, 0]
    y_coords = Y[:, 1]
    # display scatter plot
    plt.scatter(x_coords, y_coords)

    for label, x, y in zip(word_labels, x_coords, y_coords):
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
    plt.xlim(x_coords.min()+0.00005, x_coords.max()+0.00005)
    plt.ylim(y_coords.min()+0.00005, y_coords.max()+0.00005)
    plt.show()

def tsne_plot(model):
    "Creates and TSNE model and plots it"
    labels = []
    tokens = []

    for word in model.wv.vocab:
        tokens.append(model[word])
        labels.append(word)
    
    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)

    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])
        
    plt.figure(figsize=(12, 12)) 
    for i in range(len(x)):
        plt.scatter(x[i],y[i])
        plt.annotate(labels[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
    plt.show()
 
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

'''
    model training... 
'''
# sentences = word2vec.Text8Corpus('text8')
raw_documents = read_data('../../data/security_android.txt')
print("Number of documents:",len(raw_documents))
regex = re.compile('([^\s\w]|_)+')
gen_docs = [[w.lower() for w in word_tokenize(regex.sub('', text).lower())] 
            for text in raw_documents]
stop_words = list(set(stopwords.words('english')))
filter_docs = [[w for w in text if not w in stop_words and len(w) > 1 and "'" not in w and "`" not in w]
            for text in gen_docs]

# read_doc_2_sen('../../data/security_java.txt')
# java: min_count = 15; android: min_count = 20
model= word2vec.Word2Vec(size=200, window=20, min_count=10, workers=4)
model.build_vocab(filter_docs)
model.train(gen_docs, total_examples = model.corpus_count, epochs = model.iter)
# sentences = word2vec.LineSentence('w2v_sentence.txt')
# model = word2vec.Word2Vec(sentences, size=200)
# model.save('text8.model')
# model.save('java.model')
model.save('android.model')

'''
    show model...
'''
model1 = word2vec.Word2Vec.load('android.model')
# print model1['computer']
# print model1.most_similar(positive=['woman', 'king'], negative=['man'], topn=1)
# print model1.similarity('woman', 'man')
display_closestwords_tsnescatterplot(model1, 'keystore')
display_closestwords_tsnescatterplot(model1, 'certificate')
tsne_plot(model1)




