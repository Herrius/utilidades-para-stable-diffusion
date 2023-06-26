
import csv
import json
import requests
import os

def get_star_count(user, repo, headers):
    url = f"https://api.github.com/repos/{user}/{repo}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json = response.json()
        return json['stargazers_count']
    except:
        return 0

# Tu token de acceso personal de GitHub
token = os.getenv('GITHUB')
print(token)
# Los encabezados para la solicitud
headers = {'Authorization': f'token {token}'}

# Descargar los datos JSON
response = requests.get('https://raw.githubusercontent.com/AUTOMATIC1111/stable-diffusion-webui-extensions/master/index.json', headers=headers)

# Asegurarte deque la solicitud fue exitosa
response.raise_for_status()

# Cargar los datos JSON
data = json.loads(response.text)

# Obtener la lista de extensiones
extensions = data['extensions']

# Anexar el recuento de estrellas a cada extensión
for extension in extensions:
    url = extension['url']
    # Separar la URL en partes
    parts = url.split('/')
    # El nombre del usuario es el penúltimo elemento
    user = parts[-2]
    # El nombre del repositorio es el último elemento, sin la extensión .git
    repo = parts[-1].replace('.git', '')
    # Obtener el recuento de estrellas
    stars = get_star_count(user, repo, headers)
    # Añadir el recuento de estrellas a la extensión
    extension['stars'] = stars

# Ordenar las extensiones por la cantidad de estrellas
sorted_extensions = sorted(extensions, key=lambda x: x.get('stars', 0), reverse=True)

# Imprimir los resultados en formato de tabla
print("Nombre de la Extensión\t\t\tEstrellas")
for item in sorted_extensions:
    print(f"{item['name']}\t\t\t{item.get('stars', 'No tiene estrellas')}")

# Guardar los resultados en un archivo CSV
with open('resultados.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Nombre de la Extensión", "Estrellas"])
    for item in sorted_extensions:
        writer.writerow([item['name'], item.get('stars', 'No tiene estrellas')]) 
