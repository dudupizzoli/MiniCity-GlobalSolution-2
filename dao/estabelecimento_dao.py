import oracledb
from conexaodb import Conexaodb
import os
from dotenv import load_dotenv

load_dotenv()

class EstabelecimentoDAO:
    def __init__(self):
        self.conexao = Conexaodb(
            usuario=os.getenv("DB_USUARIO"),
            senha=os.getenv("DB_SENHA"),
            host=os.getenv("DB_HOST"),
            porta=os.getenv("DB_PORTA"),
            service_name=os.getenv("DB_SERVICE_NAME")
        )

    def listar_estabelecimentos(self):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return None

        cursor = conn.cursor()
        sql = """select id_estabelecimento, nome_estabelecimento, rua, 
        bairro, link_estabelecimento from estabelecimentos_minicity order by id_estabelecimento"""

        try:
            cursor.execute(sql)
            estabelecimentos = cursor.fetchall()
            if len(estabelecimentos) == 0:
                return None
            else:
                return estabelecimentos

        except oracledb.Error as erro:
            print(f"\nHouve um erro: {erro}")
                
        finally:
            cursor.close()
            conn.close() 