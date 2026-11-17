import oracledb
from dao.conexaodb import Conexaodb
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

    def fazer_relatorio(self, id_usuario, relatorio, endereco): # Lembrar de inverter a ordem de endereço e relatório qnd chamar isso
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return False

        cursor = conn.cursor()
        sql = """insert into relatorios_minicity (texto, endereco, id_usuario) 
        values (:texto, :endereco, :id_usuario)"""

        try:
            cursor.execute(sql,
                           texto = relatorio,
                           endereco = endereco, 
                           id_usuario = id_usuario)
            conn.commit()
            print("Relatório enviado com sucesso!")

        except oracledb.Error as erro:
            conn.rollback()
            print(f"\nHouve um erro: {erro}")
    
        finally:
            cursor.close()
            conn.close() 

    def listar_relatorios(self):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return None

        cursor = conn.cursor()

        sql = """
            select id_relatorio, texto, endereco
            from relatorios_minicity
            order by id_relatorio
        """

        try:
            cursor.execute(sql)
            relatorios = cursor.fetchall()

            if len(relatorios) == 0:
                return None
            else:
                return relatorios

        except oracledb.Error as erro:
            print(f"\nHouve um erro: {erro}")
        
        finally:
            cursor.close()
            conn.close()

    def buscar_id_relatorio(self, id_relatorio):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return None
        
        cursor = conn.cursor()
        sql = """select id_relatorio, texto, endereco, id_usuario from relatorios_minicity where id_relatorio = :id_relatorio"""

        try:
            cursor.execute(sql, id_relatorio = id_relatorio)
            relatorio = cursor.fetchone()
            if relatorio is None:
                return None
            else:
                return relatorio              

        except oracledb.Error as erro:
            print(f"\nHouve um erro: {erro}")
                        
        finally:
            cursor.close()
            conn.close()

    def editar_relatorio(self, id_relatorio):    
        relatorio = self.buscar_id_relatorio(id_relatorio)

        if relatorio is None:
            return None

        else:

            endereco = input(f"O endereço atual do relatório é: {relatorio[2]}. \nCaso não queira alterar o endereço, aperte enter. Digite o novo endereço do relatório: ").strip()
            if endereco == "":
                endereco = relatorio[2]
            if len(endereco) > 200:
                print("O endereço não pode conter mais do que 200 caracteres.")
                return None

            texto = input("Caso não queira alterar o texto do relatório, aperte enter. Digite o novo texto do relatório: ").strip()
            if texto == "":
                texto = relatorio[1]
            if len(texto) > 400:
                print("O relatório não pode conter mais do que 400 caracteres.")
                return None
            
            conn = self.conexao.conectar()
            if conn is None:
                print("Erro ao conectar ao Oracle.")
                return None

            cursor = conn.cursor()
            sql = """update relatorios_minicity 
                    set texto = :texto,
                    endereco = :endereco
                    where id_relatorio = :id_relatorio 
                    """

            try:
                cursor.execute(sql, texto=texto, endereco=endereco, id_relatorio=id_relatorio)
                conn.commit()
                print("Relatório editado com sucesso!")

                return self.buscar_id_relatorio(id_relatorio)
            
            except oracledb.Error as erro:
                conn.rollback()
                print("Houve um erro: ", erro)
            finally:
                cursor.close()
                conn.close()

    def excluir_relatorio(self, id_relatorio):
        relatorio = self.buscar_id_relatorio(id_relatorio)

        if relatorio is None:
            return None

        else:

            confirmacao = input("Você realmente deseja excluir este relatório? (S para Sim/N para Não): ").upper().strip()
            if confirmacao == "N":
                print("A exclusão foi cancelada com sucesso!")
                return False
            elif confirmacao == "S":

                conn = self.conexao.conectar()
                if conn is None:
                    print("Erro ao conectar ao Oracle.")
                    return False

                cursor = conn.cursor()
                sql = """delete from relatorios_minicity where id_relatorio = :id_relatorio"""

                try:
                    cursor.execute(sql, id_relatorio=id_relatorio)
                    conn.commit()
                    print("O relatório foi excluído com sucesso!")
                except oracledb.Error as erro:
                    conn.rollback()
                    print("Houve um erro: ", erro)
                finally:
                    cursor.close()
                    conn.close()

            else:
                print("Digite apenas S ou N.")