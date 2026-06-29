import outline_bajar_articulo_con_comentarios as obacc
import integrate_comments_to_text as ictt
import outline_crear_documento as ocd
import json
import time
from datetime import datetime

##la clave se pide haciendo click en preferencias->API keys 
##revisar vencimiento de la clave
##el token debe empezar con "Bearer" seguido de un espacio " ", sino falla
with open("PATH/outline_api_key", "r") as f:
    token_crudo = f.read()
    
mi_token = "Bearer " + token_crudo

##Los id de las colecciones fueron extraidos de los liks de la UI cuando se hace click en la colección
##https://gemis-dev.getoutline.com/collection/NOMBRE_DE_MI_COLECCION-ksj6bekR7/recent
## ksj6bekR7 --> va a ser el collection_id
collection_urlid = "9LgrJulWwm"
collection_UUID = "5beaab4b-8263-4fd7-9fb8-237421e8a202"
   
#collection_info = titles_and_ids_in_collection(collection_urlid, mi_token)
#print(list(collection_info.keys()))
#print(list(collection_info.values()))   


#ESTRAER DOCUMENTOS DE UNA COLECCIÓN    
documents = [obacc.descargar_documento_con_comentarios("273604ad-1fb6-4047-b239-edb4577533af",mi_token)]
brownie_tests = documents[0]
#GUARDADO DE DOCUMENTOS DE MANERA LOCAL
obacc.save_documents_to_json(documents, "YOUR_PATHgestion_del_conocimiento_francisco/code/documents_with_comments.json")

#PROCESAMIENTO DE DOCUMENTOS PARA ENVIARLE A LA IA
for document in documents:
    path = "YOUR_PATHgestion_del_conocimiento_francisco/code/outputs_from_tests/" + document.title + "_original.json"
    obacc.save_document_to_json_no_title_no_id(document,path)

#ENVIO DEL ARTÍCULO CON SUS COMENTARIOS
#El código funciona pero está comentado para no usar tokens de la api de chat gpt innecesariamente
#input_path = "YOUR_PATHgestion_del_conocimiento_francisco/code/outputs_from_tests/Brownie_original.json"
#output_path = "YOUR_PATHgestion_del_conocimiento_francisco/code/outputs_from_tests/Brownie_con_comentarios_integrados"
#ictt.integrate_comments_with_openai(input_path,output_path)

#ARMADO DE NUEVO DOCUMENTO
with open("YOUR_PATHgestion_del_conocimiento_francisco/code/outputs_from_tests/Brownie_con_comentarios_integrados", "r") as f:
    articulo_nuevo = f.read()
documento_con_comentarios_integrados = obacc.DocumentoConComentarios(id="",title=brownie_tests.title + "_con_comentarios_integrados ",original_text=articulo_nuevo,comments=[])

#SUBIR EL NUEVO DOCUMENTO QUE INTEGRÓ LOS COMNETARIOS AL CUERPO DE TEXTO
timestamp = time.time()
dt_object = datetime.fromtimestamp(timestamp)
# Convert to string
timestamp_str = dt_object.strftime("%Y-%m-%d %H:%M:%S") 

print(ocd.crear_documento(mi_token, documento_con_comentarios_integrados.title + timestamp_str, documento_con_comentarios_integrados.original_text, collection_UUID))