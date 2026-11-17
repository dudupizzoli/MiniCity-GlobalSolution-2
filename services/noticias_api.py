import os
import requests
from dotenv import load_dotenv

load_dotenv()

class NoticiaAPI:
    URL = "https://newsapi.org/v2/everything"

    def buscar_noticias(self, bairro, cidade, quantidade=5):
        termo = f'"{bairro}" AND "{cidade}"' if bairro else f'"{cidade}"'
        chave = os.getenv("NEWS_API_CHAVE")
        if chave is None or chave == "":
            print("\nNão foi possível realizar a busca de notícias pois a chave da API não foi localizada.")
            return None

        parametros = {
            "q": termo,
            "language": "pt",
            "sortBy": "publishedAt",
            "pageSize": quantidade,
            "apiKey": os.getenv("NEWS_API_CHAVE"),
        }
        try:
            resposta = requests.get(self.URL, params=parametros, timeout=10)
            dados = resposta.json()
            if dados.get("status") != "ok":
                print(f"\nHouve um erro com a API: {dados.get('message')}")
                return None
            
            if len(dados["articles"]) == 0:
                return None
            
            return dados["articles"]
        
        except requests.exceptions.RequestException as erro:
            print(f"\nNão foi possível acessar a API: {erro}")
            return None

        except ValueError as erro:
            print(f"\nA resposta da API veio em um formato inesperado: {erro}")
            return None