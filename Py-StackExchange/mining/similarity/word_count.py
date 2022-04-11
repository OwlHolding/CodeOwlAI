import matplotlib.pyplot as plt
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
plt.style.use('ggplot')


class Word_count:
    def __init__(self):
        self.document = None
        self.sorted_words = None

    def extract_words(self, document):
        gen_docs = [[w.lower() for w in word_tokenize(text)]
                    for text in document]
        stop_words = list(set(stopwords.words('english')))
        self.document = [[w for w in text if not w in stop_words and len(w) > 1]
                         for text in gen_docs]
        java_words = self.count_word()
        self.sorted_words = sorted(
            java_words.iteritems(), key=lambda asd: asd[1], reverse=False)

    def count_word(self):
        word_dict = {}
        for line in self.document:
            for w in line:
                if w != '' and "'" not in w and '`' not in w:
                    if w not in word_dict:
                        word_dict[w] = 1
                    else:
                        old = word_dict[w]
                        word_dict[w] = old + 1
        return word_dict

    def plot(self, pic_path, num=40):
        data1 = []
        label1 = []
        for pair in self.sorted_words[-num:]:
            label1.append(pair[0])
            data1.append(pair[1])
        x_bar = np.arange(len(data1))
        fig = plt.figure(figsize=(9, 9))
        plt.barh(x_bar, data1, color='lightblue', alpha=0.6)
        plt.yticks(x_bar + 0.1, label1)
        plt.grid(axis='x')
        plt.savefig(pic_path)
        plt.show()
