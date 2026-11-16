class Local:
    #Construtor da classe Local
    def __init__(self, cidade, bairro, endereco):
        self._cidade = cidade
        self._bairro = bairro
        self._endereco = endereco

    #Método para exibir o objeto Local
    def __str__(self):
        return f" Cidade: {self._cidade} | Bairro: {self._bairro} | \nEndereço: {self._endereco}"




