from ClasseFilmes import *
from ClasseAtores import *
from ClasseCast import *
from ClasseFamosos import *
from ClasseGeneros import *

filmes = TMDB()
atores = Ator()
elenco = Elenco()
famosos = Famosos()
elenco = Elenco()
generos = Genero()



#Atores Favoritos
atores_favoritos = ["Brad Pitt","Angelina Jolie","Jack Nicholson","Robert De Niro","Spencer Tracy","Denzel Washington",
    "Al Pacino",
    "Anthony Hopkins",
    "Tom Hanks",
    "Jason Statham",
]
print("Top 10 Atores Favoritos")
dados_atores = atores.ObterDadosVarios(atores_favoritos)
ApresentarAtores.tabulacao(dados_atores)
AtoresManipulador.salvar_json(dados_atores, 'atores_favoritos.json')
AtoresManipulador.criar_excel(dados_atores, 'atore_filmes.xlsx')

#Filmes favoritos:
titulos = ["The Matrix", "Inception", "Interstellar", "Back to the Future",
           "Intouchables", "WALL·E", "Avengers: Endgame", "The Sixth Sense",
             "Kill Bill: Vol. 1", "Hacksaw Ridge"]

print("Top 10 Filmes Favoritos")
dados_filmes = filmes.obter_detalhes_varios_por_titulos(titulos)
ApresentarFilmes.tabulacao(dados_filmes)
ApresentarFilmes.salvar_json(dados_filmes, 'filmesfavoritos.json')
ApresentarFilmes.criar_excel(dados_filmes, 'dados_filmes.xlsx')

# Obter dados dados de 10 filmes com atores com <primeiro nome>
print("10 filmes com atores com o meu primeiro nome")
first_name = "John"
filmes_atores = atores.ObterFilmesAtores(first_name)
AtoresManipulador.salvar_json(filmes_atores, 'FilmesAtores.json')

#Fotos Atore Favorito:
nome_ator = "Jason Statham"
print(f"As fotos do {nome_ator} serao guardadas")
atores.SalvarFotosAtor(nome_ator)
print(f'Foi criado um documento Word com informacao sobre {nome_ator}')

#Filme preferido com 5 atores pricipais e produtoras:
print('O filme favorito escolhido: Regresso ao Futuro (105):')
elenco_json = elenco.obter_elenco(105)
atores_info = elenco.selecionar_nome_foto_atores(elenco_json)
detalhes_filme = elenco.obter_detalhes_filme(105)
elenco.criar_documento_word(105, elenco_json, detalhes_filme, atores_info)
elenco.converter_docx_para_pdf(str(105), 'Detalhes_do_Filme')

# Obter famosos com o mesmo aniversario assincronamente:
print("A procura por atores famosos com o aniverario em comum foi iniciada")
atores_filtrados = asyncio.run(Famosos().obter_famosos(quantidade=10, mes_dia="05-18"))
for ator in atores_filtrados:
    # (id, name, place_of_birth, popularity, profile_path(foto))
    print(f"ID: {ator['id']}, Nome: {ator['name']}, Local de Nascimento: {ator.get('place_of_birth', 'N/A')}, Popularidade: {ator.get('popularity', 'N/A')}, Foto: {ator['profile_path']}")
    
    with open('10atores.json', 'w', encoding='utf-8') as f:
        json.dump(atores_filtrados, f, ensure_ascii=False, indent=4)

# Generos:
print("Generos Disponiveis")
generos_disponiveis = generos.obter_genero()
for id_genero, nome_genero in generos_disponiveis.items():
    print(f"ID: {id_genero}, Nome: {nome_genero}")