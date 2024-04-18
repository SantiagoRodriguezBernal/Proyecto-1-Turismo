import React, { useState } from "react";
import {Form, Button} from 'react-bootstrap';
import axios from 'axios';

import Tabla from "./tabla";


// Funcion NavbarMarvel
function Analisis () {
    const [archivo, setArchivo] = useState()
    const [review, setReview] = useState('')
    const [resultadoArchivo, setResultadoArchivo] = useState([])
    const [resultadoTexto, setResultadoTexto] = useState([])
    const [mensajeFile, setMensajeFile] = useState(null) 
    const [mensajeText, setMensajeText] = useState(null) 

    function handleFileChange(event) {
        setArchivo(event.target.files[0])
      }
    
      function handleTextChange(event) {
        setReview(event.target.value)
      }
    
    const enviarTexto = (event) => {
        event.preventDefault()
        console.log(review, resultadoTexto)
        prediccionTexto();
    }

    const enviarArchivo = (event) => {
        event.preventDefault()
        console.log(archivo, resultadoArchivo)
        prediccionArchivo();
    }
    async function prediccionArchivo() {

        const url = 'http://localhost:8000/predict';
        const formData = new FormData();
        formData.append('file', archivo);
        formData.append('fileName', archivo.name);
        const config = {
          headers: {
            'content-type': 'multipart/form-data',
          },
        };
        setMensajeFile('Procesando archivo...')
        axios.post(url, formData, config).then((response) => {
          console.log(response.data);   setResultadoArchivo(JSON.parse(response.data)) ; setMensajeFile('Enviado correctamente');
        }); 
    }

    async function prediccionTexto() {

        const url = 'http://localhost:8000/predictText';
        const data = { 'review_es' : review };
        setMensajeText('Procesando texto...')
        axios.post(url, data).then((response) => {
            console.log(response.data);   setResultadoTexto([...resultadoTexto, {review_es: response.data.review_es, sentimiento: response.data.sentimiento}]);  setMensajeText('Enviado correctamente');});
      }
    return (
        <div>
            <div className="jumbotron"  style={{backgroundColor: '#e1e2e1'}}>
                <div className="col 1 border">
                    <Form onSubmit={enviarTexto}>
                        <Form.Group className="mt-3">
                            <Form.Label><b>Analizar un texto</b></Form.Label>
                            <Form.Control type="text" placeholder="Ingresa el texto" id="review" onChange={handleTextChange}/>
                        </Form.Group>
                       <Button className="btn btn-danger" type="submit">
                            Enviar
                        </Button> 
                        <span> {mensajeText}</span>  
                    </Form>
                    <Form onSubmit={enviarArchivo}>
                        <Form.Group className="mt-3">
                            <Form.Label><b>Analizar multiples textos (adjunta un archivo CSV)</b></Form.Label>
                            <Form.Control type="file" text id="archivo" onChange={handleFileChange}/>
                        </Form.Group>
                        <Button className="btn btn-danger" type="submit">
                            Enviar
                        </Button>   
                        <span> {mensajeFile}</span>
                    </Form>
                </div>
            </div> 
            <br></br>
            <ul className="nav nav-tabs" id="myTab" role="tablist">
                    <li className="nav-item">
                        <a className="nav-link active" id="texto-tab" data-toggle="tab" href="#texto" role="tab" aria-controls="texto" aria-selected="true">Resultado texto</a>
                    </li>
                    <li className="nav-item">
                        <a className="nav-link" id="file-tab" data-toggle="tab" href="#file" role="tab" aria-controls="file" aria-selected="false">Resultado Archivo</a>
                    </li>
            </ul>
            <div className="tab-content" id="myTabContent">
                <div className="tab-pane fade show active" id="texto" role="tabpanel" aria-labelledby="texto-tab"> {resultadoTexto.length ? <Tabla resultados={resultadoTexto} /> : null}</div>
            </div>
            <br></br>
            <br></br>
        </div>

    )
}

// Exportar funcion NavbarMarvel para ser visible en otros archivos
export default Analisis;