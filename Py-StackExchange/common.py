class Config:
    @staticmethod
    def get_default_config(term):
        config = Config()
        config.TERM = term
        config.Q_OUTPUT_FILE = 'data/question_' + term + '.txt'
        config.QINFO_OUTPUT_FILE = 'data/question_info_' + term + '.txt'
        config.A_OUTPUT_FILE = 'data/answer_' + term + '.txt'
        config.T_OUTPUT_FILE = 'data/tag_' + term + '.txt'
        config.TOPIC_FILE = 'data/topic.txt'
        config.CODE_XML = 'data/code.xml'
        config.WORDCLOUD_PIC = 'data/image/'+term+'_wordcloud.png'
        config.WORDCOUNT_PIC = 'data/image/'+term+'_wordcount.png'
        config.TAGCOUNT_PIC = 'data/image/'+term+'_tagcount.png'
        config.WORDVEC_PIC = 'data/image/'+term+'_wordvec.png'
        return config

    def __init__(self):
        self.TERM = ''
        self.Q_OUTPUT_FILE = ''
        self.QINFO_OUTPUT_FILE = ''
        self.A_OUTPUT_FILE = ''
        self.T_OUTPUT_FILE = ''
        self.TOPIC_FILE = ''
        self.CODE_XML = ''
        self.WORDCLOUD_PIC = ''
        self.WORDCOUNT_PIC = ''
        self.TAGCOUNT_PIC = ''
        self.WORDVEC_PIC = ''
