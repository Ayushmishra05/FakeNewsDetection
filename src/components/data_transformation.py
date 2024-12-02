import gensim.models.word2vec
from src.logging import logger 
import os 
import pandas as pd 
import numpy as np 
from src.entity.artifcats_entity import DataTransformationArtifacts, DataValidationArtifacts
from src.entity.config_entity import TransformationPipelineConfig 
import nltk 
from gensim.utils import tokenize 
import gensim 
import string 
from nltk.corpus import stopwords 
from sklearn.model_selection import train_test_split 


class DataTransformation:
    def __init__(self, valid_arts : DataValidationArtifacts, transformation_config : TransformationPipelineConfig):
        self.config = transformation_config 
        self.artifacts = valid_arts 
    
    @staticmethod
    def get_data(data):
        return pd.read_csv(data)
    def initiate_data_transformation(self):
        try:
            logger.info("Initiating Data Transformation")
            print(self.artifacts.valid_data)
            data = DataTransformation.get_data(self.artifacts.valid_data)
            logger.info("Data Extracted")
            data = self.transform_data(data)
            logger.info("Transformation Completed")
            train_data, test_data = train_test_split(data, random_state = 42)
            os.makedirs(self.config.root_dir, exist_ok=True)
            os.makedirs(self.config.train_dir, exist_ok=True)
            os.makedirs(self.config.test_dir, exist_ok=True)
            logger.info("Saving Train Data and Test Data to CSV ")
            train_data.to_csv(self.config.train_path, header = True, index = False)
            logger.info("Saving Train Data and Test Data to CSV ")
            test_data.to_csv(self.config.test_path, header = True, index = False)
            return DataTransformationArtifacts(
                train_data=self.config.train_path, 
                test_data=self.config.test_path
            )
        except Exception as e:
            raise e 
    
    def transform_data(self , data):
        try:
            logger.info("Inside Transform Data Function")
            nltk.download('punkt')
            nltk.download('stopwords')
            data = data.drop(columns = ['title' , 'subject' , 'date'])
            punctuations = set(string.punctuation)
            stop_words = set(stopwords.words('english'))
            story = [ ]
            for news in data['text']:
                tokenized = tokenize(news.lower())
                story.append([word for word in tokenized if word not in stop_words and word not in punctuations])
            model = gensim.models.Word2Vec(
                window = 3, 
                min_count = 2 
            )
            logger.info("Data has been Tokenized")
            model.build_vocab(story)
            model.train(story, total_examples = model.corpus_count, epochs = model.epochs)
            data['text'] = data['text'].apply(lambda x : self.get_sentence_embedding(x , model).tolist())
            logger.info("Tokenization and Data Modification Completed")
            os.makedirs(self.config.gensim_model, exist_ok = True)
            model.save(self.config.gensim_model_path)
            return data
        except Exception as e:
            raise e
        
    
    def get_sentence_embedding(self,sentence, model):
        try:
            words = sentence.split()
            word_vectors = [ ]

            for word in words:
                if word in model.wv.key_to_index:
                    word_vectors.append(model.wv[word])
                else:
                    word_vectors.append(np.zeros(model.vector_size))
            
            if word_vectors:
                sentence_embedding = np.mean(word_vectors , axis = 0)
            else:
                sentence_embedding = np.zeros(model.vector_size)
            return sentence_embedding
        except Exception as e:
            raise e
    

        
        

        