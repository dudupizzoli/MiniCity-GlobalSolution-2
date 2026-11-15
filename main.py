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
    print("2 - Ver Planos.") #Opção para ver os planos disponíveis e assinar
    print("3 - Consultar notícias e estabelecimentos.") #Submenu para consultar notícias e estabelecimentos por perto, além de buscar por locais
    print("4 - Escrever relatório.") #Submenu para escrever relatórios
    print("5 - Central do usuário.") #Submenu do usuário
    print("6 - Criar JSON.") #Opção para criar um relatório de usuários em JSON
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

        case 3:
            while True:    #Submenu do sistema - trata sobre as consultas dos mapas 
                print("\n======= Menu MiniCity - Mapa =======")
                print("1 - Ver meu local.") # Mostra o local em que o usuário se encontra atualmente
                print("2 - Ver notícias perto de mim.") # Mostra notícias que ocorreram perto do local em que o usuário se encontra atualmente
                print("3 - Ver estabelecimentos e comércios perto de mim.") # Mostra estabelecimentos perto do local em que o usuário se encontra atualmente
                print("4 - Buscar local.") # Busca um local para o usuário ver as notícias
                print("5 - Ver histórico de locais buscados.") # Mostra o histórico de locais que o usuário buscou
                print("6 - Voltar.") #Volta ao menu principal
                try:
                    opcao_mapa = int(input("Digite o número da opção que você deseja: "))
                except ValueError:
                    print("Opção inválida. Digite apenas números.")
                    continue
            
        case 4:
            print("EM DESENVOLVIMENTO")

        case 5:
            while True:    #Submenu do sistema - trata sobre as contas do usuário | Aqui se encontra um CRUD
                print("\n======= Menu MiniCity - Usuário =======")
                print("1 - Conferir conta atual.") #Confere a conta logada atualmente
                print("2 - Logar em outra conta.") #Faz o login em outra conta
                print("3 - Cadastrar nova conta.") #Create
                print("4 - Ver contas cadastradas.") #Read
                print("5 - Procurar conta pelo nome de usuário.")#Read
                print("6 - Editar nome de usuário e email.") #Update
                print("7 - Remover conta.") #Delete
                print("8 - Voltar.") #Volta ao menu principal
                try:
                    opcao_user = int(input("Digite o número da opção que você deseja: "))
                except ValueError:
                    print("Opção inválida. Digite apenas números.")
                    continue
                match opcao_user:
                    case 1:
                        print("\n=== Conta Logada Atualmente ===")
                        print(usuario_atual)

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
                                    print("O login foi efetuado com sucesso!")
                                    print("Agora você está logado com: ", usuario_atual._username)  

                            except ValueError as erro:
                                print("Ocorreu um erro: ", erro)
                    

                    case 3:
                        try:
                            username = validar_texto("Digite seu nome de usuário: ")
                            email = validar_texto("Digite seu email: ")
                            senha = validar_texto("Sua senha precisa conter ao menos 4 caracteres e não pode ter espaços. Digite sua senha: ")
                            validar_credenciais(email, senha)

                            novo_usuario = Usuario(username, senha, email)
                            user_dao.cadastrar_usuario(novo_usuario)
                        except ValueError as erro:
                            print("Ocorreu um erro: ", erro)

                    case 4:
                        usuarios = user_dao.listar_usuarios()
                        if usuarios is None:
                            print("Nenhum usuário cadastrado.")
                        else:
                            for usuario in usuarios:
                                print("\n========================")
                                print("ID do usuário: ", usuario[0])
                                print("Nome de usuário: ", usuario[1])
                                print("Email: ", usuario[3])
                                print("Plano: ", usuario[4])

                    case 5:
                        username_procurado = validar_texto("Digite o Username da conta que você deseja buscar: ")
                        usuario = user_dao.buscar_nome_usuario(username_procurado)
                        if usuario is None:
                            print("Nenhum usuário foi encontrado.")
                        else:
                            print("\n========================")
                            print("ID do usuário: ", usuario[0])
                            print("Nome de usuário: ", usuario[1])
                            print("Email: ", usuario[3])
                            print("Plano: ", usuario[4])  

                    case 6:
                        usuario_editado = validar_texto("Digite o nome do usuário que você deseja editar: ")
                        usuario = user_dao.editar_usuario(usuario_editado)
                        if usuario is None:
                            print("Não foi possível editar o usuário.")
                        else:
                            if usuario[0] == usuario_atual._id_usuario:
                                usuario_atual._username = usuario[1]
                                usuario_atual._email_user = usuario[3]

                            print("\n========================")
                            print("ID do usuário: ", usuario[0])
                            print("Nome de usuário: ", usuario[1])
                            print("Email: ", usuario[3])
                            print("Plano: ", usuario[4])      

                    case 7:
                        usuario_excluido = validar_texto("Digite o nome do usuário que você deseja excluir: ")
                        usuario = user_dao.buscar_nome_usuario(usuario_excluido)
                        if usuario is None:
                            print("Nenhum usuário foi encontrado.")
                        else:
                            print("\n========================")
                            print("ID do usuário: ", usuario[0])
                            print("Nome de usuário: ", usuario[1])
                            print("Email: ", usuario[3])
                            print("Plano: ", usuario[4])  

                            conta_excluida = user_dao.excluir_usuario(usuario_excluido)
                            if conta_excluida and usuario[0] == usuario_atual._id_usuario:
                                print("Sua conta foi excluída. Encerrando sistema...")
                                opcao = 0
                                break                      

                    case 8:
                        print("Voltando ao menu anterior...")
                        break
                    
                    case _:
                        print("Opção inválida. Digite uma opção válida do menu.")

        case 6:
            print("EM DESENVOLVIMENTO")

        case 0:
            print("Encerrando sistema...")
            break
        
        case _:
            print("Opção inválida. Digite uma opção válida do menu.")

