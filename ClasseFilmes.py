import requests
import json
from openpyxl import Workbook


class TMDB:
    BASE_URL = "https://api.themoviedb.org/3"
    HEADERS = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwZGMxMTg3NjU4NjIxNmQ1NWM3ZTQ2Y2EzZjU1ZmJmYiIsInN1YiI6IjY1ZjE3MjFjNmRlYTNhMDE2Mzc4YThjYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mniwNJ0_EVyiz75FjAgZWI2SUFKoTV2A9eci3cpcEhQ"
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
    
    def _fazer_requisicao(self, endpoint):
        full_url = f"{self.BASE_URL}/{endpoint}"
        response = self.session.get(full_url)
        response.raise_for_status()
        return response.json()

    def obter_dados_filme(self, titulo):
        endpoint = f"search/movie?query={titulo}&include_adult=false&language=en-US&page=1"
        return self._fazer_requisicao(endpoint)
    
    def obter_dados_filme_exato(self, titulo):
        filmes = self.obter_dados_filme(titulo=titulo)
        for filme in filmes.get("results", []):
            if filme.get('original_title') == titulo:
                return filme
            
    def obter_dados_varios(self, titulos):
        resultado = {}
        for titulo in titulos:
            filme = self.obter_dados_filme_exato(titulo)
            if filme is not None:
                resultado[titulo] = filme
        return resultado

    def obter_detalhes(self, movie_id):
        endpoint = f"movie/{movie_id}?language=en-US"
        return self._fazer_requisicao(endpoint)
            
    def obter_detalhes_varios(self, movie_ids):
        resultado = {}
        for movie_id in movie_ids:
            detalhes = self.obter_detalhes(movie_id)
            if detalhes:
                resultado[movie_id] = detalhes
        return resultado
    
    def obter_detalhes_varios_por_titulos(self, titulos):
        dados_filmes = self.obter_dados_varios(titulos)
        ids_filmes = [(filme['id']) for filme in dados_filmes.values()]
        detalhes_filmes = self.obter_detalhes_varios(ids_filmes)
        return detalhes_filmes
    
class ApresentarFilmes:
    def tabulacao(dados):
        print(f"{'ID':<10}{'IMDB ID':<15}{'Title':<30}{'Release Date':<15}{'Poster Link':<50}{'Homepage'}")
        print("-" * 130)
        for filme in dados.values():
            id_filme = filme.get('id', 'N/A')
            imdb_id = filme.get('imdb_id', 'N/A')
            title = filme.get('title', 'N/A')
            release_date = filme.get('release_date', 'N/A')
            poster_link = f"https://image.tmdb.org/t/p/w1280{filme.get('poster_path', '')}" if filme.get('poster_path') else 'N/A'
            homepage = filme.get('homepage', 'N/A')
            print(f"{id_filme:<10}{imdb_id:<15}{title:<30}{release_date:<15}{poster_link:<50}{homepage}")

    @staticmethod
    def salvar_json(dados, caminho_arquivo):
        dados_para_salvar = []
        for filme in dados.values():
            dados_para_salvar.append({
                'ID': filme.get('id', 'N/A'),
                'IMDB ID': filme.get('imdb_id', 'N/A'),
                'Title': filme.get('title', 'N/A'),
                'Release Date': filme.get('release_date', 'N/A'),
                'Poster Link': f"https://image.tmdb.org/t/p/w1280{filme.get('poster_path', '')}" if filme.get('poster_path') else 'N/A',
                'Homepage': filme.get('homepage', 'N/A')
            })
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(dados_para_salvar, arquivo, ensure_ascii=False, indent=4)

    @staticmethod
    def criar_excel(dados_filmes, caminho_excel):
        wb = Workbook()
        ws = wb.active
        ws.append(['ID', 'IMDB ID', 'Title', 'Release Date', 'Poster Link', 'Homepage'])
        for filme in dados_filmes.values():
            ws.append([
                filme.get('id', 'N/A'),
                filme.get('imdb_id', 'N/A'),
                filme.get('title', 'N/A'),
                filme.get('release_date', 'N/A'),
                f"https://image.tmdb.org/t/p/w1280{filme.get('poster_path', '')}" if filme.get('poster_path') else 'N/A',
                filme.get('homepage', 'N/A')
        ])
        wb.save(caminho_excel)