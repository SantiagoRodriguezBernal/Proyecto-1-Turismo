from urllib import request
from flask import Flask, jsonify, send_file, request
from flask_cors import CORS
from joblib import dump, load
import pandas as pd
import dataModel
import joblib
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
import num2words
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import stanza
from custom import CustomPreprocessor
from custom import CustomRegression

app = Flask(__name__)
CORS(app)

# Cargar el modelo y el vectorizador
modelo = load("ModeloReview2.joblib")
reg = modelo["model"].model
vectorizer = modelo["model"].vec

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Obtener los datos del formulario enviado y convertirlos en un objeto DataModel
        data = request.json
        # Vectorizar los datos de entrada
        vectors = vectorizer.transform([data['Textos_espanol']])
        # Realizar la predicción
        prediction = reg.predict(vectors)[0]
        # Convertir la predicción a un tipo compatible con JSON
        prediction = int(prediction)  # o str(prediction)
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/uploadexcel', methods=['POST'])
def upload_excel():
    # Verificar si se envió un archivo
    if 'excel_file' not in request.files:
        return jsonify({'error': 'No se envió ningún archivo'})

    excel_file = request.files['excel_file']

    # Verificar la extensión del archivo
    if excel_file.filename.endswith(".xlsx"):
        # Leer el archivo Excel
        df = pd.read_excel(excel_file)
        # Vectorizar los datos de texto
        vectors = vectorizer.transform(df['texto'])
        # Realizar las predicciones
        predictions = reg.predict(vectors)
        # Agregar las predicciones al DataFrame
        df['prediction'] = predictions
        # Guardar el DataFrame con las predicciones en un nuevo archivo Excel temporal
        temp_filename = 'predicted_data.xlsx'
        df.to_excel(temp_filename, index=False)
        # Devolver el archivo Excel generado como respuesta
        return send_file(temp_filename, as_attachment=True)
    else:
        return jsonify({'error': 'El archivo debe tener la extensión .xlsx'})
    
@app.route('/')
def hello_world():
    try:
        return str("resultado")
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(port=5000)