from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

import re
import pickle


model = pickle.load(open('model2.pkl', 'rb'))
vectorizer = pickle.load(open('tfidfvect2.pkl', 'rb'))
ps = PorterStemmer()


def preprocess_text(text):
    final_text = re.sub('[^a-zA-Z]', ' ', text)
    final_text = final_text.lower()
    final_text = final_text.split()
    
    final_text = [ps.stem(word) for word in final_text if not word in stopwords.words('english')]
    final_text = ' '.join(final_text)

    return final_text


def predict(text):
    processed_text = preprocess_text(text)
    vectorized_text = vectorizer.transform([processed_text]).toarray()
    prediction = model.predict(vectorized_text)
    
    return prediction