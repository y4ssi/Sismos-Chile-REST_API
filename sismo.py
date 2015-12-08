# -*- coding: utf-8 -*-

# Importamos librerías necesarias
import requests
import re
from flask import Flask, jsonify
import os
import json

app = Flask(__name__)


@app.errorhandler(405)
def page_not_found(e):
    '''
    Function: page_not_found
    Summary: En caso de usar un método diferente al GET, mostramos error
    Attributes:
        @param (e):exceptions
    Returns: json response
    '''
    response = jsonify({'error': 'Metodo HTTP no permitido'})
    response.status_code = 405
    return response


@app.route('/v1/sismos', methods=['GET'])
def consulta_ultimos_sismos_chile():
    '''
    Function: consulta_ultimos_sismos_chile
    Summary: 
    Examples: GET HTTP/1.1 /v1/sismos
    Attributes:
    Returns: json response
    '''
    url_consulta = ('https://www.sismos.cl/')
    # Mandamos una solicitud GET a la pagina de consulta de
    # Sismos
    r = requests.get(url_consulta)
    '''
    Recibimos la respuesta del servidor (Pagina HTML) y verificamos la 
    actividad de sismos. Si la consulta es efectiva parseamos el texto
    HTML para buscar los ultimos sismos
    '''

    if '<table style="font-size: small; font-family: sans-serif;">' in r.text:
        sismos = re.findall(('<table style="font-size: small; font-family: sans-serif;">'
                             '(.*?)</tr>\n</table>'),
                                 r.text, re.DOTALL
                                 )
        lugares = re.findall(('Permanent Link to '
                             '(.*?)">'),
                                 r.text, re.DOTALL
                                 )
        if sismos:
            lista = []
            for key,sismo in enumerate(sismos):
                lista_json = {}
                preliminar = re.findall(('<th style="text-align:left">Preliminar:</th>\n<td>'
                             '(.*?)</td>'),
                                 sismo, re.DOTALL
                                 )
                magnitud = re.findall(('<th style="text-align:left">Magnitud:</th>\n<td>'
                             '(.*?)</td>'),
                                 sismo, re.DOTALL
                                )
                profundidad = re.findall(('<th style="text-align:left">Profundidad:</th>\n<td>'
                             '(.*?)</td>'),
                                 sismo, re.DOTALL
                                 )
                hora = re.findall(('<th style="text-align:left">Hora cerca del Epicentro:</th>\n<td>'
                             '(.*?)</td>'),
                                 sismo, re.DOTALL
                                 )
                lista_json["Preliminar"] = preliminar[0]
                lista_json["Magnitud"] = magnitud[0]
                lista_json["Profundidad"] = profundidad[0]
                lista_json["Hora"] = hora[0]
                lista_json["Lugar"] = lugares[key]
                lista.append(lista_json)
            # Devolvemos los sismos de Chile
            return jsonify(Chile=[e for e in lista])

    # En caso de no obtener los sismos devolvemos error
    else:
        response = jsonify({'error': ('Ups, algo salio mal')})
        response.status_code = 404
        return response

# Inicializamos un servidor web en el puerto 80 (puerto por defecto 5000)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port, debug=True)

