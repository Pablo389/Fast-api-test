from fastapi import FastAPI, Body, Path, Query, Depends, HTTPException, Request
from fastapi .responses import HTMLResponse, JSONResponse
from pydantic import BaseModel,Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer


app = FastAPI()
#https://fastapi.tiangolo.com/es/
#Documentacion con swagger
app.title = "Mi app con fastapi"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)

Base.metadata.create_all(bind=engine)


class User(BaseModel):
    email:str
    password:str

    class Config:
        schema_extra = {
            "example": {
                "email" : "admin@gmail.com",
                "password" : "admin"
            }
        }

class Movie(BaseModel):
    id: Optional[int] = None
    #Validacion de parametros de ruta
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=100)
    year: int = Field(le=2022)
    rating:float = Field(default=10, ge=1, le=10)
    category:str = Field(default='Categoría', min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi película",
                "overview": "Descripción de la película",
                "year": 2022,
                "rating": 9.8,
                "category" : "Acción"
            }
        }


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

@app.post("/login", tags= ["login"])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token = create_token(user.dict())
        return JSONResponse(status_code= 200, content=token)

@app.get("/movies", tags = ["movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#parametros de ruta, usando {id}, podemos especificar que ruta y parametros queremos para poder acceder a cierto url
@app.get("/movies/{id}", tags = ["movies"], response_model= Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#cuando no se especifica en la ruta, usamos lo que sonn parametros query
#estos parametros son los que salen con ?en el navegador
@app.get("/movies/", tags = ["movies"], response_model=List[Movie])
#Validacion de parametros query
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
      return JSONResponse(status_code=404, content={"message": "Movie not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#Ponerle el body hace que tome los parametros de un body que se le manda, y no los pide individualmente
@app.post("/movies", tags = ["movies"], response_model= dict, status_code=201)
def create_movie(movie: Movie) ->dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"})
    
#En estos dos faltaria poner dict como retorno, pero vamos dejandolo asi a ver que pasa
@app.put("/movies/{id}", tags = ["movies"])
def update_movie(id: int, movie: Movie):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"})
        
	
@app.delete("/movies/{id}", tags = ["movies"])
def delete_movie(id: int):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado la película"})