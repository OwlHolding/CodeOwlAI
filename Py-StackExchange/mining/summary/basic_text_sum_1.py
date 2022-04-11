# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

'''
Use Library 'sumy' to Implement
Four Basic Summary Algorithms:
LSA, LEX_RANK, TEXT_RANK, SUM_BASIC 
'''

LANGUAGE = "english"
SENTENCES_COUNT = 5


def lsa_summary(parser, stemmer, count):
    print('========== LSA ==========')
    summarizer = LsaSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        print(sentence)


def lex_rank_summary(parser, stemmer, count):
    print('========== LEX_RANK ==========')
    summarizer = LexRankSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    for sentence in summarizer(parser.document, count):
        print(sentence)


def text_rank_summary(parser, stemmer, count):
    print('========== TEXT_RANK ==========')
    summarizer = TextRankSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    for sentence in summarizer(parser.document, count):
        print(sentence)


def sum_basic_summary(parser, stemmer, count):
    print('========== SUM_BASIC ==========')
    summarizer = SumBasicSummarizer(Stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    for sentence in summarizer(parser.document, count):
        print(sentence)


if __name__ == "__main__":
    ''' 
    # Test text 1
    text = "Strings are immutable. That means once you've created the String, if another process can dump memory, there's no way (aside from reflection) you can get rid of the data before garbage collection kicks in. \
With an array, you can explicitly wipe the data after you're done with it. You can overwrite the array with anything you like, and the password won't be present anywhere in the system, even before garbage collection. \
So yes, this is a security concern - but even using char[] only reduces the window of opportunity for an attacker, and it's only for this specific type of attack. \
As noted in the comments, it's possible that arrays being moved by the garbage collector will leave stray copies of the data in memory. I believe this is implementation-specific - the garbage collector may clear all memory as it goes, to avoid this sort of thing. Even if it does, there's still the time during which the char[] contains the actual characters as an attack window."
    '''
    
    # Test text 2
    text = "We spend a lot of time thinking about web API design, and we learn a lot from other APIs and discussion with their authors. In the hopes that it helps others, we want to share some thoughts of our own. In this post, we’ll discuss the limitations of the HTTP GET method and what we decided to do about it in our own API.  As a rule, HTTP GET requests should not modify server state. This rule is useful because it lets intermediaries infer something about the request just by looking at the HTTP method.  For example, a browser doesn’t know exactly what a particular HTML form does, but if the form is submitted via HTTP GET, the browser knows it’s safe to automatically retry the submission if there’s a network error. For forms that use HTTP POST, it may not be safe to retry so the browser asks the user for confirmation first.  HTTP-based APIs take advantage of this by using GET for API calls that don’t modify server state. So if an app makes an API call using GET and the network request fails, the app’s HTTP client library might decide to retry the request. The library doesn’t need to understand the specifics of the API call.  The Dropbox API tries to use GET for calls that don’t modify server state, but unfortunately this isn’t always possible. GET requests don’t have a request body, so all parameters must appear in the URL or in a header. While the HTTP standard doesn’t define a limit for how long URLs or headers can be, most HTTP clients and servers have a practical limit somewhere between 2 kB and 8 kB.  This is rarely a problem, but we ran up against this constraint when creating the /delta API call. Though it doesn’t modify server state, its parameters are sometimes too long to fit in the URL or an HTTP header. The problem is that, in HTTP, the property of modifying server state is coupled with the property of having a request body.  We could have somehow contorted /delta to mesh better with the HTTP worldview, but there are other things to consider when designing an API, like performance, simplicity, and developer ergonomics. In the end, we decided the benefits of making /delta more HTTP-like weren’t worth the costs and just switched it to HTTP POST.  HTTP was developed for a specific hierarchical document storage and retrieval use case, so it’s no surprise that it doesn’t fit every API perfectly. Maybe we shouldn’t let HTTP’s restrictions influence our API design too much.  For example, independent of HTTP, we can have each API function define whether it modifies server state. Then, our server can accept GET requests for API functions that don’t modify server state and don’t have large parameters, but still accept POST requests to handle the general case. This way, we’re opportunistically taking advantage of HTTP without tying ourselves to it."

    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    lsa_summary(parser, stemmer, SENTENCES_COUNT)
    lex_rank_summary(parser, stemmer, SENTENCES_COUNT)
    text_rank_summary(parser, stemmer, SENTENCES_COUNT)
    sum_basic_summary(parser, stemmer, SENTENCES_COUNT)
