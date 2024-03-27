import requests
import json

class Genero:
    def obter_genero(self):
        url = "https://api.themoviedb.org/3/genre/movie/list?language=en-US&api_key=sua_api_key_aqui"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwZGMxMTg3NjU4NjIxNmQ1NWM3ZTQ2Y2EzZjU1ZmJmYiIsInN1YiI6IjY1ZjE3MjFjNmRlYTNhMDE2Mzc4YThjYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mniwNJ0_EVyiz75FjAgZWI2SUFKoTV2A9eci3cpcEhQ"
        }
        response = requests.get(url, headers=headers)
        dados = response.json()

        # Processando os dados para criar um dicionário de gêneros
        generos = {genero['id']: genero['name'] for genero in dados['genres']}
        return generos
 
 