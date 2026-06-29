import outline_bajar_articulo_con_comentarios as obacc
import json
import time
from datetime import datetime

def crear_documento(token:str, titulo:str, texto:str, collection_id:str)->str:
    payload_document_dict = {
        "title": titulo,
        "text": texto,
        "collectionId": collection_id,
        "publish": True
    }   
    headers = {
        'Content-Type': "application/json",
        'Authorization': token
    }
    response_text = obacc.intercambio_con_outline("POST","/api/documents.create", payload_document_dict, headers)
    response_dict = json.loads(response_text)
    return response_dict

def list_collections(mi_token:str)->dict:
    payload = {}
    headers = {
    'Content-Type': "application/json",
    'Authorization': mi_token
    }   
    response_text = obacc.intercambio_con_outline("POST","/api/collections.list",payload, headers)
    response_dict = json.loads(response_text)
    return response_dict


