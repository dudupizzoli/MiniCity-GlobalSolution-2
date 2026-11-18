import hashlib
#Função para transformar senhas em hash
def gerar_hash(senha):
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()
