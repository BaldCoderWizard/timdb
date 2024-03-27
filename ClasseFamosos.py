import aiohttp
import asyncio

class Famosos:
    BASE_URL = "https://api.themoviedb.org/3"
    HEADERS = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwZGMxMTg3NjU4NjIxNmQ1NWM3ZTQ2Y2EzZjU1ZmJmYiIsInN1YiI6IjY1ZjE3MjFjNmRlYTNhMDE2Mzc4YThjYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mniwNJ0_EVyiz75FjAgZWI2SUFKoTV2A9eci3cpcEhQ"
    }

    async def obter_detalhes_ator(self, session, id):
        async with session.get(f"{self.BASE_URL}/person/{id}?language=en-US", headers=self.HEADERS) as response:
            if response.status == 200:
                return await response.json()
            return {}

    async def obter_famosos(self, quantidade, mes_dia):
        async with aiohttp.ClientSession() as session:
            atores = []
            page = 1
            while len(atores) < quantidade:
                print(f'\rA procurar na pagina {page}...', end='')
                params = {'language': 'en-US', 'page': page}
                async with session.get(f"{self.BASE_URL}/person/popular", headers=self.HEADERS, params=params) as response:
                    data = await response.json()
                    tasks = []
                    for pessoa in data['results']:
                        task = asyncio.create_task(self.obter_detalhes_ator(session, pessoa['id']))
                        tasks.append(task)
                    
                    detalhes_atores = await asyncio.gather(*tasks)
                    for detalhes in detalhes_atores:
                        if 'birthday' in detalhes and detalhes['birthday'] and detalhes['birthday'][5:10] == mes_dia:
                            profile_path = f"https://image.tmdb.org/t/p/w1280{detalhes.get('profile_path', '')}" if detalhes.get('profile_path') else 'N/A'
                            atores.append({
                                'id': detalhes['id'],
                                'name': detalhes['name'],
                                'place_of_birth': detalhes.get('place_of_birth', 'N/A'),
                                'popularity': detalhes.get('popularity', 'N/A'),
                                'profile_path': profile_path
                            })
                            if len(atores) == quantidade:
                                break
                    page += 1
            print("\nProcura completa.")
            return atores

