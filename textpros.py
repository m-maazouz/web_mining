import re,csv
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
import pandas as pd
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from wordcloud import WordCloud
import arabic_reshaper
from bidi.algorithm import get_display

class textPros:

    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stop_words = stopwords.words('arabic')
        with open("arabic_stop_words.txt","r", newline="",encoding="utf-8") as f:        
            for l in f:
                l = re.sub(r"\n+","",l)
                self.stop_words.append(l)

    def text_pros(self, text):
        # result =[]
        # for line in text:
        #     line = self.tokenize_regex_punct_keep(line)
        #     result.append(line)
        # return " ".join(result)
        return self.tokenize_regex_punct_keep(text)
    
    def tokenize_regex_punct_keep(self, text):
        #delete all non words exept html tags
        text = re.sub('[^\w<>]',' ',text)
        #delete javascript tags
        text =re.sub('< *script*>.*?< *script*>',' ',text)
        #delete all html tags
        text = re.sub('<.*?>',' ',text)
        #delete numbers 
        text = re.sub("[0-9><,]+"," ",text)
        #delete reteur a la ligne
        text = re.sub(r"\n+"," ",text)
        #replace multiple spaces with one space
        text = re.sub(r"\s+"," ",text)
        #transfer text to lowercase
        text = text.lower() 
        # tokenaze text
        tokens = re.split(" ", text)
        # Remove stop words        
        tokens = [word for word in tokens if word not in self.stop_words]
        
        stems = [self.stemmer.stem(t) for t in tokens]
        return " ".join(stems)
    def plot(self, csv_path = "topics.csv"):
        df = pd.read_csv(csv_path)
        # print(len(df['type'].unique()))
        for article_type in df['field'].unique():
            comments = df[df['field']==article_type]['processing_comment_text']
            all_comments = " ".join(comments)
            all_comments = get_display(arabic_reshaper.reshape(all_comments))

            tokens = [[token for token in doc.lower().split() ] for doc in comments]
            
            # print(tokens)
            dict = Dictionary(tokens)
            corpus_doc2bow_vectors = [dict.doc2bow(tok_doc) for tok_doc in tokens]
            # tfidf_model = TfidfModel(corpus_doc2bow_vectors, id2word=dict, normalize=False)
            tfidf_model = TfidfModel(corpus_doc2bow_vectors)
            corpus_tfidf_vectors = tfidf_model[corpus_doc2bow_vectors[0]]

            # data = arabic_reshaper.reshape(f.read())
            # data = get_display(data) # add this line
            
            # Get terms from the dictionary and pair with weights
            # weights = {dict[pair[0]]: pair[1] for pair in corpus_tfidf_vectors}
            weights = {get_display(arabic_reshaper.reshape(dict[pair[0]])): pair[1] for pair in corpus_tfidf_vectors}
            # Initialize the word cloud
            # print(weights)
            wc = WordCloud(
                font_path='arial',
                background_color="white",
                mode='RGB',
                max_words=2000,
                width = 1024,
                height = 720,
                stopwords = self.stop_words
            )

            # # Generate the cloud
            # wc.generate_from_frequencies(weights)
            wc.generate(all_comments)

            # Save the could to a file
            wc.to_file("word_cloud.png")

            plt.title(article_type)
            plt.imshow(wc)
            plt.axis("off")
            plt.show()
            # break

# textPros().plot()
            
