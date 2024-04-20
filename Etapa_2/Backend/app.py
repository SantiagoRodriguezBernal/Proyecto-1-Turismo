from flask import Flask
from joblib import dump,load
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from num2words import num2words
import re, string, unicodedata
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import stanza
from custom import CustomPreprocessor

app = Flask(__name__)
CustomPreprocessor = CustomPreprocessor()
modelo = load("ModeloReview2.joblib")


@app.route('/')
def hello_world():
    return 'Hello, World!'
