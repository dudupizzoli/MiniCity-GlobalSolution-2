import oracledb
from conexaodb import Conexaodb
from models.usuario import Usuario
import os
from dotenv import load_dotenv

load_dotenv()

class UsuarioDAO:
    def __init__(self):
        self.conexao = Conexaodb(
            usuario=os.getenv("DB_USUARIO"),
            senha=os.getenv("DB_SENHA"),
            host=os.getenv("DB_HOST"),
            porta=os.getenv("DB_PORTA"),
            service_name=os.getenv("DB_SERVICE_NAME")
        )

    def cadastrar_usuario(self, usuario):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return False

        username = usuario._username
        senha = usuario._senha_user
        email = usuario._email_user
        assinatura = usuario._assinatura

        cursor = conn.cursor()
        sql = """insert into usuarios_minicity (username, senha, email, assinatura) 
        values (:username, :senha, :email, :assinatura)"""

        try:
            cursor.execute(sql,
                username = username,
                senha = senha,
                email = email,
                assinatura = assinatura)
            conn.commit()

            cursor.execute("select id_usuario from usuarios_minicity where email = :email", email = email)
            linha = cursor.fetchone()
            if linha is not None:
                usuario._id_usuario = linha[0]

            print("Cadastro realizado com sucesso!")
            return True

        except oracledb.Error as erro:
            conn.rollback()
            print(f"\nHouve um erro: {erro}")
            return False
    
        finally:
            cursor.close()
            conn.close()

    def listar_usuarios(self):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return None

        cursor = conn.cursor()
        sql = """select id_usuario, username, senha, email, assinatura from usuarios_minicity order by id_usuario"""

        try:
            cursor.execute(sql)
            usuarios = cursor.fetchall()
            if len(usuarios) == 0:
                return None
            else:
                return usuarios

        except oracledb.Error as erro:
            print(f"\nHouve um erro: {erro}")
                
        finally:
            cursor.close()
            conn.close()   

    def buscar_nome_usuario(self, username):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return None
        
        cursor = conn.cursor()
        sql = """select id_usuario, username, senha, email, assinatura from usuarios_minicity where username = :username"""

        try:
            cursor.execute(sql, username =username)
            usuario = cursor.fetchone()
            if usuario is None:
                return None
            else:
                return usuario              

        except oracledb.Error as erro:
            print(f"\nHouve um erro: {erro}")
                        
        finally:
            cursor.close()
            conn.close()

    def editar_usuario(self, nome_usuario):    
        usuario = self.buscar_nome_usuario(nome_usuario)

        if usuario is None:
            return None

        else:

            senha = input("Digite a senha da conta a ser editada: ").strip()

            if senha == usuario[2]:

                username = input(f"Seu nome de usuário atual é: {usuario[1]}, caso não queira mudá-lo, aperte enter. Digite seu novo nome de usuário: ").strip()
                email = input(f"Seu email atual é: {usuario[3]}, caso não queira mudá-lo, aperte enter. Digite seu novo email: ").strip()

                if username == '':
                    username = usuario[1]
                
                if email == '':
                    email = usuario[3]

                if "@" not in email or len(email) < 8:
                    print("O email precisa ter @ e não pode ter menos de 8 caracteres.")
                    return None

                conn = self.conexao.conectar()
                if conn is None:
                    print("Erro ao conectar ao Oracle.")
                    return None

                cursor = conn.cursor()
                sql = """update usuarios_minicity 
                        set username = :username, 
                        email = :email 
                        where username = :nome_usuario 
                        """

                try:
                    cursor.execute(sql, username=username, email=email, nome_usuario=nome_usuario)
                    conn.commit()
                    print("Usuário editado com sucesso!")

                    return self.buscar_nome_usuario(username)
                except oracledb.Error as erro:
                    conn.rollback()
                    print(f"\nHouve um erro: {erro}")
                finally:
                    cursor.close()
                    conn.close()

            else:
                print("Senha incorreta. Não foi possível editar o usuário.")
                return None

    def excluir_usuario(self, username):
        usuario = self.buscar_nome_usuario(username)
        if usuario is None:
            print("Nenhum usuário foi encontrado.")
            return False
        
        confirmacao = input("A exclusão de uma conta é uma ação perigosa e potencialmente irreversível. Você realmente deseja excluir esta conta? (S para Sim/N para Não): ").upper().strip()
        if confirmacao == "N":
            print("A exclusão foi cancelada com sucesso!")
            return False
        
        elif confirmacao == "S":
            senha = input("Digite a senha da conta a ser excluída: ").strip()

            if senha == usuario[2]:
                conn = self.conexao.conectar()
                if conn is None:
                    print("Erro ao conectar ao Oracle.")
                    return False

                cursor = conn.cursor()
                sql = """delete from usuarios_minicity where username = :username"""

                try:
                    cursor.execute(sql, username=username)
                    conn.commit()
                    print("A conta foi excluída com sucesso!")
                    return True
                except oracledb.Error as erro:
                    conn.rollback()
                    print(f"\nHouve um erro: {erro}")
                    return False

                finally:
                    cursor.close()
                    conn.close()

            else:
                print("Senha incorreta. Não foi possível excluir o usuário.")
                return False
        else:
            print("Digite apenas S ou N.")
            return False

    def validar_login(self, email, senha):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return None
        
        cursor = conn.cursor()
        sql = """
            select id_usuario, username, senha, email, assinatura from usuarios_minicity
            where email = :email and senha = :senha
            """

        try:
            cursor.execute(sql, {"email": email, "senha": senha})
            usuario_validado = cursor.fetchone()

            if usuario_validado is None:
                return None

            usuario = Usuario(username=usuario_validado[1], senha_user=usuario_validado[2], email_user=usuario_validado[3], 
                              assinatura=usuario_validado[4], id_usuario=usuario_validado[0])

            return usuario

        except oracledb.Error as erro:
            print(f"\nHouve um erro: {erro}")
            return None
        
        finally:
            cursor.close()
            conn.close()

    def alterar_plano(self, id_usuario, assinatura):
        conn = self.conexao.conectar()
        if conn is None:
               print("Erro ao conectar ao Oracle.")
               return False
        
        cursor = conn.cursor()

        sql = """update usuarios_minicity 
        set assinatura = :assinatura
        where id_usuario = :id_usuario"""

        try:
            cursor.execute(sql, assinatura = assinatura, id_usuario = id_usuario)
            conn.commit()
            print("Plano alterado com sucesso!")

        except oracledb.Error as erro:
            conn.rollback()
            print(f"\nHouve um erro: {erro}")
        finally:
            cursor.close()
            conn.close()