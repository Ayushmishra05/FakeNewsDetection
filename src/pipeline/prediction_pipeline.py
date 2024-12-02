from src.logging import logger 
import pickle 
import os 
from gensim.models import Word2Vec
from src.constants import VECTORIZED_PATH, PREDICTION_PATH
import nltk
import string
from nltk.corpus import stopwords 
from gensim.utils import tokenize
import numpy as np 




class PredictionPipeline:
    def __init__(self):
        pass 

    def predict(self, data):
        data = self.convert_data(data)
        return data
    

    def convert_data(self, data):
        nltk.download('stopwords')
        nltk.download('punkt')
        punctuations = set(string.punctuation)
        stop_words = set(stopwords.words('english'))
        tokenized = tokenize(data.lower())
        data =[word for word in tokenized if word not in stop_words and word not in punctuations]
        model = Word2Vec.load(VECTORIZED_PATH)
        filtered_words = [word for word in data if word in model.wv.key_to_index]
        with open(PREDICTION_PATH , 'rb') as fp:
            prediction_model = pickle.load(fp)
        if filtered_words:
            sentence_vector = sum(model.wv[word] for word in filtered_words) / len(filtered_words) 
            sentence_vector = sentence_vector.reshape(1, 100)
            return prediction_model.predict(sentence_vector)
          
        else:
            logger.info("No Words in the Vocab")
            return np.array([0])
            


# if __name__ == "__main__":
#     predict = PredictionPipeline()
#     predict.predict("Hello This is Ayush ")

        