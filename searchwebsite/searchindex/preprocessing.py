# import Stemmer
from nltk.stem import *
import re 

# The file 'datasets/stopwords_en.txt' contains a list of stopwords - one per line.
with open(r"searchindex\datasets\stopwords_en.txt", encoding="utf8") as f:
    enStopWords = set(f.read().splitlines())

# Initialze the SnowballStemmer
# enStemmer = Stemmer.Stemmer('english')
enStemmer = PorterStemmer()

def preprocess_line_en(line: str) -> list[str]:
    # Convert to lower case
    tokens = line.lower()
    
    # Split into tokens with no punctuation
    tokens = re.split("[^\w]", tokens)
    
    # Remove empty strings and stop words and apply the stemmer
    tokens = [enStemmer.stem(x) for x in tokens if x and x not in enStopWords]
    
    # Return the tokens
    return tokens