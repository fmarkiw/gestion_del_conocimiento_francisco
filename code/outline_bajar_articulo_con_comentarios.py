import http.client
import json
from datetime import datetime
import time
    
##FUNCIONES DE UTILIDAD
def intercambio_con_outline(command:str, url:str,payload:dict,headers:dict) -> json:
#    conn = http.client.HTTPSConnection("app.getoutline.com")
    conn = http.client.HTTPSConnection("gemis-dev.getoutline.com")
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
        'Authorization': token
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
  
def documents(document_id : str, mi_token : str) ->dict:
    payload_document_dict = {"id": document_id}
    headers = {
    'Content-Type': "application/json",
    'Authorization': mi_token
    }   
    response_text = intercambio_con_outline("POST","/api/documents.info",payload_document_dict, headers)
    response_dict = json.loads(response_text)
    return response_dict

def comments_from_document(document_id : str, mi_token : str) ->dict:
    payload_document_dict = {"documentId": document_id,"includeAnchorText" : True}
    headers = {
    'Content-Type': "application/json",
    'Authorization': mi_token
    }   
    response_text = intercambio_con_outline("POST","/api/comments.list",payload_document_dict, headers)
    response_dict = json.loads(response_text)
    return response_dict

class Comentario:
    def __init__(self, comment: str, anchor_text: str):
        self.comment = comment
        self.anchor_text = anchor_text

    def to_dict(self):
        return {
            "comment": self.comment,
            "anchor_text": self.anchor_text
        }

class DocumentoConComentarios:
    # El id debe ser UUID porque es el que funciona siempre
    def __init__(self, id: str, title: str, original_text: str, comments: list):
        self.id = id
        self.title = title
        self.original_text = original_text
        self.comments = comments

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "original_text": self.original_text,
            "comments": [comment.to_dict() for comment in self.comments]
        }
    def to_dict_no_title_no_id(self):
        return {
            "original_text": self.original_text,
            "comments": [comment.to_dict() for comment in self.comments]
        }
    


def save_documents_to_json(documents: list, filename: str):
    """
    Saves a list of DocumentoConComentarios objects to a JSON file.
    """

    data = [document.to_dict() for document in documents]

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def save_document_to_json_no_title_no_id(document: DocumentoConComentarios, filename: str):
    """
    Saves a list of DocumentoConComentarios objects to a JSON file.
    """

    data = document.to_dict_no_title_no_id()

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        
def extraer_comentarios(id_documento:str,token:str):
    comments_info = comments_from_document(id_documento, token)
    comentarios_de_un_documento = []
    for comment_info in comments_info["data"]:   
        commentario_texto = comment_info["data"]["content"][0]["content"][0]["text"]
        try:
            #Parte del documento al que vino asociado el comentario
            anchor_text = comment_info["anchorText"]
        except:
            #A veces no viene asociado a nada
            anchor_text = ""
        comentario = Comentario(commentario_texto,anchor_text)
        comentarios_de_un_documento.append(comentario)
    return comentarios_de_un_documento
    
            
def descargar_documento_con_comentarios(document_id:str,token:str):
    documento_crudo = documents(document_id,token)
    title = documento_crudo["data"]["title"]
    original_text = documento_crudo["data"]["text"]
    commentarios = extraer_comentarios(document_id,token)
    documento_con_comentarios = DocumentoConComentarios(document_id,title,original_text,commentarios)
    return documento_con_comentarios
