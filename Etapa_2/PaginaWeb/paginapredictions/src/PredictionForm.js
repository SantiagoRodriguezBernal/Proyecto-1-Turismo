import React, { useState } from "react";
import "./PredictionForm.css";
import FileUpload from "./FileUpload";


function PredictionForm() {
  const [textosEspanol, setTextosEspanol] = useState("");
  const [prediction, setPrediction] = useState(null);

  const handlePredictClick = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ Review: textosEspanol }),
      });

      if (response.ok) {
        const result = await response.json();
        setPrediction(result);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleFileUpload = async (file) => {
    try {
      const formData = new FormData();
      formData.append("csv_file", file);
      const response = await fetch("http://127.0.0.1:8000/uploadcsv", {
        method: "POST",
        body: formData,
        redirect: 'follow',
      });

      if (response.ok) {
        // Maneja la respuesta para descargar el archivo resultante
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "predicted_data.csv";
        a.click();
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div>
      <textarea
        placeholder="Textos en español"
        value={textosEspanol}
        onChange={(e) => setTextosEspanol(e.target.value)}
      />
      <button onClick={handlePredictClick}>Predecir</button>
      <FileUpload onFileUpload={handleFileUpload} />
      {prediction !== null && (
        <div>
          <h3>Resultado de la prediccion (con un 50% de precision):</h3>
          <p>El texto tiene una calificacion de: {prediction}</p>
        </div>
      )}
    </div>
  );
}

export default PredictionForm;
