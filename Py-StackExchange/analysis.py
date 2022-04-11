#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import utils.file_util as fu
from mining.similarity.topic_model import Topic_model
from mining.similarity.word_count import Word_count
from mining.similarity.tag_count import Tag_count
from mining.summary.text_summary import Text_summary
from common import Config
import sys
import argparse

try:
    get_input = raw_input
except NameError:
    get_input = input

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("term", help="your search tag")
    parser.add_argument(
        "--topic", help="choose topic model: 0 - no; 1 - lsa; 2 - lda", type=int)
    parser.add_argument(
        "--tfidf", help="use tfidf vertor: 0 - no;1 - yes", type=int)
    parser.add_argument(
        "--word", help="choose word count: 1 - wordcount&cloud;", type=int)
    parser.add_argument(
        "--tag", help="choose tag count: 1 - tagcount;", type=int)
    parser.add_argument("--summary", help="choose summary algorithm: 0 - LSA; 1 - LEX_RANK; \
    2 - TEXT_RANK; 3 - SUM_BASIC; 4 - TextTeaser; 5 - MMR", type=int)
    args = parser.parse_args()
    print(args)
    # check data is prepared
    term = args.term
    config = Config.get_default_config(term)
    if not fu.file_exist(config.Q_OUTPUT_FILE):
        print(config.Q_OUTPUT_FILE + ' File not exists...')
        sys.exit()

    raw_documents = fu.read_data(config.Q_OUTPUT_FILE)
    '''
        First Analysis Words and Tags 
    '''
    if args.word == 1:
        # count words
        wc = Word_count()
        wc.extract_words(raw_documents)
        # wc.plot(config.WORDCOUNT_PIC)
    if args.tag == 1:
        # count tags
        if not fu.file_exist(config.T_OUTPUT_FILE):
            print(config.T_OUTPUT_FILE + ' File not exists...')
        else:
            tc = Tag_count()
            tc.count_tag(config.T_OUTPUT_FILE)
            # tc.plot(config.TAGCOUNT_PIC)

    '''
        Then Analysis Questions' Topic
    '''
    tm = Topic_model()
    if args.topic != None:
        tm.generate_model(raw_documents, args.topic, args.tfidf)
        model = tm.get_model()          # Return Gensim Topic Model
        tm.print_model()
    # Use topic model to find similar questions
    text = get_input('Input query text(input "##" to stop):')
    while(text != "##"):
        tm.query_similar_question(text)
        text = get_input('Input query text(input "##" to stop):')


    '''
        Finally Summary the Question Body
    '''
    if args.summary == None or args.summary > 7:
        print("No Summary")
    else:
        ts = Text_summary()
        ts.summary(args.summary, 'test')
