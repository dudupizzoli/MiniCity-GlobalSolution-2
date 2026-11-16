import os
import requests
from dotenv import load_dotenv

load_dotenv()

class NoticiaAPI:
    URL = "https://newsapi.org/v2/everything"

    def buscar_noticias(self, bairro, cidade, quantidade=5):
        termo = f'"{bairro}" AND "{cidade}"' if bairro else f'"{cidade}"'
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