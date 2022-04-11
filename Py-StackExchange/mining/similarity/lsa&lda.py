import gensim
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import sys
import re

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

reload(sys)
sys.setdefaultencoding('utf-8')

def read_data(filename):
#     documents = ["I'm taking the show on the road.",
#                  "My socks are a force multiplier.",
#                  "I am the barber who cuts everyone's hair who doesn't cut their own.",
#                  "Legend has it that the mind is a mad monkey.",
#                  "I make my own fun."
    # ----------------------------------------------------------------
    # read stackoverflow data
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
        

def count_topics(model,corpus):
    topic_dict = {}
    for index in range(len(corpus)):
        topic_id = model.get_document_topics(corpus[index], minimum_probability=0.1)
        print(index, topic_id)
        for pair in topic_id:
            topic = pair[0]
            if topic not in topic_dict:
                topic_dict[topic] = 1
            else:
                old = topic_dict[topic]
                topic_dict[topic] = old+1
    topic_dict = sorted(topic_dict.iteritems(), key = lambda asd:asd[1], reverse = True)
    print topic_dict

def tf_idf(corpus, query_text):
    tf_idf = gensim.models.TfidfModel(corpus)
    sims = gensim.similarities.Similarity('./', tf_idf[corpus], num_features=len(dictionary))

    query_doc = [w.lower() for w in word_tokenize(query_text)]
    query_filter_doc = [w for w in query_doc if not w in stop_words and len(w) > 1]
    query_doc_bow = dictionary.doc2bow(query_filter_doc)
    query_doc_tf_idf = tf_idf[query_doc_bow]
    return tf_idf[corpus]

def lsi(corpus, query_text):
    print '\n-------------LSI---------------'
    topic_num = 15
    lsi_model = gensim.models.LsiModel(corpus, id2word=dictionary, num_topics=topic_num) 
    sims = gensim.similarities.Similarity('Similarity-LSI-index', lsi_model[corpus], num_features=len(dictionary))

    topic_list = lsi_model.print_topics(topic_num)
    index = 0
    for topic in topic_list:
        pattern = re.compile('\"(.*?)\"')
        topics = pattern.findall(topic[1])
        tStr = ''
        for t in topics:
            tStr = tStr + t + '; '
        print "%s" %(tStr)
        index += 1

    query_doc = [w.lower() for w in word_tokenize(query_text)]
    query_filter_doc = [w for w in query_doc if not w in stop_words and len(w) > 1]
    query_doc_bow = dictionary.doc2bow(query_filter_doc)
    query_doc_lsi = lsi_model[query_doc_bow]

def lda_model(corpus,dictionary):
    print '\n-------------LDA---------------'
    topic_num = 15
    lda = gensim.models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=topic_num, passes=20, iterations=100)
    topic_list = lda.show_topics(topic_num)
    index = 0
    for topic in topic_list:
        pattern = re.compile('\"(.*?)\"')
        topics = pattern.findall(topic[1])
        tStr = ''
        for t in topics:
            tStr = tStr + t + '; '
        print "%s" %(tStr)
        index += 1
       # print topicStr
        
    count_topics(lda, corpus)
    return lda
        #     print(lda.show_topic(id[0], topn=10))
            # print(lda.get_topic_terms(id[0], topn=10))

def get_model(raw_document, topic_type, tf_idf_type):
    regex = re.compile('([^\s\w]|_)+')
    gen_docs = [[w.lower() for w in word_tokenize(regex.sub('', text).lower())] 
            for text in raw_documents]
    stop_words = list(set(stopwords.words('english')))
    filter_docs = [[w for w in text if not w in stop_words and len(w) > 1 and "'" not in w and "`" not in w and not re.search(r'\d', w)]
            for text in gen_docs]
    dictionary = gensim.corpora.Dictionary(filter_docs)
    corpus = [dictionary.doc2bow(filter_doc) for filter_doc in filter_docs]
    if tf_idf_type == 1:
        corpus = tf_idf(corpus, query_text)  
    model = None
    if topic_type == 1:
        lsi(corpus, query_text)
    elif topic_type == 2:
        model = lda_model(corpus, dictionary)
    else:
        pass
    


def print_segment():
        print('--------------------\n')

if __name__ == '__main__':
    # Input Document File Name
    filename = ''
    if len(sys.argv) < 2:
        filename = raw_input('Please provide a filename:')
    elif len(sys.argv) > 2:
        print('too many args')
        sys.exit(0)
    else:
        filename = sys.argv[1]

    raw_documents = read_data(filename)
    print("Number of documents:",len(raw_documents))
    regex = re.compile('([^\s\w]|_)+')
    porter_stemmer = PorterStemmer()
    gen_docs = [[w.lower() for w in word_tokenize(regex.sub('', text).lower())] 
            for text in raw_documents]

    stop_words = list(set(stopwords.words('english')))
    # and "'" not in w
    # porter_stemmer.stem(w) 
    filter_docs = [[w for w in text if not w in stop_words and len(w) > 1 and "'" not in w and "`" not in w and not re.search(r'\d', w)]
            for text in gen_docs]

    dictionary = gensim.corpora.Dictionary(filter_docs)
    print("Number of words in dictionary:",len(dictionary))
    corpus = [dictionary.doc2bow(filter_doc) for filter_doc in filter_docs]
    print_segment()
    
    query_text = "Socks are a force for good."
    corpus_tfidf = tf_idf(corpus, query_text)
    lsi(corpus, query_text)
    lsi(corpus_tfidf, query_text)

    lda_model(corpus,dictionary)
    lda_model(corpus_tfidf, dictionary)

    tfidf_dict = {}
    for line in list(corpus_tfidf):
        line = sorted(dict(line).iteritems(), key = lambda asd:asd[1], reverse = True)
        line = line[0:len(line)/3]
        for pair in line:
            word = dictionary.get(pair[0])
            if word not in tfidf_dict:
                tfidf_dict[word] = 1
            else:
                old = tfidf_dict[word]
                tfidf_dict[word] = old+1
    tfidf_dict = sorted(tfidf_dict.iteritems(), key = lambda asd:asd[1], reverse = False)
    data1 = []
    label1 = []
    for pair in tfidf_dict[-40:]:
        label1.append(pair[0])
        data1.append(pair[1])
    x_bar=np.arange(len(data1))
    fig = plt.figure(figsize=(9,9))
    plt.barh(x_bar, data1, color='lightblue',alpha=0.6)
    plt.yticks(x_bar+0.1,label1)
    plt.grid(axis='x')
    plt.show()





