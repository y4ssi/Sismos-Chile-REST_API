Sismo-ApiREST
=============================================================
**Api REST** para consultar los ultimos 8 sismos en Chile.
Aplicación hecha bajo el Framework Python **Flask**.

## Descripción

Esta aplicación se conecta con el sitio www.sismos.cl.

## Funcionamiento General

Esta **API REST** tiene la finalidad de entregar los últimos 8 sismos de Chile, esta aplicación para obtener el listado utiliza **Scraping**.

Esta API manda una solicitud GET a https://www.sismos.cl

Luego de realizar la solicitud GET se recibe una página en HTML, esta es parseada
Finalmente, se devuelve un **JSON** con los últimos sismos.

Instalar Dependencias de API REST
---------------------
```
# pip install -r requirements.txt
```
Ejecucion de la API
------------------------------------
```
# python sismo.py
```
Comentarios Generales
------------------------------------

### Ejemplo de consulta de sismos

```
curl http://simos.yasserisa.com/v1/sismos
```
