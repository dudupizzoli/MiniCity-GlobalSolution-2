import oracledb
from conexaodb import Conexaodb
import os
from dotenv import load_dotenv

load_dotenv()

class RelatorioDAO:
    def __init__(self):
        self.conexao = Conexaodb(
            usuario=os.getenv("DB_USUARIO"),
            senha=os.getenv("DB_SENHA"),
            host=os.getenv("DB_HOST"),
            porta=os.getenv("DB_PORTA"),
            service_name=os.getenv("DB_SERVICE_NAME")
        )

    #FAZER ESSE DAO
    #Talvez juntar a opção de ver os planos e o "sobre" em uma opção "Geral"