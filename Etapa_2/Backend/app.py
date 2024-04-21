from io import BytesIO
import tempfile
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


@app.route('/uploadtxt', methods=['POST'])
def upload_txt():
    if 'txt_file' not in request.files:
        return jsonify({'error': 'No se envió ningún archivo'})

    txt_file = request.files['txt_file']

    if txt_file.filename.endswith(".txt"):
        # Leer el archivo de texto línea por línea
        lines = txt_file.readlines()
        
        # Ejemplo de procesamiento de cada línea
        processed_lines = [line.decode().strip() for line in lines]

        # Crear un DataFrame con las líneas procesadas
        df = pd.DataFrame(processed_lines, columns=['Textos_espanol'])

        # Vectorizar los datos de texto
        vectors = vectorizer.transform(df['Textos_espanol'])
        # Realizar las predicciones
        predictions = reg.predict(vectors)
        # Agregar las predicciones al DataFrame
        df['Prediction'] = predictions

        # Crear un archivo temporal para guardar los datos procesados
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
            temp_filename = temp_file.name
            # Escribir los datos procesados en el archivo temporal
            df.to_csv(temp_filename, sep=';', index=False)

        # Devolver el archivo temporal como respuesta
        return send_file(temp_filename, as_attachment=True, mimetype='text/plain')
    else:
        return jsonify({'error': 'El archivo debe tener la extensión .txt'})

    
@app.route('/')
def hello_world():
    try:
        return str("este es el back")
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(port=5000)