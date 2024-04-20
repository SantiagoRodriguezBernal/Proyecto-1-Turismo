from flask import Flask
from joblib import dump,load
import joblib
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from num2words import num2words
import re, string, unicodedata
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import stanza
from custom import CustomPreprocessor
from custom import CustomRegression

app = Flask(__name__)


modelo = joblib.load("ModeloReview2.joblib")
reg = modelo["model"].model
vectorizer = modelo["model"].vec
vectors = vectorizer.transform(['Me gusto demasiado volveria a ir'])
predict = reg.predict(vectors)
resultado = predict[0]
print(resultado)

@app.route('/')
def hello_world():
    try:
        return str(resultado)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run()
