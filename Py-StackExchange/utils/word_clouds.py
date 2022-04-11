from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

# text = 'The United States shall guarantee to every State in this Union a Republican Form of Government baby baby baby'
d = path.dirname(__file__)
text = open(path.join(d, '../data/security_android.txt')).read()
stop_words = set(stopwords.words('english'))
stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '@', '#', 'rt', 'amp', 'realdonaldtrump', 'http', 'https', '/', '://', '_', 'co', 'trump', 'donald', 'makeamericagreatagain'])

wordcloud = WordCloud(
        stopwords = stop_words,
        max_words = 1024,
        max_font_size = 100).generate(text)
plt.figure(figsize=(12,12))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
