from fastapi import FastAPI, Body
from fastapi .responses import HTMLResponse
app = FastAPI()

#Documentacion con swagger
app.title = "Mi app con fastapi"
app.version = "0.0.1"


movies = [
    {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	},
    {
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	}
]

@app.get("/", tags = ["home"])
def message():
    return HTMLResponse("<h1> Hello world</h1>")


@app.get("/movies", tags = ["movies"])
def get_movies():
    return movies

#parametros de ruta, usando {id}, podemos especificar que ruta y parametros queremos para poder acceder a cierto url
@app.get("/movies/{id}", tags = ["movies"])
def get_movie(id: int):
    for item in movies:
        if item["id"]== id:
            return item
    return []

#cuando no se especifica en la ruta, usamos lo que sonn parametros query
#estos parametros son los que salen con ?en el navegador
@app.get("/movies/", tags = ["movies"])
def get_movies_by_category(category: str):
    # Utilizar una comprensión de lista para verificar la condición en cada diccionario
    resultados = resultados = [d for d in movies if 'category' in d and d['category'] == category]
    
    # Retornar la lista de resultados
    return resultados

#Ponerle el body hace que tome los parametros de un body que se le manda, y no los pide individualmente
@app.post("/movies", tags = ["movies"])
def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    new_movie = {
		"id": id,
		"title": title,
		"overview": overview,
		"year": year,
		"rating": rating,
		"category": category
	}
    movies.append(new_movie)
    return movies
    

@app.put("/movies/{id}", tags = ["movies"])
def update_movie(id: int, title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    for item in movies:
        if item["id"] ==id:
            item["title"] = title
            item["overview"] = overview
            item["year"] = year
            item["rating"] = rating
            item["category"] = category
            return movies
        
	
@app.delete("/movies/{id}", tags = ["movies"])
def delete_movie(id: int):
    for item in movies:
        if item["id"] ==id:
            movies.remove(item)
            return movies