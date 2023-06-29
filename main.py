from fastapi import FastAPI, Body
from fastapi .responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

#Documentacion con swagger
app.title = "Mi app con fastapi"
app.version = "0.0.1"

class Movie(BaseModel):
    id: Optional[int] = None
    title: str
    overview: str
    year: int
    rating: float
    category: str


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
def create_movie(movie: Movie):
    #Verificar que usar dict sea la mejor opcion
    movies.append(movie.dict())
    return movies
    

@app.put("/movies/{id}", tags = ["movies"])
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item["id"] ==id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
            return movies
        
	
@app.delete("/movies/{id}", tags = ["movies"])
def delete_movie(id: int):
    for item in movies:
        if item["id"] ==id:
            movies.remove(item)
            return movies