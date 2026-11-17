#Importações
import sys
from models.usuario import Usuario
from models.local import Local
from dao.usuario_dao import UsuarioDAO
from dao.relatorio_dao import RelatorioDAO
from dao.estabelecimento_dao import EstabelecimentoDAO
from dao.locais_dao import LocaisDAO
from services.noticias_api import NoticiaAPI
import json

#Instanciando os objetos DAO
user_dao = UsuarioDAO()
relatorio_dao = RelatorioDAO()
estabelecimento_dao = EstabelecimentoDAO()
locais_dao = LocaisDAO()
noticia_api = NoticiaAPI()

#Funções
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
            print(f"Ocorreu um erro: {erro}", ". Digite apenas números válidos.")

def validar_credenciais(email, senha): #Função para validar email e senha colocados pelo usuário
    if len(senha) < 4 or " " in senha:
        raise ValueError("Sua senha precisa ter ao menos 4 caracteres e nenhum espaço.")
    if "@" not in email or len(email) < 8:
        raise ValueError("O email precisa ter @ e não pode ter menos de 8 caracteres.")

def exportar_json(): #Função para gerar o relatório de histórico de locais em JSON
    try:
        historico = locais_dao.listar_locais_buscados(usuario_atual._id_usuario)
        if historico is None:
            raise OSError("O histórico de locais buscados desta conta não foi encontrado.")
        else:
            lista_historico = []
            for local in historico:
                dados_local = {
                    "id_local": local[0],
                    "cidade": local[1],
                    "bairro": local[2],
                    "id_usuario": local[3],
                    }
                lista_historico.append(dados_local)
            with open("historico_minicity.json","w",encoding="utf-8") as arquivo:
                json.dump(lista_historico, arquivo, ensure_ascii=False, indent=4)
            print("\nO arquivo 'historico_minicity.json' foi gerado com sucesso!")
            print(f"Foram exportados {len(lista_historico)} locais.")

    except OSError as erro:
                    print("Ocorreu um erro durante a criação do arquivo: ", erro)    

usuario_atual = None #Variável que definirá o usuário que utilizará o código. Será definida no login
local_atual = None
login = False #Define se o login foi realizado

while not login: #Menu de login, permite a criação de uma conta e o login caso o usuário já possua uma conta
    print("\n=======================================")
    print("Bem-vindo à MiniCity!")
    print("Ainda não possui uma conta? Cadastre-se!")
    print("1 - Realizar cadastro.") #Opção para fazer o cadastro de uma nova conta
    print("Já possui uma conta? Faça o login!")
    print("2 - Login.") #Opção para logar em uma conta já existente
    print("3 - Sair.") #Sair do sistema sem realizar login
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
                print(f"Ocorreu um erro: {erro}")

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
                    print(f"Ocorreu um erro: {erro}")

        case 3:
            print("Encerrando sistema...")
            sys.exit()
        
        case _:
            print("Opção inválida. Digite uma opção válida do menu.")

opcao = -1

while opcao != 0:
    print("\n===== Menu MiniCity =====")
    print("1 - Geral") #Submenu com opções gerais
    print("2 - Consultar notícias e estabelecimentos.") #Submenu para consultar notícias próximas e estabelecimentos, além de buscar por locais
    print("3 - Escrever relatório cidadão.") #Submenu para escrever relatórios
    print("4 - Central do usuário.") #Submenu do usuário
    print("5 - Criar JSON.") #Opção para criar um relatório do histórico de locais buscados em JSON
    print("0 - Sair.") #Saída do sistema
    try:
        opcao = int(input("Digite o número da opção que você deseja: "))
    except ValueError:
        print("Opção inválida. Digite apenas números.")
        continue

    match opcao:
        case 1:
                while True:
                    print("\n======= Menu MiniCity - Geral =======")
                    print("1 - Conhecer a MiniCity.") #Opção para ver algumas informações a respeito da MiniCity
                    print("2 - Ver Planos.") #Opção para ver os planos disponíveis e assinar
                    print("3 - Declarar meu local atual.")
                    print("4 - Voltar.") #Volta ao menu principal
                    try:
                        opcao_geral = int(input("Digite o número da opção que você deseja: "))
                    except ValueError:
                        print("Opção inválida. Digite apenas números.")
                        continue
                    match opcao_geral:
                        case 1:
                            print("Bem-vindo(a) à MiniCity!!! \nA MiniCity é uma startup criada em Novembro de 2026 baseada nos famosos mini mapas de videogames. Temos intenção de ajudar na distribuição de notícias geograficamente relevantes para a população. Focamos em ajudar os usuários a conhecer melhor o seu redor, além de incentivar a prática da cidadania. ")
                            print("\nAtualmente, nossos projetos estão voltados para o desenvolvimento de mapas que exibirão notícias, relatórios de cidadãos e estabelecimentos bem avaliados de forma geolocalizada, facilitando o compartilhamento de notícias relevantes para a rotina das pessoas.")
                            print("\nAlém de simplesmente exibir notícias, a MiniCity deseja incentivar a participação do cidadão na sociedade. Os usuários poderão publicar relatórios falando sobre ocorrências como alagamentos ou lotações para ajudar outros usuários e moradores da região.")
                
                        case 2:
                            print("\nA MiniCity possui 3 planos diferentes: ")
                            print("""\nPlano Padrão: O plano padrão é gratuito e permite a utilização do aplicativo com todas as funcionalidades básicas, incluindo: 
Utilização dos mapas do aplicativo; 
Serviço de relatório cidadão; 
Salvamento de locais; 
Envio de notificações; 
Acompanhamento de notícias nacionais.""")
                            print("""\nPlano Empreendedor: O plano empreendedor é voltado para comerciantes que desejam impulsionar seus estabelecimentos dentro dos mapas da MiniCity, garantindo funcionalidades como: 
Todos os benefícios do plano básico;
Seu estabelecimento será impulsionado no mapa da Mini City, permitindo que ele apareça a distâncias maiores e para mais pessoas;
Seu estabelecimento ganhará um selo especial no mapa;
Seu app da MiniCity não terá mais anúncios.""")
                            print("""\nPlano Empreendedor+: É a evolução do plano empreendedor, potencializando seus efeitos e garantindo benefícios como: 
Todos os benefícios do plano empreendedor;
Seu estabelecimento ganhará um selo de maior nível no mapa;
Você poderá impulsionar mais de um estabelecimento.""")

                            print(f"Seu plano atual é: {usuario_atual._assinatura}")

                            print("Deseja alterar seu plano? Se sim, digite o número do plano que você deseja.")
                            print("1 - Padrão - Gratuito")
                            print("2 - Empreendedor - R$50,00 mensais")
                            print("3 - Empreendedor+ - R$75,00 mensais")
                            print("4 - Não alterar")
                            try:
                                opcao_plano = int(input("Digite o número da opção que você deseja: "))
                            except ValueError:
                                print("Opção inválida. Digite apenas números.")
                                continue
                            match opcao_plano:
                                case 1:
                                    if usuario_atual._assinatura == "Padrão":
                                        print("Seu plano já é o padrão. Ele não foi alterado.")
                                    else:
                                        usuario_atual._assinatura = "Padrão"
                                        user_dao.alterar_plano(usuario_atual._id_usuario, usuario_atual._assinatura)
                                        print("Plano atual: Padrão")

                                case 2:
                                    if usuario_atual._assinatura == "Empreendedor":
                                        print("Seu plano já é o empreendedor. Ele não foi alterado.")
                                    else:
                                        usuario_atual._assinatura = "Empreendedor"
                                        user_dao.alterar_plano(usuario_atual._id_usuario, usuario_atual._assinatura)
                                        print("Plano atual: Empreendedor")

                                case 3:
                                    if usuario_atual._assinatura == "Empreendedor+":
                                        print("Seu plano já é o empreendedor+. Ele não foi alterado.")
                                    else:
                                        usuario_atual._assinatura = "Empreendedor+"
                                        user_dao.alterar_plano(usuario_atual._id_usuario, usuario_atual._assinatura)
                                        print("Plano atual: Empreendedor+")  

                                case 4:
                                    print("Voltando ao menu anterior...")                           

                        case 3:
                            cidade = validar_texto("Digite a cidade em que você se encontra atualmente: ")
                            bairro = validar_texto("Digite o bairro em que você se encontra atualmente: ")
                            endereco = validar_texto("Digite a rua em que você se encontra atualmente: ")

                            local_atual = Local(cidade=cidade, bairro=bairro, endereco=endereco)

                            print("Local declarado com sucesso!")

                        case 4:
                            print("Voltando ao menu anterior...")
                            break

                        case _:
                            print("Opção inválida. Digite uma opção válida do menu.")

        case 2:
            while True:    #Submenu do sistema - trata sobre as consultas dos mapas 
                print("\n======= Menu MiniCity - Mapa =======")
                print("1 - Ver meu local.") # Mostra o local em que o usuário se encontra atualmente
                print("2 - Ver notícias perto de mim.") # Mostra notícias que ocorreram perto do local em que o usuário se encontra atualmente
                print("3 - Ver estabelecimentos e comércios recomendados.") # Mostra estabelecimentos recomendados
                print("4 - Buscar local.") # Busca um local para o usuário ver as notícias
                print("5 - Ver histórico de locais buscados.") # Mostra o histórico de locais que o usuário buscou
                print("6 - Voltar.") #Volta ao menu principal
                try:
                    opcao_mapa = int(input("Digite o número da opção que você deseja: "))
                except ValueError:
                    print("Opção inválida. Digite apenas números.")
                    continue

                match opcao_mapa:
                    case 1:
                        if local_atual is None:
                            print("É necessário definir seu local atual antes. Faça isso na opção 3 do submenu Geral.")
                        else:                        
                            print("Atualmente, você se encontra em: ")
                            print(local_atual)

                    case 2:
                        if local_atual is None:
                            print("É necessário definir seu local atual antes. Faça isso na opção 3 do submenu Geral.")
                        else:
                            noticias = noticia_api.buscar_noticias(local_atual._bairro, local_atual._cidade)
                            if noticias is None:
                                print("Nenhuma notícia foi encontrada.")
                            else:
                                for noticia in noticias:
                                    print("\n========================")
                                    print(f"{noticia['title']}")
                                    print(f"Fonte: {noticia['source']['name']} | {noticia['publishedAt'][:10]}")
                                    print(f"Link: {noticia['url']}")     

                    case 3:
                        estabelecimentos = estabelecimento_dao.listar_estabelecimentos()
                        if estabelecimentos is None:
                            print("Nenhum estabelecimento foi encontrado.")
                        else:
                            for estabelecimento in estabelecimentos:
                                print("\n========================")
                                print(f"ID do estabelecimento: {estabelecimento[0]}")
                                print(f"Nome do estabelecimento: {estabelecimento[1]}")
                                print(f"Bairro: {estabelecimento[3]}")
                                print(f"Logradouro: {estabelecimento[2]}")
                                print(f"Link: {estabelecimento[4]}")

                    case 4:
                        cidade = validar_texto("Digite a cidade que você deseja buscar: ")
                        bairro = validar_texto("Digite o bairro que você deseja buscar: ")
                        locais_dao.gravar_local_buscado(cidade, bairro, usuario_atual._id_usuario)
                        noticias = noticia_api.buscar_noticias(bairro, cidade)
                        if noticias is None:
                            print("Nenhuma notícia foi encontrada.")
                        else:
                            for noticia in noticias:
                                print("\n========================")
                                print(f"{noticia['title']}")
                                print(f"Fonte: {noticia['source']['name']} | {noticia['publishedAt'][:10]}")
                                print(f"Link: {noticia['url']}")   

                    case 5:
                        historico = locais_dao.listar_locais_buscados(usuario_atual._id_usuario)
                        if historico is None:
                            print("O histórico não pôde ser recuperado. Confira se você já realizou uma busca.")
                        else: 
                            print("Apenas você pode ver seu histórico.")
                            for local in historico:
                                print("\n========================")
                                print(f"ID do usuário: {local[3]}")
                                print(f"ID do local: {local[0]}")
                                print(f"Cidade: {local[1]}")
                                print(f"Bairro: {local[2]}")


                    case 6:
                        print("Voltando ao menu anterior...")
                        break

                    case _:
                        print("Opção inválida. Digite uma opção válida do menu.")

        case 3:
            while True:  #Submenu do sistema - trata sobre os relatórios enviados pelo usuário | Aqui se encontra um CRUD
                print("\n======= Menu MiniCity - Relatório Cidadão =======") 
                print("1 - Escrever novo relatório.") #Create   
                print("2 - Ver todos os relatórios.") #Read
                print("3 - Procurar relatório pelo ID.") #Read    
                print("4 - Editar um relatório.") #Update  
                print("5 - Excluir um relatório.") #Delete
                print("6 - Voltar.") 
                try:
                    opcao_relatorio = int(input("Digite o número da opção que você deseja: "))
                except ValueError:
                    print("Opção inválida. Digite apenas números.")
                    continue

                match opcao_relatorio:
                    case 1: 
                        try: 
                            endereco_relatorio = validar_texto("Qual o endereço da ocorrência? ")
                            if len(endereco_relatorio) > 200:
                                raise ValueError("O endereço não pode conter mais do que 200 caracteres.")
                            
                            texto_relatorio = validar_texto("Qual foi a ocorrência? ")
                            if len(texto_relatorio) > 400:
                                raise ValueError("O relatório não pode conter mais do que 400 caracteres.")

                            relatorio_dao.fazer_relatorio(usuario_atual._id_usuario, texto_relatorio, endereco_relatorio)

                        except ValueError as erro:
                            print(f"Ocorreu um erro: {erro}") 

                    case 2:
                        relatorios = relatorio_dao.listar_relatorios()
                        if relatorios is None:
                            print("Nenhum relatório foi publicado.")  
                        else:
                            for relatorio in relatorios:
                                print("\n========================")
                                print(f"ID do relatório: {relatorio[0]}")
                                print(f"Endereço da ocorrência: {relatorio[2]}")
                                print(f"Relatório: {relatorio[1]}")  

                    case 3:
                        relatorio_procurado = ler_inteiro("Digite o ID do relatório que você deseja buscar: ")
                        relatorio = relatorio_dao.buscar_id_relatorio(relatorio_procurado)
                        if relatorio is None:
                            print("Nenhum relatório foi encontrado.")
                        else:
                            print("\n========================")
                            print(f"ID do relatório: {relatorio[0]}")
                            print(f"Endereço da ocorrência: {relatorio[2]}")
                            print(f"Relatório: {relatorio[1]}")      

                    case 4:
                        relatorio_editado = ler_inteiro("Digite o ID do relatório que você deseja editar: ")
                        relatorio_encontrado = relatorio_dao.buscar_id_relatorio(relatorio_editado)
                        if relatorio_encontrado is None:
                            print("Nenhum relatório foi encontrado.")

                        elif relatorio_encontrado[3] != usuario_atual._id_usuario:
                            print("Não é possível editar os relatórios de outros usuários.")

                        else:
                            relatorio = relatorio_dao.editar_relatorio(relatorio_editado)
                            if relatorio is not None:
                                print("\n========================")
                                print(f"ID do relatório: {relatorio[0]}")
                                print(f"Endereço da ocorrência: {relatorio[2]}")
                                print(f"Relatório: {relatorio[1]}")  

                    case 5:
                        relatorio_excluido = ler_inteiro("Digite o ID do relatório que você deseja excluir: ")
                        relatorio = relatorio_dao.buscar_id_relatorio(relatorio_excluido)
                        if relatorio is None:
                            print("Nenhum relatório foi encontrado.")

                        elif relatorio[3] != usuario_atual._id_usuario:
                            print("Não é possível excluir os relatórios de outros usuários.")

                        else:
                            print("\n========================")
                            print(f"ID do relatório: {relatorio[0]}")
                            print(f"Endereço da ocorrência: {relatorio[2]}")
                            print(f"Relatório: {relatorio[1]}") 

                            relatorio_dao.excluir_relatorio(relatorio_excluido) 
                    
                    case 6:
                        print("Voltando ao menu anterior...")
                        break

                    case _:
                        print("Opção inválida. Digite uma opção válida do menu.")

        case 4:
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
                                print(f"Ocorreu um erro: {erro}")
                    

                    case 3:
                        try:
                            username = validar_texto("Digite seu nome de usuário: ")
                            email = validar_texto("Digite seu email: ")
                            senha = validar_texto("Sua senha precisa conter ao menos 4 caracteres e não pode ter espaços. Digite sua senha: ")
                            validar_credenciais(email, senha)

                            novo_usuario = Usuario(username, senha, email)
                            user_dao.cadastrar_usuario(novo_usuario)
                        except ValueError as erro:
                            print(f"Ocorreu um erro: {erro}")

                    case 4:
                        usuarios = user_dao.listar_usuarios()
                        if usuarios is None:
                            print("Nenhum usuário cadastrado.")
                        else:
                            for usuario in usuarios:
                                print("\n========================")
                                print(f"ID do usuário: {usuario[0]}")
                                print(f"Nome de usuário: {usuario[1]}")
                                print(f"Email: {usuario[3]}")
                                print(f"Plano: {usuario[4]}")

                    case 5:
                        username_procurado = validar_texto("Digite o Username da conta que você deseja buscar: ")
                        usuario = user_dao.buscar_nome_usuario(username_procurado)
                        if usuario is None:
                            print("Nenhum usuário foi encontrado.")
                        else:
                            print("\n========================")
                            print(f"ID do usuário: {usuario[0]}")
                            print(f"Nome de usuário: {usuario[1]}")
                            print(f"Email: {usuario[3]}")
                            print(f"Plano: {usuario[4]}")

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
                            print(f"ID do usuário: {usuario[0]}")
                            print(f"Nome de usuário: {usuario[1]}")
                            print(f"Email: {usuario[3]}")
                            print(f"Plano: {usuario[4]}")    

                    case 7:
                        usuario_excluido = validar_texto("Digite o nome do usuário que você deseja excluir: ")
                        usuario = user_dao.buscar_nome_usuario(usuario_excluido)
                        if usuario is None:
                            print("Nenhum usuário foi encontrado.")
                        else:
                            print("\n========================")
                            print(f"ID do usuário: {usuario[0]}")
                            print(f"Nome de usuário: {usuario[1]}")
                            print(f"Email: {usuario[3]}")
                            print(f"Plano: {usuario[4]}")

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

        case 5:
            print("\nEsta opção irá gerar um relatório .json sobre o histórico de locais que você buscou na MiniCity.")
            print("Gerando relatório...")
            exportar_json()

        case 0:
            print("Encerrando sistema...")
            break
        
        case _:
            print("Opção inválida. Digite uma opção válida do menu.")

