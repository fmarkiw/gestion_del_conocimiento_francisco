import re

# Read file
with open("/home/dash/Escritorio/UTN/Proyecto/gestion_del_conocimiento_francisco/articulos_para_subir_a_outline/brownie", "r") as f:
    text = f.read()

# Replace newline characters with PPP
new_text = text.replace("\.\n", "PPP")

# Write result
with open("/home/dash/Escritorio/UTN/Proyecto/gestion_del_conocimiento_francisco/articulos_para_subir_a_outline/brownie_texto_procesado", "w") as f:
    f.write(new_text)
