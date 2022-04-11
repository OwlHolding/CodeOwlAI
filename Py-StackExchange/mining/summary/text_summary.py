import basic_text_sum_1 as b1
from utils.textteaser import TextTeaser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
import sys
sys.path.append('..')
sys.path.append('../..')

class Text_summary:
    def __init__(self):
        self.type = 0
        self.sum_sentence_num = 5
        self.lauguage = 'english'

    def text_sum_0(self, text):
        parser = PlaintextParser.from_string(text, Tokenizer(self.lauguage))
        stemmer = Stemmer(self.lauguage)
        b1.lsa_summary(parser, stemmer, self.sum_sentence_num)

    def text_sum_1(self, text):
        parser = PlaintextParser.from_string(text, Tokenizer(self.lauguage))
        stemmer = Stemmer(self.lauguage)
        b1.lex_rank_summary(parser, stemmer, self.sum_sentence_num)

    def text_sum_2(self, text):
        parser = PlaintextParser.from_string(text, Tokenizer(self.lauguage))
        stemmer = Stemmer(self.lauguage)
        b1.text_rank_summary(parser, stemmer, self.sum_sentence_num)

    def text_sum_3(self, text):
        parser = PlaintextParser.from_string(text, Tokenizer(self.lauguage))
        stemmer = Stemmer(self.lauguage)
        b1.sum_basic_summary(parser, stemmer, self.sum_sentence_num)

    def text_sum_4(self, text):
        tt = TextTeaser()
        title = 'title'
        sentences = tt.summarize(title, text, self.sum_sentence_num)
        for sentence in sentences:
            print(sentence)

    def text_sum_5(self, text):
        pass

    def sum_default(self, text):
        print('Text summary type is wrong...')

    def summary(self, type, text):
        self.type = type
        switchDic = {
            0: self.text_sum_0,
            1: self.text_sum_1,
            2: self.text_sum_2,
            3: self.text_sum_3,
            4: self.text_sum_4,
            5: self.text_sum_5
        }
        switchDic.get(type, self.sum_default)(text)

    