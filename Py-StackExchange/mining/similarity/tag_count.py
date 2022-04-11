import matplotlib.pyplot as plt
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
plt.style.use('ggplot')


class Tag_count:
    def __init__(self):
        self.tag_dict = {}
        self.sorted_tags = {}
        self.pic = 'data/'

    def count_tag(self, filename):
        f = open(filename, 'r')
        for line in f.readlines():
            tags = line.strip().split(';')
            for t in tags:
                if t != '':
                    if t not in self.tag_dict:
                        self.tag_dict[t] = 1
                    else:
                        old = self.tag_dict[t]
                        self.tag_dict[t] = old + 1
        f.close()
        self.sort_android_tags = sorted(
            self.tag_dict.iteritems(), key=lambda asd: asd[1], reverse=False)

    def plot(self, pic_path, num=40):
        data1 = []
        label1 = []
        for pair in self.sort_android_tags[-num:]:
            label1.append(pair[0])
            data1.append(pair[1])
        x_bar = np.arange(len(data1))
        fig = plt.figure(figsize=(9, 9))
        plt.barh(x_bar, data1, color='lightblue', alpha=0.6)
        plt.yticks(x_bar + 0.4, label1)
        plt.grid(axis='x')
        plt.savefig(pic_path)
        plt.show()
