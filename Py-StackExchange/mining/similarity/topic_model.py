import gensim
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import sys
import re

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

class Topic_model:
    def __init__(self):
        self.raw_documents = None
        self.dictionary = None
        self.corpus = None
        self.topic_type = 0
        self.tfidf_type = 0
        self.model = None
        self.topic_num = 15

    def count_topic(self):
        topic_dict = {}
        for index in range(len(self.corpus)):
            topic_id = self.model.get_document_topics(self.corpus[index], minimum_probability=0.1)
            print(index, topic_id)
            for pair in topic_id:
                topic = pair[0]
                if topic not in topic_dict:
                    topic_dict[topic] = 1
                else:
                    old = topic_dict[topic]
                    topic_dict[topic] = old+1
        topic_dict = sorted(topic_dict.iteritems(), key = lambda asd:asd[1], reverse = True)
        return topic_dict

    def tf_idf(self):
        if self.corpus == None or self.dictionary == None:
            print('Please generate model first...')
            return
        tf_idf = gensim.models.TfidfModel(self.corpus)
        self.corpus = tf_idf[self.corpus]
        
    def lsi(self):
        print '\n-------------LSI---------------'
        if self.corpus == None or self.dictionary == None:
            print('Please generate model first...')
            return
        lsi_model = gensim.models.LsiModel(self.corpus, id2word=self.dictionary, num_topics=self.topic_num) 
        return lsi_model
        
    def lda(self):
        print '\n-------------LDA---------------'
        if self.corpus == None or self.dictionary == None:
            print('Please generate model first...')
            return
        lda = gensim.models.LdaModel(corpus=self.corpus, id2word=self.dictionary, num_topics=self.topic_num, passes=20, iterations=100)
        return lda

    def generate_model(self, raw_documents, topic_type, tf_idf_type):
        regex = re.compile('([^\s\w]|_)+')
        self.raw_documents = raw_documents
        gen_docs = [[w.lower() for w in word_tokenize(regex.sub(' ', text).lower())] 
                for text in raw_documents]
        stop_words = list(set(stopwords.words('english')))
        filter_docs = [[w for w in text if not w in stop_words and len(w) > 1 and "'" not in w and "`" not in w and not re.search(r'\d', w)]
                for text in gen_docs]
        self.dictionary = gensim.corpora.Dictionary(filter_docs)
        self.corpus = [self.dictionary.doc2bow(filter_doc) for filter_doc in filter_docs]
        if tf_idf_type == 1:
            self.corpus = self.tf_idf() 
        self.model = None
        if topic_type == 1:
            self.model = self.lsi()
        elif topic_type == 2:
            self.model = self.lda()
        else:
            pass

    def query_similar_question(self, text):
        query_doc = [w.lower() for w in word_tokenize(text)]
        stop_words = list(set(stopwords.words('english')))
        query_filter_doc = [w for w in query_doc if not w in stop_words and len(w) > 1]
        query_doc_bow = self.dictionary.doc2bow(query_filter_doc)
        query_doc_model = self.model[query_doc_bow]
        index = gensim.similarities.MatrixSimilarity(self.corpus)
        sims = index[query_doc_model]
        for index, s in enumerate(sims):
            if s > 0:
                print(str(index) + ': ' +self.raw_documents[index])
        print('--------------------------------------------------------\n')
                


    def get_model(self):
        return self.model

    def print_model(self):
        topic_list = self.model.print_topics(self.topic_num)
        for topic in topic_list:
            pattern = re.compile('\"(.*?)\"')
            topics = pattern.findall(topic[1])
            tStr = ''
            for t in topics:
                tStr = tStr + t + '; '
            print "%s" %(tStr)

    def save_model(self):
        pass
        

    