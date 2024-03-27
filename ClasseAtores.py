import requests
import json
import openpyxl
import os
import requests
from PIL import Image
from io import BytesIO
from ClasseGeneros import Genero


class Ator:  # atores por nome

    def ObterDadosAtores(self, nome):
        url = f"https://api.themoviedb.org/3/search/person?query={nome}&include_adult=false&language=en-US&page=1"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwZGMxMTg3NjU4NjIxNmQ1NWM3ZTQ2Y2EzZjU1ZmJmYiIsInN1YiI6IjY1ZjE3MjFjNmRlYTNhMDE2Mzc4YThjYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mniwNJ0_EVyiz75FjAgZWI2SUFKoTV2A9eci3cpcEhQ",
        }
        response = requests.get(url, headers=headers)
        return response.json()

    def ObterDadosNomeExato(self, nome):  # atores por nome exato e resultados
        atores = self.ObterDadosAtores(nome=nome)
        for a in atores["results"]:
            if a["name"] == nome:
                a["id"] = a["id"]
                return a

    def ObterDadosVarios(self, atores):  # dados de varios atores
        resultado = {}
        for a in atores:
            a = self.ObterDadosNomeExato(a)
            if a is not None:
                resultado[a["name"]] = a
        return resultado

    def ObterFilmesAtores(self, nome, max_atores=10):  # filmes de 10 atores diferentes com o mesmo primeiro nome
        genero = Genero()
        mapeamento_generos = genero.obter_genero()
        filmes = []
        pagina = 1
        UrlBase = "https://image.tmdb.org/t/p/w500"
        while len(filmes) < max_atores:
            url = f"https://api.themoviedb.org/3/search/person?query={nome}&include_adult=false&language=en-US&page={pagina}"
            headers = {
                "accept": "application/json",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwZGMxMTg3NjU4NjIxNmQ1NWM3ZTQ2Y2EzZjU1ZmJmYiIsInN1YiI6IjY1ZjE3MjFjNmRlYTNhMDE2Mzc4YThjYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mniwNJ0_EVyiz75FjAgZWI2SUFKoTV2A9eci3cpcEhQ",
            }
            response = requests.get(url, headers=headers).json()
            for ator in response["results"]:
                if ator["name"].lower().startswith(nome.lower() + " "):
                    filme = next((item for item in ator.get("known_for", []) if item["media_type"] == "movie"),None,)
                    if filme and len(filmes) < max_atores:
                        filme_genres = [mapeamento_generos.get(genre_id, "Desconhecido") for genre_id in filme.get("genre_ids", [])]
                        full_poster_path = f"{UrlBase}{filme.get('poster_path', '')}" if filme.get('poster_path') else 'N/A'
                        filmes.append(
                            {
                                "id": filme["id"],
                                "original_title": filme["original_title"],
                                "genres": filme_genres,
                                "vote_average": filme.get("vote_average", 0),
                                "vote_count": filme.get("vote_count", 0),
                                "poster_path": full_poster_path,
                                "overview": filme.get("overview", ""),
                            })
            pagina += 1
            if ( pagina > response["total_pages"]or not response["results"] or len(filmes) >= max_atores):
                break
        return filmes

    def FotosAtor(self, id_ator):
        url = f"https://api.themoviedb.org/3/person/{id_ator}/images"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwZGMxMTg3NjU4NjIxNmQ1NWM3ZTQ2Y2EzZjU1ZmJmYiIsInN1YiI6IjY1ZjE3MjFjNmRlYTNhMDE2Mzc4YThjYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mniwNJ0_EVyiz75FjAgZWI2SUFKoTV2A9eci3cpcEhQ",
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        caminhos = [perfil["file_path"] for perfil in data.get("profiles", [])]
        return caminhos

    def SalvarFotosAtor(self, nome_ator):
        dados_ator = self.ObterDadosNomeExato(nome_ator)
        if not dados_ator:
            print(f"Ator '{nome_ator}' não encontrado.")
            return

        id_ator = dados_ator["id"]
        caminhos_fotos = self.FotosAtor(id_ator)
        if not caminhos_fotos:
            print(f"Nenhuma foto encontrada para o ator '{nome_ator}'.")
            return
        pasta = os.path.join(os.getcwd(), nome_ator.replace(" ", "_"))
        os.makedirs(pasta, exist_ok=True)
        base_url = "https://image.tmdb.org/t/p/original"

        for i, caminho in enumerate(caminhos_fotos):
            url_completa = base_url + caminho
            resposta = requests.get(url_completa)
            if resposta.status_code == 200:
                path_imagem = os.path.join(pasta, f"{nome_ator}_{i}.jpg")
                with open(path_imagem, "wb") as f:
                    f.write(resposta.content)
                print(f"Foto Guardada: {path_imagem}")
            else:
                print(f"Erro ao baixar a foto {url_completa}")


class ApresentarAtores:
    def tabulacao_filmes(filmes):
        print(
            f"{'Título':<30}{'ID':<10}{'Generos':<50}{'Voto Médio':<15}{'Votos':<10}{'Poster'}"
        )
        print("-" * 180)
        for filme in filmes:
            titulo = filme["original_title"]
            generos = ", ".join(filme["genres"])
            id_filme = filme["id"]
            voto_medio = filme["vote_average"]
            contagem_votos = filme["vote_count"]
            link_poster = (
                f"https://image.tmdb.org/t/p/w1280{filme.get('poster_path', 'N/A')}"
            )
            print(
                f"{titulo:<30}{id_filme:<10}{generos:<50}{voto_medio:<15}{contagem_votos:<10}{link_poster}"
            )

    def tabulacao(dados):
        print(f"{'Nome':<0}{'ID':<10}{'Link do Perfil'}")
        print("-" * 60)
        for ator in dados.values():
            nome = ator["name"]
            id_ator = ator["id"]
            link_perfil = (
                f"https://image.tmdb.org/t/p/w1280{ator.get('profile_path', 'N/A')}"
            )
            print(f"{nome:<20}{id_ator:<10}{link_perfil}")


class AtoresManipulador:
    def salvar_json(dados, nome_arquivo):
        with open(nome_arquivo, "w") as arquivo:
            json.dump(dados, arquivo, indent=2)

    def criar_excel(dados, nome_arquivo):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Atores"
        ws.append(["Nome", "ID", "Foto do Perfil"])
        for nome, ator in dados.items():
            profile_path = ator.get("profile_path", "N/A")
            if profile_path != "N/A":
                profile_path = f"https://image.tmdb.org/t/p/w1280{profile_path}"
            ws.append([ator["name"], ator["id"], profile_path])
        wb.save(nome_arquivo)

