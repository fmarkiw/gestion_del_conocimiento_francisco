import http.client
import json
from datetime import datetime
import time

##la clave se pide haciendo click en preferencias->API keys 
##revisar vencimiento de la clave
##el token debe empezar con "Bearer" seguido de un espacio " ", sino falla
mi_token = "Bearer CLAVE_ALFANUMÉRICA_LARGA" 

##Los id de las colecciones fueron extraidos de los liks de la UI cuando se hace click en la colección
##https://gemis-dev.getoutline.com/collection/NOMBRE_DE_MI_COLECCION-ksj6bekR7/recent
## ksj6bekR7 --> va a ser el collection_id
collection_id = "COMPLETAR CON EL ID CORRESPONDIENTE!!!!!!!!!!!!!!"
    
##FUNCIONES DE UTILIDAD
def intercambio_con_outline(command:str, url:str,payload:dict,headers:dict) -> json:
    conn = http.client.HTTPSConnection("app.getoutline.com")
    payload_ready = json.dumps(payload)
    conn.request(command, url, payload_ready, headers)
    res = conn.getresponse()
    data = res.read()
    jsoned = json.loads(data)
    return json.dumps(jsoned, indent = 4)
    
def mandar_time_stamp_a_outline(id:str, title:str, token:str) -> str:
    timestamp = time.time()
    dt_object = datetime.fromtimestamp(timestamp)
    # Convert to string
    timestamp_str = dt_object.strftime("%Y-%m-%d %H:%M:%S")  
    # Build a Python dictionary using the variables
    payload_document_dict_to_edit = {
        "id": id,
        "title": title,
        "text": "\n\n" + timestamp_str + " google_sheets_outline.py\n\n",
        "append": True,
        "publish": True,
        "done": True
    }   
    headers = {
        'Content-Type': "application/json",
        'Authorization': mi_token
    }
    return intercambio_con_outline("POST","/api/documents.update", payload_document_dict_to_edit, headers)

def titles_and_ids_in_collection(collection_id:str, mi_token:str)->dict:
    payload_collection_dict = {"id": collection_id}
    headers = {
    'Content-Type': "application/json",
    'Authorization': mi_token
    }   
    response_text = intercambio_con_outline("POST","/api/collections.documents",payload_collection_dict, headers)
    response_dict = json.loads(response_text)
    titles_and_ids = dict()
    for i in range (len(response_dict["data"])):
        title = response_dict["data"][i]["title"]
        id = response_dict["data"][i]["id"]
        titles_and_ids.update({title:id})
    return titles_and_ids
  

#MODIFICAR UNA SERIE DE DOCUMENTOS
collection_info = titles_and_ids_in_collection(collection_id, mi_token)  
for i in range(5):
    for title, id in collection_info.items():
        output= mandar_time_stamp_a_outline(id, title, mi_token)
        time.sleep(5)
   
        

