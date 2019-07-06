#Import Important Libraries
import re 
import nltk 
nltk.download('stopwords') 
from nltk.corpus import stopwords 
from nltk.stem.porter import PorterStemmer

#Program to remove stock word and clean the data
def clean_data_list(df_column_name):    
    corpus = []        
    for i in range(0, len(df_column_name)):         
        review = re.sub('[^a-zA-Z]', ' ', df_column_name[i])            
        review = review.lower()            
        review = review.split()            
        ps = PorterStemmer()            
        review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]            
        review = ' '.join(review)            
        corpus.append(review)
    return corpus