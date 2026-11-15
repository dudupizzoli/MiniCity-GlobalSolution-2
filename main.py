import sys
from models.usuario import Usuario
from models.local import Local
from dao.usuario_dao import UsuarioDAO

user_dao = UsuarioDAO()

def validar_texto(mensagem): #Função para ler texto
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        else:
            print("O campo não pode ficar em branco.")


def ler_inteiro(mensagem): #Função para ler números inteiros
    while True:
        try:
            valor = int(input(mensagem))
            if valor <= 0:
                raise ValueError("O número não pode ser menor ou igual a 0.")
            else:
                return valor
        except ValueError as erro:
            print("Ocorreu um erro: ", erro, ". Digite apenas números válidos.")

def validar_credenciais(email, senha): #Função para validar email e senha colocados pelo usuário
    if len(senha) < 4 or " " in senha:
        raise ValueError("Sua senha precisa ter ao menos 4 caracteres e nenhum espaço.")
    if "@" not in email or len(email) < 8:
        raise ValueError("O email precisa ter @ e não pode ter menos de 8 caracteres.")

usuario_atual = None
login = False
opcao_login = -1

while not login: #Menu de login, permite a criação de uma conta e o login caso o usuário já possua uma conta
    print("\n=======================================")
    print("Bem-vindo à MiniCity!")
    print("Ainda não possui uma conta? Cadastre-se!")
    print("1 - Realizar cadastro.")
    print("Já possui uma conta? Faça o login!")
    print("2 - Login.")
    print("3 - Sair.")
    try:
        opcao_login = int(input("Digite o número da opção que você deseja: "))
    except ValueError:
        print("Opção inválida. Digite apenas números.")
        continue
    match opcao_login:
        case 1:
            try:
                username = validar_texto("Digite seu nome de usuário: ")
                email = validar_texto("Digite seu email: ")
                senha = validar_texto("Sua senha precisa conter ao menos 4 caracteres e não pode ter espaços. Digite sua senha: ")
                validar_credenciais(email, senha)
                novo_usuario = Usuario(username, senha, email)

                if user_dao.cadastrar_usuario(novo_usuario):

                    usuario_atual = user_dao.validar_login(email, senha)
                    if usuario_atual is not None:
                        print("Agora você está logado com: ", usuario_atual._username)     
                        login = True  
            except ValueError as erro:
                print("Ocorreu um erro: ", erro)

        case 2:
                try:
                    email = validar_texto("Digite seu email: ")
                    senha = validar_texto("Digite sua senha: ")
                    validar_credenciais(email, senha)
                    usuario_validado = user_dao.validar_login(email, senha)

                    if usuario_validado is None:
                        raise ValueError("Email ou senha incorretos.")        
                    else: 
                        usuario_atual = usuario_validado
                        login = True
                        print("O login foi efetuado com sucesso!")
                        print("Agora você está logado com: ", usuario_atual._username)  

                except ValueError as erro:
                    print("Ocorreu um erro: ", erro)

        case 3:
            print("Encerrando sistema...")
            sys.exit()
        
        case _:
            print("Opção inválida. Digite uma opção válida do menu.")

opcao = -1

while opcao != 0:
    print("\n===== Menu MiniCity =====")
    print("1 - Conhecer a MiniCity.") #Opção para ver algumas informações a respeito da MiniCity
    print("2 - Consultar notícias e estabelecimentos.") #Submenu para consultar notícias e estabelecimentos por perto, além de buscar por locais
    print("3 - Escrever relatório.") #Submenu para escrever relatórios
    print("4 - Central do usuário.") #Submenu do usuário
    print("5 - Criar JSON.") #Opção para criar um relatório de usuários em JSON
    print("0 - Sair.") #Saída do sistema
    try:
        opcao = int(input("Digite o número da opção que você deseja: "))
    except ValueError:
        print("Opção inválida. Digite apenas números.")
        continue

    match opcao:
        case 1:
            print("Bem-vindo(a) à MiniCity!!! \n A MiniCity é uma startup criada em Novembro de 2026 baseada nos famosos mini mapas de videogames. Temos intenção de ajudar na distribuição de notícias geograficamente relevantes para a população. Focamos em ajudar os usuários a conhecer melhor o seu redor, além de incentivar a prática da cidadania. ")
            print("\nAtualmente, nossos projetos estão voltados para o desenvolvimento de mapas que exibirão notícias, relatórios de cidadãos e estabelecimentos bem avaliados de forma geolocalizada, facilitando o compartilhamento de notícias relevantes para a rotina das pessoas.")
            print("\nAlém de simlesmente exibir notícias, a MiniCity deseja incentivar a participação do cidadão na sociedade. Os usuários poderão publicar relatórios falando sobre ocorrências como alagamentos ou lotações para ajudar outros usuários e moradores da região.")

        case 2:
            print("EM DESENVOLVIMENTO")
            
        case 3:
            print("EM DESENVOLVIMENTO")

        case 4:
            print("EM DESENVOLVIMENTO")

        case 5:
            print("EM DESENVOLVIMENTO")

        case 0:
            print("Encerrando sistema...")
            break
        
        case _:
            print("Opção inválida. Digite uma opção válida do menu.")

