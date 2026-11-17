import oracledb
from conexaodb import Conexaodb
import os
from dotenv import load_dotenv

load_dotenv()

class LocaisDAO:
    def __init__(self):
        self.conexao = Conexaodb(
            usuario=os.getenv("DB_USUARIO"),
            senha=os.getenv("DB_SENHA"),
            host=os.getenv("DB_HOST"),
            porta=os.getenv("DB_PORTA"),
            service_name=os.getenv("DB_SERVICE_NAME")
        )

    def gravar_local_buscado(self, cidade, bairro):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return False

        cursor = conn.cursor()
        sql = """insert into locais_buscados_minicity (cidade, bairro) 
        values (:cidade, :bairro)"""

        try:
            cursor.execute(sql, cidade=cidade, bairro=bairro)
            conn.commit()

        except oracledb.Error as erro:
            conn.rollback()
            print(f"\nHouve um erro: {erro}")
    
        finally:
            cursor.close()
            conn.close()

    def listar_locais_buscados(self):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return None

        cursor = conn.cursor()
        sql = """select id_local, cidade, bairro from locais_buscados_minicity order by id_local"""

        try:
            cursor.execute(sql)
            historico = cursor.fetchall()
            if len(historico) == 0:
                return None
            else:
                return historico

        except oracledb.Error as erro:
            print(f"\nHouve um erro: {erro}")
                
        finally:
            cursor.close()
            conn.close() 